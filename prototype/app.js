"use strict";
(() => {
  const $ = id => document.getElementById(id);
  const txt = {
    zh: {
      prototype:"方法谱系 · v0.5 原型",repository:"GitHub 仓库",
      eyebrow:"WORKFLOW × GENEALOGY", heading:"从研究问题，到方法演进。",
      subtitle:"一条研究主轴，多个可复用的方法家族。选择研究环节，再沿证据支持的改进与融合关系探索方法谱系。",
      prototypeFlag:"交互布局验证原型",axisTitle:"研究主轴",clearStage:"显示全部环节",
      stageHint:"点击环节，高亮相关功能和方法演进边。颜色代表研究问题，而非方法优劣。",
      graphTitle:"方法演化图谱",fitView:"适应窗口",searchLabel:"搜索方法",
      taxonomyToggle:"显示分类边",panHint:"拖动画布 · 点击节点或连线 · 缩放",
      legendEvolution:"方法改进",legendFusion:"技术融合",legendTaxonomy:"分类/特殊化",legendFunction:"环节 → 方法功能",
      detailTitle:"方法与证据",emptyTitle:"选择方法或关系",emptyText:"点击方法节点或演化连线，查看核心思想、技术瓶颈和代表论文。",
      scopeTitle:"原型范围",scopeText:"仅展示三个真实方法分支以验证布局和信息层级。学术数据来自仓库权威记录；原型不是完整知识库。",
      method:"方法",roles:"研究环节如何使用这些方法",more:"条功能关联",
      methods:"个方法",edges:"条方法关联",coreIdea:"核心思想",tradeoff:"代价与局限",
      families:"相关方法家族",startHere:"优先阅读（非强制）",landmark:"里程碑及其他文献",
      innovation:"方法变化",bottleneck:"针对的技术瓶颈",affected:"关联研究环节",
      evidence:"证据论文",source:"查看原始数据记录",functional:"研究环节中的作用",
      type_extends:"技术扩展",type_combines:"技术融合",type_specializes:"方法分类",
      noRoles:"此筛选下没有直接功能关系",noSources:"这一层暂未关联文献",
      error:"原型数据无法加载。请先执行数据构建脚本，再使用 HTTP 服务器访问。"
    },
    en: {
      prototype:"Method genealogy · v0.5 prototype",repository:"GitHub repository",
      eyebrow:"WORKFLOW × GENEALOGY",heading:"From research questions to evolving methods.",
      subtitle:"One workflow, many reusable method families. Select a research stage and explore evidence-backed extensions and combinations.",
      prototypeFlag:"Interactive layout prototype",axisTitle:"Research workflow",clearStage:"Show all stages",
      stageHint:"Select a stage to highlight relevant roles and improvements. Colors encode research functions, not rankings.",
      graphTitle:"Method genealogy",fitView:"Fit view",searchLabel:"Search methods",
      taxonomyToggle:"Show taxonomy edges",panHint:"Drag canvas · click a node or edge · zoom",
      legendEvolution:"Method extension",legendFusion:"Method fusion",legendTaxonomy:"Classification",legendFunction:"Stage → method role",
      detailTitle:"Methods & evidence",emptyTitle:"Select a method or relation",emptyText:"Click a method node or evolution edge to inspect the core idea, technical bottleneck and references.",
      scopeTitle:"Prototype scope",scopeText:"Only three real method lineages are shown to validate layout and information hierarchy; source facts remain in the main Atlas.",
      method:"Method",roles:"Functional roles in research",more:"other roles",
      methods:"methods",edges:"method links",coreIdea:"Core idea",tradeoff:"Limitations and costs",
      families:"Related families",startHere:"Suggested reading (optional)",landmark:"Landmarks and related papers",
      innovation:"What changed",bottleneck:"Target bottleneck",affected:"Relevant research stages",
      evidence:"Evidence papers",source:"Open canonical data record",functional:"Functional role",
      type_extends:"Extension",type_combines:"Fusion",type_specializes:"Taxonomy",
      noRoles:"No directly linked roles for this filter",noSources:"No paper linked at this level",
      error:"Preview data could not load. Build the data file, then serve the directory over HTTP."
    }
  };
  const stageName={
    "stage.physics-forward":["正向模拟","Forward simulation"],
    "stage.observation":["观测模型","Observation model"],
    "stage.inverse-calibration":["个体化反演","Inverse inference"],
    "stage.prediction-uq":["可信预测","Prediction / UQ"],
    "stage.intervention-planning":["干预规划","Intervention"],
    "stage.continual-update":["持续更新","Model updating"]
  };
  const state={lang:"zh",track:"operator",stage:null,family:null,query:"",taxonomy:true,chosen:null,scale:1,panX:0,panY:0};
  let db, nodes, edges,layout;
  const repo="https://github.com/TianminWang/physics-ai-methods-atlas/blob/main/";
  function phrase(k){return txt[state.lang][k]||k;}
  function node(id){return nodes[id];}
  function name(id){return node(id)?.label[state.lang]||id;}
  function track(){return db.tracks.find(t=>t.id===state.track);}
  function elem(tag,cl,text){
    const x=document.createElement(tag);
    if(cl)x.className=cl;
    if(text!==undefined)x.textContent=String(text);
    return x;
  }
  function btn(cl,label,click){
    const b=elem("button",cl,label);b.type="button";b.addEventListener("click",click);return b;
  }
  function external(href,label,cl){
    const a=elem("a",cl,label);
    if(typeof href==="string" && /^https:\/\/[a-z0-9.-]+\//i.test(href)){
      a.href=href;a.rel="noopener noreferrer";a.target="_blank";
    }return a;
  }
  function setLanguage(){
    document.documentElement.lang=state.lang==="zh"?"zh-CN":"en";
    document.querySelectorAll("[data-i18n]").forEach(x=>x.textContent=phrase(x.dataset.i18n));
    $("lang-toggle").textContent=state.lang==="zh"?"EN":"中文";
    $("search").placeholder=state.lang==="zh"?"搜索方法名称或英文术语…":"Search methods or terminology…";
    $("corpus-count").textContent=state.lang==="zh"?
      db.counts.method_count+" 个独立方法节点 · 3 条真实谱系":
      db.counts.method_count+" distinct methods · 3 genuine lineages";
  }
  function workflow(){
    const root=$("stages");root.replaceChildren();
    db.workflow.forEach(id=>{
      const n=node(id),selected=state.stage===id;
      const b=btn("stage"+(selected?" active":state.stage?" inactive":""),"",()=>{
        state.stage=selected?null:id;render();
      });
      b.style.setProperty("--stage",n.color);
      b.style.setProperty("--stage-bg",n.color+"18");
      b.setAttribute("aria-pressed",String(selected));
      b.title=n.summary[state.lang];
      b.append(elem("span","stage-number",String(n.order).padStart(2,"0")));
      b.append(elem("div","stage-title",stageName[id][state.lang==="zh"?0:1]));
      b.append(elem("span","stage-arrow","↗"));root.append(b);
    });
    $("stage-clear").disabled=!state.stage;
    $("stage-clear").style.opacity=state.stage?"1":".5";
  }
  function tabs(){
    const root=$("tracks");root.replaceChildren();
    db.tracks.forEach(tr=>{
      const b=btn("tab"+(tr.id===state.track?" active":""),tr.title[state.lang],()=>{
        state.track=tr.id;state.family=null;state.query="";state.chosen=null;$("search").value="";
        render();requestAnimationFrame(fit);
      });
      b.setAttribute("role","tab");
      b.setAttribute("aria-selected",String(tr.id===state.track));root.append(b);
    });
    $("track-description").textContent=track().description[state.lang];
  }
  function roleLinks(){
    const allowed=new Set([...track().family_ids,...track().method_ids]);
    return db.edges.filter(e=>e.type==="uses_method"&&allowed.has(e.target)&&(!state.stage||e.source===state.stage));
  }
  function roles(){
    const root=$("role-summary");root.replaceChildren(elem("span","role-lead",phrase("roles")+":"));
    const items=roleLinks();
    items.slice(0,6).forEach(e=>{
      const b=btn("role-card","",()=>select("edge",e.id));
      b.style.setProperty("--role-color",node(e.source)?.color||"#64748b");
      b.title=e.role[state.lang]||e.label[state.lang];
      b.append(elem("span","role-arrow","↗"));
      b.append(elem("span","",stageName[e.source][state.lang==="zh"?0:1]+" → "+name(e.target)));
      root.append(b);
    });
    if(items.length>6)root.append(elem("span","role-more","+"+(items.length-6)+" "+phrase("more")));
    if(!items.length)root.append(elem("span","role-more",phrase("noRoles")));
  }
  function families(){
    const root=$("family-filters");root.replaceChildren();
    track().family_ids.forEach(id=>{
      const b=btn("family-button"+(state.family===id?" active":""),name(id),()=>{
        state.family=state.family===id?null:id;draw();
      });
      b.setAttribute("aria-pressed",String(state.family===id));root.append(b);
    });
  }
  const graphTypes=new Set(["extends","combines","specializes"]);
  function familyMember(id){
    return !state.family || db.edges.some(e=>e.type==="member_of_family"&&e.source===id&&e.target===state.family);
  }
  function fadedNode(id){
    const n=node(id),q=state.query.toLowerCase().trim();
    if(!familyMember(id))return true;
    return !!q && !(n.label.zh+" "+n.label.en+" "+n.summary.zh+" "+n.summary.en).toLowerCase().includes(q);
  }
  function fadedEdge(e){
    return (state.stage && !e.stage_ids.includes(state.stage)) ||
      (fadedNode(e.source)&&fadedNode(e.target));
  }
  function methodEdges(ids){
    return db.edges.filter(e=>graphTypes.has(e.type)&&ids.has(e.source)&&ids.has(e.target)&&
      (state.taxonomy||e.type!=="specializes"));
  }
  function layoutMethods(ids,rels){
    const idList=[...ids], neighbors=new Map(idList.map(id=>[id,new Set()]));
    rels.forEach(e=>{
      neighbors.get(e.source).add(e.target);
      neighbors.get(e.target).add(e.source);
    });
    const visited=new Set(), comps=[];
    idList.forEach(id=>{
      if(visited.has(id))return;
      const q=[id],members=[];visited.add(id);
      while(q.length){
        const current=q.shift();members.push(current);
        neighbors.get(current).forEach(n=>{if(!visited.has(n)){visited.add(n);q.push(n);}});
      }
      comps.push(members);
    });
    comps.sort((a,b)=>b.length-a.length || name(a[0]).localeCompare(name(b[0])));
    const positions={};let yBase=45,maxDepth=0;
    comps.forEach(comp=>{
      const set=new Set(comp), depth=new Map(comp.map(id=>[id,0]));
      for(let step=0;step<comp.length;step++){
        let changed=false;
        rels.forEach(e=>{
          if(set.has(e.source)&&set.has(e.target)){
            const proposed=depth.get(e.source)+1;
            if(proposed>depth.get(e.target)){depth.set(e.target,proposed);changed=true;}
          }
        });
        if(!changed)break;
      }
      const columns=new Map();
      comp.forEach(id=>{
        const d=depth.get(id);maxDepth=Math.max(d,maxDepth);
        if(!columns.has(d))columns.set(d,[]);
        columns.get(d).push(id);
      });
      const height=Math.max(...[...columns.values()].map(a=>a.length))*110;
      columns.forEach((idsInColumn,d)=>{
        idsInColumn.sort((a,b)=>name(a).localeCompare(name(b)));
        const offset=(height-idsInColumn.length*110)/2;
        idsInColumn.forEach((id,index)=>{positions[id]={x:48+d*272,y:yBase+offset+index*110};});
      });
      yBase+=height+48;
    });
    return {positions,width:Math.max(525,272*(maxDepth+1)+100),height:yBase+15};
  }
  function svgElem(name){return document.createElementNS("http://www.w3.org/2000/svg",name);}
  function transform(){
    $("diagram").style.transform="translate("+state.panX+"px,"+state.panY+"px) scale("+state.scale+")";
  }
  function draw(){
    const ids=new Set(track().method_ids),rels=methodEdges(ids);
    layout=layoutMethods(ids,rels);
    const container=$("diagram");container.style.width=layout.width+"px";container.style.height=layout.height+"px";
    const svg=$("lines"), nodeLayer=$("graph-nodes"),edgeLayer=$("graph-edge-labels");
    svg.setAttribute("width",String(layout.width));svg.setAttribute("height",String(layout.height));
    svg.setAttribute("viewBox","0 0 "+layout.width+" "+layout.height);
    svg.replaceChildren();nodeLayer.replaceChildren();edgeLayer.replaceChildren();
    const defs=svgElem("defs");svg.append(defs);
    rels.forEach(e=>{
      const start=layout.positions[e.source],end=layout.positions[e.target];if(!start||!end)return;
      const color=e.type==="specializes"?"#a6b4c3":e.color;
      const x1=start.x+188,y1=start.y+39,x2=end.x,y2=end.y+39;
      const gap=Math.max(26,(x2-x1)*.44);
      const path=svgElem("path");
      path.setAttribute("d","M "+x1+" "+y1+" C "+(x1+gap)+" "+y1+" "+(x2-gap)+" "+y2+" "+x2+" "+y2);
      path.setAttribute("stroke",color);
      const markId="arrow-"+e.id.replaceAll(".","-");
      const marker=svgElem("marker");marker.setAttribute("id",markId);marker.setAttribute("viewBox","0 0 10 10");
      marker.setAttribute("refX","8");marker.setAttribute("refY","5");
      marker.setAttribute("markerWidth","5");marker.setAttribute("markerHeight","5");
      marker.setAttribute("orient","auto");
      const arrow=svgElem("path");arrow.setAttribute("d","M 0 0 L 10 5 L 0 10 z");
      arrow.setAttribute("fill",color);marker.append(arrow);defs.append(marker);
      path.setAttribute("marker-end","url(#"+markId+")");
      path.classList.add("graph-line");
      if(e.type==="specializes")path.classList.add("taxonomy");
      if(e.type==="combines")path.classList.add("combines");
      if(fadedEdge(e))path.classList.add("dimmed");
      svg.append(path);
      const full=e.innovation[state.lang]||e.label[state.lang];
      const abbreviated=e.type==="specializes"?txt[state.lang].type_specializes:
        (full.length>15?full.slice(0,15)+"…":full);
      const b=btn("graph-edge-btn"+(fadedEdge(e)?" dimmed":"")+
        (state.chosen?.kind==="edge"&&state.chosen.id===e.id?" selected":""),abbreviated,()=>select("edge",e.id));
      b.style.setProperty("--edge-color",color);
      b.style.left=((x1+x2)/2)+"px";
      b.style.top=((y1+y2)/2-21)+"px";
      b.title=full;
      b.setAttribute("aria-label",name(e.source)+" → "+name(e.target)+": "+full);
      edgeLayer.append(b);
    });
    ids.forEach(id=>{
      const p=layout.positions[id],n=node(id);
      const b=btn("graph-node"+(fadedNode(id)?" dimmed":"")+
        (state.chosen?.kind==="node"&&state.chosen.id===id?" selected":""),"",()=>select("node",id));
      b.style.left=p.x+"px";b.style.top=p.y+"px";
      b.title=n.label[state.lang];b.setAttribute("aria-label",n.label[state.lang]);
      b.append(elem("span","node-kind",phrase("method").toUpperCase()));
      b.append(elem("span","node-title",n.label[state.lang]));
      b.append(elem("span","node-pill"));nodeLayer.append(b);
    });
    $("graph-count").textContent=ids.size+" "+phrase("methods")+" · "+rels.length+" "+phrase("edges");
    transform();
  }
  function header(root,s){root.append(elem("div","detail-label",s));}
  function desc(root,s){if(s)root.append(elem("p","detail-text",s));}
  function details(){
    const root=$("detail-content");root.replaceChildren();
    if(!state.chosen){
      root.append(elem("div","placeholder-icon","↗"));
      root.append(elem("h3","",phrase("emptyTitle")));desc(root,phrase("emptyText"));return;
    }
    if(state.chosen.kind==="node"){
      const n=node(state.chosen.id);
      if(!n){state.chosen=null;details();return;}
      root.append(elem("span","detail-status",phrase("method")));
      root.append(elem("h3","",n.label[state.lang]));
      desc(root,n.summary[state.lang]||n.summary.en);
      if(n.core_idea){header(root,phrase("coreIdea"));desc(root,n.core_idea);}
      if(n.limitations.length){
        header(root,phrase("tradeoff"));
        n.limitations.slice(0,3).forEach(x=>desc(root,"• "+x));
      }
      const group=db.edges.filter(e=>e.type==="member_of_family"&&e.source===n.id);
      if(group.length){
        header(root,phrase("families"));
        group.forEach(e=>root.append(elem("span","detail-chip",name(e.target))));
      }
      header(root,phrase("startHere"));
      if(!n.readings.length)desc(root,phrase("noSources"));
      n.readings.forEach(r=>{
        const a=external(r.url,r.title,"source-item");
        a.append(elem("small","",r.focus));a.title=r.why;root.append(a);
      });
      const marks=n.sources.filter(s=>s.significance==="landmark");
      if(marks.length){
        header(root,phrase("landmark"));
        marks.slice(0,4).forEach(s=>{
          const a=external(s.url,s.title,"source-item");
          a.append(elem("small","",s.year+" · "+s.role+" · landmark"));root.append(a);
        });
      }
      root.append(elem("div","detail-separator"));
      root.append(external(repo+n.source_path,phrase("source"),"source-item"));
    }else{
      const e=edges[state.chosen.id];
      if(!e){state.chosen=null;details();return;}
      root.append(elem("span","detail-status",e.category==="genealogy"?phrase("innovation"):phrase("functional")));
      root.append(elem("h3","",name(e.source)+" → "+name(e.target)));
      root.append(elem("span","detail-chip",txt[state.lang]["type_"+e.type]||e.type));
      if(e.role[state.lang]){header(root,phrase("functional"));desc(root,e.role[state.lang]);}
      if(e.innovation[state.lang]){header(root,phrase("innovation"));desc(root,e.innovation[state.lang]);}
      if(e.bottleneck[state.lang]){header(root,phrase("bottleneck"));desc(root,e.bottleneck[state.lang]);}
      if(e.tradeoff){header(root,phrase("tradeoff"));desc(root,e.tradeoff);}
      if(e.stage_ids.length){
        header(root,phrase("affected"));
        e.stage_ids.forEach(s=>{
          const chip=elem("span","detail-chip",stageName[s]?.[state.lang==="zh"?0:1]||s);
          chip.style.borderLeft="3px solid "+(db.palette[s]||"#64748b");root.append(chip);
        });
      }
      if(e.evidence.length){
        header(root,phrase("evidence"));
        e.evidence.forEach(p=>root.append(external(p.url,p.title,"source-item")));
      }
    }
  }
  function select(kind,id){state.chosen={kind,id};draw();details();}
  function render(){setLanguage();workflow();tabs();roles();families();draw();details();}
  function fit(){
    if(!layout)return;
    const v=$("viewport"),s=Math.min(1.12,(v.clientWidth-34)/layout.width,(v.clientHeight-34)/layout.height);
    state.scale=Math.max(.33,s);
    state.panX=Math.round((v.clientWidth-layout.width*state.scale)/2);
    state.panY=Math.round((v.clientHeight-layout.height*state.scale)/2);
    transform();
  }
  function zoom(ratio){
    const v=$("viewport"),x=v.clientWidth/2,y=v.clientHeight/2;
    const newScale=Math.max(.33,Math.min(2.5,state.scale*ratio)),diff=newScale/state.scale;
    state.panX=x-(x-state.panX)*diff;state.panY=y-(y-state.panY)*diff;
    state.scale=newScale;transform();
  }
  function dragSetup(){
    const v=$("viewport");let start=null;
    v.addEventListener("pointerdown",event=>{
      if(event.button!==0||event.target.closest("button,a"))return;
      start={x:event.clientX,y:event.clientY,px:state.panX,py:state.panY};
      v.classList.add("dragging");v.setPointerCapture(event.pointerId);
    });
    v.addEventListener("pointermove",event=>{
      if(!start)return;
      state.panX=start.px+event.clientX-start.x;
      state.panY=start.py+event.clientY-start.y;transform();
    });
    const finish=event=>{
      start=null;v.classList.remove("dragging");
      if(v.hasPointerCapture(event.pointerId))v.releasePointerCapture(event.pointerId);
    };
    v.addEventListener("pointerup",finish);v.addEventListener("pointercancel",finish);
    v.addEventListener("wheel",event=>{
      if(!event.ctrlKey&&!event.metaKey)return;
      event.preventDefault();zoom(event.deltaY<0?1.10:.90);
    },{passive:false});
  }
  async function init(){
    try{
      const result=await fetch("./data/preview.json",{cache:"no-store"});
      if(!result.ok)throw Error("Data HTTP "+result.status);
      db=await result.json();
      nodes=Object.fromEntries(db.nodes.map(n=>[n.id,n]));
      edges=Object.fromEntries(db.edges.map(e=>[e.id,e]));
      if(Object.keys(nodes).length!==db.nodes.length)throw Error("Duplicate nodes");
      state.lang=new URLSearchParams(location.search).get("lang")==="en"?"en":"zh";
      $("lang-toggle").addEventListener("click",()=>{
        state.lang=state.lang==="zh"?"en":"zh";render();requestAnimationFrame(fit);
      });
      $("stage-clear").addEventListener("click",()=>{state.stage=null;render();});
      $("show-taxonomy").addEventListener("change",event=>{
        state.taxonomy=event.target.checked;draw();requestAnimationFrame(fit);
      });
      $("search").addEventListener("input",event=>{state.query=event.target.value;draw();});
      $("zoom-in").addEventListener("click",()=>zoom(1.18));
      $("zoom-out").addEventListener("click",()=>zoom(.85));
      $("fit-view").addEventListener("click",fit);
      document.addEventListener("keydown",event=>{
        if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==="k"){
          event.preventDefault();$("search").focus();
        }else if(event.key==="Escape"&&state.chosen){
          state.chosen=null;draw();details();
        }
      });
      dragSetup();render();requestAnimationFrame(fit);
    }catch(error){
      console.error(error);
      $("detail-content").replaceChildren(elem("p","",txt.zh.error));
    }
  }
  init();
})();
