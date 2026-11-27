"""Metadata-retrieval coverage audit; no scholarly-admission decisions."""
from __future__ import annotations
import collections
import datetime as dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE=ROOT/"research/corpus_v1"
IDX=BASE/"indexed"
OUT=IDX/"retrieval_audit.json"

def norm(s):
    return re.sub(r"[^a-z0-9]","",str(s or "").lower())

def statdict(counter):
    return dict(sorted(counter.items(), key=lambda p:(-p[1],p[0])))

def main():
    summary=json.loads((IDX/"search_summary.json").read_text(encoding="utf-8"))
    logs=json.loads((IDX/"query_audit.json").read_text(encoding="utf-8"))
    with (IDX/"indexed_candidates.jsonl").open(encoding="utf-8") as f:
        entries=[json.loads(line) for line in f if line.strip()]
    old=json.loads((BASE/"discovery-leads-2026-11-26.json").read_text(encoding="utf-8"))
    old_titles={norm(x.get("title")) for x in old["candidates"]}
    old_dois={str(x["doi"]).lower() for x in old["candidates"] if x.get("doi")}
    overlaps=[x for x in entries if norm(x.get("title")) in old_titles or (x.get("doi") and x["doi"].lower() in old_dois)]

    errs=collections.Counter()
    by_engine=collections.defaultdict(lambda:collections.Counter())
    by_facet=collections.defaultdict(lambda:collections.Counter())
    by_era=collections.defaultdict(lambda:collections.Counter())
    total_expected=0
    for q in logs:
        key=q.get("engine","unknown")
        status=q.get("status","unknown")
        by_engine[key][status]+=1
        by_facet[q.get("facet","unknown")][status]+=1
        by_era[str(q.get("era"))][status]+=1
        if q.get("result_cap_applied"):by_engine[key]["capped_first_page"]+=1
        total_expected+=int(q.get("retrieved") or 0)
        if status=="error":
            msg=str(q.get("error","unknown"))
            code=re.search(r"HTTP\s+(\d{3})",msg)
            errs[(key,code.group(1) if code else msg.split(":")[0][:30])]+=1
    tp=collections.Counter(x.get("type","unknown") for x in entries)
    overlap_hist=collections.Counter(x.get("best_title_token_overlap",0) for x in entries)
    years=collections.Counter(str((int(x["year"])//10)*10)+"s" for x in entries if isinstance(x.get("year"),int))
    candidate_by_index=collections.Counter(e for x in entries for e in x.get("found_in",[]))
    source_multiplicity=collections.Counter(len(x.get("found_in",[])) for x in entries)
    titles_top={}
    for facet in [*(f"M{x}" for x in range(1,9)),*(f"A{x}" for x in range(1,7))]:
        category="method_search_tags" if facet.startswith("M") else "biomedical_application_tags"
        subset=[x for x in entries if facet in x[category]]
        high=sorted(subset,key=lambda x:(-int(x.get("best_title_token_overlap") or 0),-(x.get("citation_count_index") or 0)))
        titles_top[facet]=[{"title":x.get("title"),"year":x.get("year"),"venue":x.get("venue"),"doi":x.get("doi")}
                         for x in high[:5]]
    report={
      "kind":"INDEX_COVERAGE_AUDIT_NOT_ACADEMIC_ADMISSION",
      "generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
      "retrieval_cutoff":summary.get("cutoff"),
      "total_queries":len(logs),
      "query_counts_by_engine":{k:dict(v) for k,v in sorted(by_engine.items())},
      "query_counts_by_facet":{k:dict(v) for k,v in sorted(by_facet.items())},
      "query_counts_by_era":{k:dict(v) for k,v in sorted(by_era.items())},
      "query_error_reasons":[{"engine":k[0],"error_type":k[1],"count":v} for k,v in errs.most_common()],
      "actual_retrieved_items":total_expected,
      "unique_indexed_records":len(entries),
      "records_with_doi":sum(bool(x.get("doi")) for x in entries),
      "work_type_distribution":statdict(tp),
      "query_title_token_overlap_histogram":dict(sorted(overlap_hist.items())),
      "by_publication_decade":dict(sorted(years.items())),
      "by_retrieval_source":statdict(candidate_by_index),
      "index_support_multiplicity":dict(sorted(source_multiplicity.items())),
      "previous_147_exact_title_or_doi_overlap_count":len(overlaps),
      "previous_147_total":len(old["candidates"]),
      "examples_by_facet_for_manual_review":titles_top,
      "all_admission_pending":all(x.get("admission_status")=="pending" for x in entries),
      "all_scientific_quality_unreviewed":all(x.get("scientific_quality_review")=="not_performed" for x in entries),
      "interpretation":[
         "Index hit count sums are inflated by overlapping queries and not unique studies.",
         "Search is first-page capped and a portion of queries can be rate-limited; no recall saturation has been proven.",
         "Topic tags are inherited from the queries that retrieved each item, not expert validation.",
         "Book type labels may include ambiguous registrations; ISBN, publisher and edition remain to verify.",
         "This audit does not establish formal academic admission or clinical evidence maturity."
      ]
    }
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    compact={k:report[k] for k in ("total_queries","query_counts_by_engine","unique_indexed_records","records_with_doi","previous_147_exact_title_or_doi_overlap_count","all_admission_pending")}
    print("AUDIT "+json.dumps(compact,ensure_ascii=False),flush=True)

if __name__=="__main__":main()
