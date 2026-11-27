"""Reproducible *discovery* of scholarly works from external bibliographic indices.

Output is NOT an admission-approved scholarly corpus. Each record is pending.
Uses Crossref, Europe PMC, and optional keyless OpenAlex; respects API caps.
Run: python -m scripts.research.retrieve_index
     ATLAS_SEARCH_MAX_QUERIES=6 python -m scripts.research.retrieve_index
"""
from __future__ import annotations
import concurrent.futures
import threading
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PLAN_PATH=ROOT/"research/corpus_v1/INDEX_SEARCH_PLAN_V2.json"
OUTPUT=ROOT/"research/corpus_v1/indexed"
OUTPUT.mkdir(parents=True,exist_ok=True)
PLAN=json.loads(PLAN_PATH.read_text(encoding="utf-8"))
CUTOFF=PLAN["cutoff"]
UA="Physics-AI-Methods-Atlas-Corpus-Discovery/0.1 (scholarly-metadata-only; +https://github.com/TianminWang/physics-ai-methods-atlas)"
MAX_QUERIES=int(os.environ.get("ATLAS_SEARCH_MAX_QUERIES","0"))
ENABLE_OPENALEX=os.environ.get("ATLAS_OPENALEX","1")=="1"
TERMS=set("of for in on to an a and or the with from using via through approach framework towards based methods method study studies analysis model modeling models learning deep machine data system systems algorithm algorithms survey review clinical patients patient".split())
records={}
lookup={}
stats=[]
failures=[]
snapshot_time=dt.datetime.now(dt.timezone.utc).isoformat()
config_digest=hashlib.sha256(PLAN_PATH.read_bytes()).hexdigest()[:16]
RECORD_LOCK=threading.RLock()
HOST_LIMITS={"api.crossref.org":threading.Semaphore(5),"www.ebi.ac.uk":threading.Semaphore(2),"api.openalex.org":threading.Semaphore(1)}

def words(t):
    return [w for w in re.findall(r"[a-z0-9]+",t.lower()) if len(w)>2 and w not in TERMS]

def titlekey(t):
    return re.sub(r"[^a-z0-9]","",t.lower())

def normal_doi(x):
    if not x:return ""
    x=str(x).strip().lower()
    x=re.sub(r"^https?://(?:dx[.])?doi[.]org/","",x)
    return x.strip().replace(" ","")

def request(url,retries=3):
    for i in range(retries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
            with urllib.request.urlopen(req,timeout=25) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503,504) and i<retries-1:
                time.sleep(min(6,1.7**(i+1)))
                continue
            raise RuntimeError(f"HTTP {e.code}: {url[:120]}")
        except (OSError,ValueError) as e:
            if i<retries-1:
                time.sleep(min(6,1.7**(i+1)))
                continue
            raise RuntimeError(f"{type(e).__name__}: {e}")

def clean_title(x):
    if isinstance(x,list):return str(x[0]) if x else ""
    return str(x or "")

def year_from_crossref(x):
    for f in ("published","issued","published-online","published-print","created"):
        v=(x.get(f) or {}).get("date-parts") or []
        if v and v[0] and isinstance(v[0][0],int):
            return v[0][0]
    return None

def date_from_crossref(x):
    for f in ("published","issued","published-online","published-print"):
        v=(x.get(f) or {}).get("date-parts") or []
        if v and v[0]:
            z=v[0];return "%04d-%02d-%02d" % (z[0],z[1] if len(z)>1 else 1,z[2] if len(z)>2 else 1)
    return None

def normal(x,engine):
    if engine=="crossref":
        au=x.get("author") or []
        authors=[" ".join([str(y.get("given","")),str(y.get("family",""))]).strip() for y in au[:6]]
        title=clean_title(x.get("title"))
        venue=clean_title(x.get("container-title"))
        return {"title":title,"year":year_from_crossref(x),"published_date":date_from_crossref(x),
         "doi":normal_doi(x.get("DOI")),"work_type":x.get("type") or "unknown",
         "authors":authors,"venue":venue,"source_url":x.get("URL") or "",
         "citation_count_index":x.get("is-referenced-by-count"),"isbn":x.get("ISBN") or []}
    if engine=="europepmc":
        au=x.get("authorString") or ""
        authors=[a.strip() for a in au.split(",")[:6] if a.strip()]
        return {"title":x.get("title") or "","year":int(x.get("pubYear")) if str(x.get("pubYear","")).isdigit() else None,
         "published_date":x.get("firstPublicationDate"),
         "doi":normal_doi(x.get("doi")),"work_type":x.get("pubType") or "article",
         "authors":authors,"venue":x.get("journalTitle") or "",
         "source_url":("https://europepmc.org/article/MED/"+x["id"]) if x.get("source")=="MED" and x.get("id") else "https://europepmc.org/search?query="+urllib.parse.quote(x.get("title") or ""),
         "pmid":x.get("pmid"),"citation_count_index":int(x.get("citedByCount") or 0)}
    if engine=="openalex":
        source=(x.get("primary_location") or {}).get("source") or {}
        au=x.get("authorships") or []
        return {"title":x.get("title") or "","year":x.get("publication_year"),
         "published_date":x.get("publication_date"),
         "doi":normal_doi(x.get("doi")),"work_type":x.get("type") or "unknown",
         "authors":[(z.get("author") or {}).get("display_name","") for z in au[:6]],
         "venue":source.get("display_name") or "",
         "source_url":x.get("id") or "",
         "openalex_id":x.get("id"),"citation_count_index":x.get("cited_by_count")}
    raise ValueError(engine)

def add(x,engine,facet,qid,query_text,search_rank):
    c=normal(x,engine)
    title=c.get("title","").strip()
    y=c.get("year")
    if not title or len(title)<12 or not isinstance(y,int) or y<1900 or y>2026:return False
    pub=c.get("published_date")
    if pub and pub>CUTOFF:return False
    doi=c.get("doi") or ""
    key=("doi:"+doi) if doi else "title:"+titlekey(title)+":"+str(y)
    title_id="title:"+titlekey(title)+":"+str(y)
    oldkey=lookup.get(key) or lookup.get(title_id)
    if oldkey and oldkey not in records:oldkey=None
    entry=records.get(oldkey) if oldkey else None
    if entry is None:
        entry={
            "candidate_id":"idx_"+hashlib.sha1(key.encode()).hexdigest()[:15],
            "title":title,"year":y,"doi":doi or None,"authors":c.get("authors") or [],
            "venue":c.get("venue") or "","type":c.get("work_type") or "unknown",
            "source_urls":[],"isbn":c.get("isbn",[]),"pmid":c.get("pmid"),"openalex_id":c.get("openalex_id"),
            "method_search_tags":[],"biomedical_application_tags":[],
            "found_in":[],"query_ids":[],"first_seen_at":snapshot_time,
            "admission_status":"pending","publication_integrity_check":"not_completed",
            "scientific_quality_review":"not_performed",
            "citation_count_index":c.get("citation_count_index")
        }
        records[key]=entry
        oldkey=key
    lookup[key]=oldkey
    lookup[title_id]=oldkey
    if doi and not entry["doi"]:entry["doi"]=doi;lookup["doi:"+doi]=oldkey
    if c.get("source_url") and c["source_url"] not in entry["source_urls"] and len(entry["source_urls"])<4:
        entry["source_urls"].append(c["source_url"])
    if c.get("venue") and not entry["venue"]:entry["venue"]=c["venue"]
    if c.get("authors") and not entry["authors"]:entry["authors"]=c["authors"]
    if c.get("isbn") and not entry.get("isbn"):entry["isbn"]=c["isbn"]
    if c.get("pmid") and not entry.get("pmid"):entry["pmid"]=c["pmid"]
    if c.get("openalex_id") and not entry.get("openalex_id"):entry["openalex_id"]=c["openalex_id"]
    if engine not in entry["found_in"]:entry["found_in"].append(engine)
    if qid not in entry["query_ids"]:entry["query_ids"].append(qid)
    if facet!="BOOK":
        tagfield="biomedical_application_tags" if facet.startswith("A") else "method_search_tags"
        if facet not in entry[tagfield]:entry[tagfield].append(facet)
    title_terms=set(words(title))
    qterms=set(words(query_text))
    overlap=len(title_terms&qterms)
    old=entry.get("best_title_token_overlap",0)
    if overlap>old:entry["best_title_token_overlap"]=overlap
    return True

def run_query(engine,facet,phrase,era=None,stype=None,index=0):
    params={}
    if engine=="crossref":
        filt=[]
        if era:
            filt=[f"from-pub-date:{era[1]}",f"until-pub-date:{era[2]}"]
        else:filt=[f"until-pub-date:{CUTOFF}"]
        if stype:filt.append("type:"+stype)
        params={"query.title":phrase,"rows":PLAN["crossref_firstpage_per_era"],
          "filter":",".join(filt)}
        url="https://api.crossref.org/works?"+urllib.parse.urlencode(params)
    elif engine=="europepmc":
        tokens=words(phrase)[:4]
        query=" AND ".join(f"TITLE_ABS:{t}" for t in tokens)
        if era:query+=f" AND FIRST_PDATE:[{era[1]} TO {era[2]}]"
        else:query+=f" AND FIRST_PDATE:[1900-01-01 TO {CUTOFF}]"
        params={"query":query,"format":"json","resultType":"lite","pageSize":PLAN["europepmc_firstpage_per_era"]}
        url="https://www.ebi.ac.uk/europepmc/webservices/rest/search?"+urllib.parse.urlencode(params)
    elif engine=="openalex":
        params={"search.title_and_abstract":phrase,"per_page":PLAN["openalex_firstpage"],
             "filter":"to_publication_date:"+CUTOFF,
             "select":"id,title,publication_year,publication_date,doi,type,cited_by_count,primary_location,authorships"}
        url="https://api.openalex.org/works?"+urllib.parse.urlencode(params)
    else:raise ValueError(engine)
    qid=f"{engine}-{facet}-{index:03d}"+(f"-{era[0]}" if era else "")+(f"-{stype}" if stype else "")
    log={"id":qid,"engine":engine,"facet":facet,"phrase":phrase,"era":era[0] if era else None,
         "filter_type":stype,"request_url":url,"status":"unknown","retrieved":0}
    try:
        host=urllib.parse.urlparse(url).netloc
        sem=HOST_LIMITS.get(host,threading.Semaphore(1))
        with sem:
            obj=request(url)
        if engine=="crossref":
            items=(obj.get("message") or {}).get("items",[])
            log["index_total_hits"]=(obj.get("message") or {}).get("total-results")
        elif engine=="europepmc":
            items=(obj.get("resultList") or {}).get("result",[])
            log["index_total_hits"]=obj.get("hitCount")
        else:
            items=obj.get("results",[])
            log["index_total_hits"]=(obj.get("meta") or {}).get("count")
        log["retrieved"]=len(items)
        log["limit"]=params.get("rows",params.get("pageSize",params.get("per_page")))
        log["result_cap_applied"]=isinstance(log["index_total_hits"],int) and log["index_total_hits"]>len(items)
        # Do not treat index hit counts as eligible article counts.
        selected=0
        for k,x in enumerate(items,1):
            try:
                with RECORD_LOCK:
                    if add(x,engine,facet,qid,phrase,k):selected+=1
            except Exception as e:
                failures.append({"query":qid,"record_rank":k,"error":str(e)[:130]})
        log["valid_metadata_selected"]=selected
        log["status"]="ok"
    except Exception as e:
        log["status"]="error";log["error"]=str(e)[:250]
        failures.append({"query":qid,"error":str(e)[:300]})
    stats.append(log)
    if len(stats)%30==0:
        print(f"PROGRESS queries={len(stats)} records={len(records)} last={qid} status={log['status']}",flush=True)

def summarize():
    entries=list(records.values())
    entries.sort(key=lambda x:(x["year"],x["title"].lower()))
    m=Counter(t for x in entries for t in x["method_search_tags"])
    a=Counter(t for x in entries for t in x["biomedical_application_tags"])
    engines=Counter(e for x in entries for e in x["found_in"])
    status=Counter(q["status"] for q in stats)
    report={
       "retrieval_version":PLAN["version"],"cutoff":CUTOFF,"started_at":snapshot_time,
       "completed_at":dt.datetime.now(dt.timezone.utc).isoformat(),
       "query_plan_sha256_16":config_digest,"source_status":"indexed_discovery_only",
       "queries_executed":len(stats),"by_query_status":dict(status),
       "index_total_hits_sum_not_unique_or_eligible":sum(x.get("index_total_hits") or 0 for x in stats),
       "total_source_records_in_first_pages":sum(x["retrieved"] for x in stats),
       "unique_candidates":len(entries),"papers_and_proceedings":sum(x["type"] not in ("book","monograph","edited-book","reference-book") for x in entries),
       "books_and_monographs":sum(x["type"] in ("book","monograph","edited-book","reference-book") for x in entries),
       "with_doi":sum(bool(x["doi"]) for x in entries),
       "by_method_facet":dict(sorted(m.items())),"by_biomedical_facet":dict(sorted(a.items())),
       "by_index":dict(engines),"pending":len(entries),"failed_queries":len([x for x in stats if x["status"]!="ok"]),
       "methodology_notes":[
          "These are metadata search hits, not a comprehensive field census or approved publications.",
          "Queries draw first page per era, limits are recorded per query; total hits are not independent or eligible studies.",
          "Cited-by-count is stored only for retrieval context, never an admission rating.",
          "Basic DOI/title/year dedup can miss version equivalences; formal dedup and quality screening remain required.",
          "No peer-review validation, retraction audit, full-text methods assessment or ontology mapping is implied."
       ]
    }
    (OUTPUT/"search_summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUTPUT/"query_audit.json").write_text(json.dumps(stats,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUTPUT/"errors.json").write_text(json.dumps(failures,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (OUTPUT/"indexed_candidates.jsonl").open("w",encoding="utf-8") as f:
        for x in entries:f.write(json.dumps(x,ensure_ascii=False,separators=(",",":"))+"\n")
    print("SUMMARY "+json.dumps({k:report[k] for k in ("queries_executed","unique_candidates","with_doi","books_and_monographs","by_query_status","by_method_facet","by_biomedical_facet")},ensure_ascii=False),flush=True)

def main():
    tasks=[]
    eras=PLAN["eras"]
    for facet,phrases in PLAN["method_app_facet_queries"].items():
        for i,phrase in enumerate(phrases,1):
            for era in eras:
                tasks.append(("crossref",facet,phrase,era,None,i))
    # Fewer, targeted book-type queries.
    for i,phrase in enumerate(PLAN["books_queries"],1):
        tasks.append(("crossref","BOOK",phrase,None,"book",i))
        # Crossref registers some technical books as monographs.
        tasks.append(("crossref","BOOK",phrase,None,"monograph",i))
    # EuropePMC biomedical-only: two era windows to recover older clinical literature.
    mederas=[("historic","1900-01-01","2014-12-31"),("recent","2015-01-01",CUTOFF)]
    for facet,phrases in PLAN["method_app_facet_queries"].items():
        if not facet.startswith("A"):continue
        for i,phrase in enumerate(phrases,1):
            for era in mederas:tasks.append(("europepmc",facet,phrase,era,None,i))
    # Keyless OpenAlex is a complementary sample only; obey daily budget if throttled.
    if ENABLE_OPENALEX:
        for facet,phrases in PLAN["method_app_facet_queries"].items():
            for i,phrase in enumerate(phrases[:2],1):
                tasks.append(("openalex",facet,phrase,None,None,i))
    print("TASKS "+str(len(tasks))+" total, max="+str(MAX_QUERIES),flush=True)
    if MAX_QUERIES>0:tasks=tasks[:MAX_QUERIES]
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda args: run_query(*args),tasks))
    finally:
        stats.sort(key=lambda q:q["id"])
        summarize()
    success=sum(q["status"]=="ok" for q in stats)
    if not success:
        print("ERROR: all external metadata requests failed",file=sys.stderr)
        return 2
    return 0

if __name__=="__main__":
    sys.exit(main())
