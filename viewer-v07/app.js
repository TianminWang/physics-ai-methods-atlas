"use strict";
(() => {
  const $=id=>document.getElementById(id);
  const L={
    zh:{
      brand:"科学计算与物理 AI 方法谱系",repo:"GitHub 仓库",
      title:"从正问题，到反问题，再到数字孪生。",
      subtitle:"三阶段研究主轴解释“要解决什么”，统一方法 DAG 展示“方法如何演变”。节点颜色代表技术范式，有色演进边代表它主要针对的研究阶段。",
      axisTitle:"研究主轴",clearStage:"取消阶段筛选",
      axisNote:"物理模型与观测是反问题基础；个体化模型可继续预测和干预，并由新数据反馈更新。",
      concerns:"横向要求：物理一致性 · 可辨识性 · 数值误差 · 不确定性 · 外部验证",
      mappingTitle:"阶段如何使用这些方法？",moreMappings:"查看全部映射",fewerMappings:"收起映射",
      mappingNote:"功能映射可能指向一个方法家族，不能因此宣称家族的所有方法都已单独验证；点击卡片查看具体作用与证据。",
      dagTitle:"统一方法演化图",fitAll:"查看全图",readingZoom:"阅读比例",
      taxonomy:"显示分类关系",comparisons:"显示对照关系",clearFocus:"清除局部聚焦",
      canvasTip:"拖动画布平移；点击节点或有向边查看详情",
      graphNote:"位置由真实方法关系计算 · 灰虚线为分类，不代表历史改进",
      legendExtends:"扩展／演进",legendCombines:"技术融合",legendTaxonomy:"分类联系",legendMuted:"当前未聚焦",
      dagNote:"允许多个不连通的 DAG 分量；不会为连通画面编造方法继承边。阅读方法的论文、背景和限制请点击节点或连线。",
      details:"方法与证据",prototype:"v0.7 为真实数据驱动的布局验证版本。",
      prototypeDesc:"保留全部原始论文、专著、方法与关系，未将三个阶段理解成互斥的方法分类。",
      selected:"当前阶段",noPhase:"未筛选阶段",directRole:"方法级直接映射",familyRole:"方法家族级映射",
      familyCaution:"家族级关联是研究线索，不能代替单个方法的实证验证。",
      direct:"直接关联",family:"家族级",ancestor:"上层家族",none:"暂无映射",
      core:"核心机制",limits:"局限与代价",reading:"建议优先阅读（非强制）",
      landmark:"里程碑与代表性论文",memberships:"方法家族（可多重归属）",
      workflowUses:"方法与研究阶段的关系",innovation:"方法改变了什么",bottleneck:"解决的技术瓶颈",
      tradeoff:"改进代价与限制",relatedPhases:"相关研究阶段",evidence:"支持论文",
      source:"打开权威数据记录",method:"具体方法",edge:"方法关系",role:"功能映射",
      selectTitle:"点击方法节点或有向边",selectDesc:"方法节点显示技术范式与代表性论文；演化边显示技术变化、瓶颈及证据。点击研究阶段可以在同一张图上聚焦。",
      extends:"方法扩展",combines:"技术融合",specializes:"分类特殊化",contrasts_with:"方法对照",
      scope_conceptual:"概念适用",scope_literature_supported:"文献支持",scope_application_verified:"特定应用验证",scope_hypothesis:"研究设想",
      mappingCount:"项方法功能",methods:"方法",links:"方法关系",allParadigms:"全部范式",
      searchPlaceholder:"搜索方法或英文名称…",unrelated:"无标注不代表绝对无关"
    },
    en:{
      brand:"Scientific computing and Physics AI methods",repo:"GitHub repository",
      title:"From forward models to inverse problems and digital twins.",
      subtitle:"Three phases describe the research questions; one method DAG explains scholarly evolution. Node colors encode paradigms, edge colors denote the scientific phase an innovation targets.",
      axisTitle:"Research axis",clearStage:"Clear phase",
      axisNote:"Physical and measurement models support inversion; personalized models support prediction, intervention and updating.",
      concerns:"Cross-cutting: physical validity · identifiability · numerical error · uncertainty · external validation",
      mappingTitle:"How does this phase use methods?",moreMappings:"Show all mappings",fewerMappings:"Show fewer",
      mappingNote:"Family-wide applicability is a research lead, not separate validation of every method. Click a mapping to inspect its exact role and evidence.",
      dagTitle:"Global method genealogy DAG",fitAll:"Fit all",readingZoom:"Reading zoom",
      taxonomy:"Show taxonomy links",comparisons:"Show comparisons",clearFocus:"Clear local focus",
      canvasTip:"Drag to pan; select method nodes or directed edges",
      graphNote:"Ranks from documented relationships · gray dotted links are taxonomy, not historical improvement",
      legendExtends:"Method extension",legendCombines:"Method fusion",legendTaxonomy:"Taxonomy",legendMuted:"Outside focus",
      dagNote:"Disconnected DAG components are valid. No artificial genealogy edges are added for visual connectivity. Click nodes or edges to inspect source literature.",
      details:"Methods and evidence",prototype:"v0.7 is a real-data layout prototype.",
      prototypeDesc:"All scholarly methods, sources and relations remain canonical. Phases are not exclusive classifications.",
      selected:"Selected phase",noPhase:"No phase filter",directRole:"Direct method role",familyRole:"Method-family role",
      familyCaution:"Family-level applicability is a lead, not independently verified for every descendant method.",
      direct:"Direct",family:"Family-derived",ancestor:"Ancestor-family",none:"No mapping",
      core:"Central mechanism",limits:"Limitations",reading:"Suggested starting reading (optional)",
      landmark:"Landmarks and related papers",memberships:"Method families (nonexclusive)",
      workflowUses:"Connections to research phases",innovation:"What changed",bottleneck:"Target bottleneck",
      tradeoff:"Trade-offs",relatedPhases:"Relevant research phases",evidence:"Supporting papers",
      source:"Open canonical source record",method:"Method",edge:"Method relation",role:"Functional mapping",
      selectTitle:"Select a method or directed edge",selectDesc:"Method nodes show paradigms and literature; evolution edges explain improvements, bottlenecks and supporting evidence.",
      extends:"Extension",combines:"Combination",specializes:"Specialization",contrasts_with:"Comparison",
      scope_conceptual:"Conceptual applicability",scope_literature_supported:"Literature supported",scope_application_verified:"Verified application",scope_hypothesis:"Research hypothesis",
      mappingCount:"functional links",methods:"methods",links:"method links",allParadigms:"All paradigms",
      searchPlaceholder:"Search method names…",unrelated:"Unannotated does not mean irrelevant"
    }
  };
  const st={lang:"zh",phase:"inference",selected:null,paradigm:null,search:"",showAll:false,taxonomy:true,contrasts:false,zoom:1,x:0,y:0};
  let graph,nodes,edges,roles,phases,paradigms,svg;
  const ng=new Map(),eg=new Map(),neighbor=new Map(),sizes={};
  const repo="https://github.com/TianminWang/physics-ai-methods-atlas/blob/main/";
  const t=key=>L[st.lang][key]||key;
  const tr=obj=>obj?.[st.lang]||obj?.en||"";
  const el=(tag,cls,txt)=>{const v=document.createElement(tag);if(cls)v.className=cls;if(txt!==undefined)v.textContent=String(txt);return v;};
  const btn=(cls,title,cb)=>{const b=el("button",cls,title);b.type="button";b.addEventListener("click",cb);return b;};
  function source(url,title,detail){
    const a=el("a","source");
    if(typeof url==="string"&&/^https:\/\/[a-z0-9.-]+\//i.test(url)){a.href=url;a.target="_blank";a.rel="noopener noreferrer";}
    a.append(el("strong","",title));if(detail)a.append(el("small","",detail));return a;
  }
  const pName=id=>tr(phases[id]?.name)||id;
  const fName=id=>tr(graph.families.find(f=>f.id===id)?.name)||id;
  const subName=id=>tr(graph.subcapabilities.find(s=>s.id===id)?.name)||id;
  function selectRoles(id,phase){
    return graph.phase_roles[phase]?.[id]||[];
  }
  function rating(id){
    if(!st.phase)return 4;
    const r=selectRoles(id,st.phase);
    if(r.some(x=>x.level==="direct"))return 4;
    if(r.some(x=>x.level==="family"))return 3;
    if(r.some(x=>x.level==="ancestor_family"))return 2;
    return 0;
  }
  function selectSet(){
    const s=st.selected;if(!s)return null;
    if(s.type==="node")return new Set([s.id]);
    if(s.type==="edge"){const e=edges[s.id];return e?new Set([e.source,e.target]):new Set();}
    if(s.type==="role"){
      return new Set(Object.entries(graph.phase_roles[st.phase]||{}).filter(([_,rs])=>rs.some(r=>r.relation_id===s.id)).map(([id])=>id));
    }
    return null;
  }
  function adjacent(set){
    const out=new Set();if(set)for(const id of set)for(const n of neighbor.get(id)||[])out.add(n);return out;
  }
  function highlight(){
    const chosen=selectSet(),chosenNeighbors=adjacent(chosen);
    const phaseMembers=new Set(st.phase?Object.keys(graph.phase_roles[st.phase]||{}).filter(id=>rating(id)>=2):[]);
    const parentContext=adjacent(phaseMembers);
    const q=st.search.trim().toLowerCase();
    const matches=id=>{
      const n=nodes[id];
      return !q||(tr(n.label)+" "+n.label.en+" "+n.id).toLowerCase().includes(q);
    };
    for(const [id,g] of ng){
      g.classList.remove("dimmed","context","primary","selected");
      let c="primary";
      if(!matches(id)||st.paradigm&&nodes[id].paradigm!==st.paradigm)c="dimmed";
      else if(chosen)c=chosen.has(id)?"selected":chosenNeighbors.has(id)?"context":"dimmed";
      else if(st.phase)c=rating(id)>=3?"primary":rating(id)>=2||parentContext.has(id)?"context":"dimmed";
      g.classList.add(c);
    }
    for(const [id,g] of eg){
      const e=edges[id];
      g.classList.remove("dimmed","context","primary","selected","hidden-edge");
      if(e.type==="specializes"&&!st.taxonomy||
        e.type==="contrasts_with"&&!st.contrasts){g.classList.add("hidden-edge");continue;}
      let c="primary";
      if(q&&!matches(e.source)&&!matches(e.target)||st.paradigm&&
        nodes[e.source].paradigm!==st.paradigm&&nodes[e.target].paradigm!==st.paradigm)c="dimmed";
      if(chosen)c=st.selected?.type==="edge"&&st.selected.id===id?"selected":
        chosen.has(e.source)&&chosen.has(e.target)?"primary":
        chosen.has(e.source)||chosen.has(e.target)?"context":"dimmed";
      else if(st.phase)c=e.phase_ids.includes(st.phase)?"primary":
        rating(e.source)>=3&&rating(e.target)>=3?"context":"dimmed";
      g.classList.add(c);
    }
    $("graph-status").textContent=(st.phase?pName(st.phase):t("allParadigms"))+" · "+
      (st.phase?phaseMembers.size+" / ":"")+graph.methods.length+" "+t("methods")+
      " · "+graph.method_edges.length+" "+t("links");
  }
  function renderPhases(){
    const root=$("phases");root.replaceChildren();
    for(const ph of graph.phases){
      const active=st.phase===ph.id;
      const b=btn("phase-card"+(active?" active":""),"",()=>{
        st.phase=active?null:ph.id;st.selected=null;st.showAll=false;
        render();focusPhase();
      });
      b.dataset.phaseId=ph.id;b.style.setProperty("--phase",ph.color);b.style.setProperty("--phase-soft",ph.color+"15");
      b.setAttribute("aria-pressed",String(active));
      b.append(el("span","phase-number",ph.number+" · "+(st.lang==="zh"?"研究阶段":"RESEARCH PHASE")));
      b.append(el("strong","",tr(ph.name)));
      const sub=el("div","substeps");
      for(const id of ph.stage_ids)sub.append(el("i","",subName(id)));
      b.append(sub);root.append(b);
    }
    $("clear-phase").disabled=!st.phase;
  }
  function phaseMappings(){
    if(!st.phase)return [];
    const ids=new Set(phases[st.phase].stage_ids);
    return graph.functional.filter(r=>ids.has(r.stage)).sort((a,b)=>{
      if(a.type!==b.type)return a.type==="direct_method"?-1:1;
      return tr(a.role).localeCompare(tr(b.role));
    });
  }
  function mappedMethods(rel){
    if(!st.phase)return [];
    return Object.entries(graph.phase_roles[st.phase]).filter(([_,rs])=>rs.some(r=>r.relation_id===rel.id)).map(([id])=>id);
  }
  function renderMappings(){
    const ph=phases[st.phase],origin=$("phase-origin"),root=$("mapping-links");
    origin.replaceChildren();root.replaceChildren();
    origin.style.setProperty("--phase",ph?.color||"#7b8c9a");
    origin.style.setProperty("--phase-soft",ph?ph.color+"12":"#f3f6f8");
    origin.append(el("small","",t("selected")));
    origin.append(el("strong","",ph?tr(ph.name):t("noPhase")));
    if(ph)origin.append(el("span","",tr(ph.summary)));
    const links=phaseMappings();
    $("mapping-more").disabled=!links.length;
    $("mapping-more").textContent=st.showAll?t("fewerMappings"):t("moreMappings");
    for(const rel of (st.showAll?links:links.slice(0,8))){
      const isFamily=rel.type==="family";
      const title=isFamily?fName(rel.target):tr(nodes[rel.target].label);
      const active=st.selected?.type==="role"&&st.selected.id===rel.id;
      const b=btn("mapping-card"+(isFamily?" secondary":"")+(active?" active":""),"",()=>{
        st.selected=active?null:{type:"role",id:rel.id};highlight();inspect();
        if(!active)focusId(mappedMethods(rel)[0]);
      });
      b.dataset.roleId=rel.id;b.style.setProperty("--phase",ph.color);
      b.append(el("strong","",title));
      const description=tr(rel.role);
      b.append(el("span","role",description.length>98?description.slice(0,98)+"…":description));
      b.append(el("span","meta",(isFamily?t("familyRole"):t("directRole"))+" · "+
        subName(rel.stage)+" · "+t("scope_"+rel.scope)));
      b.title=description;root.append(b);
    }
    if(!links.length)root.append(el("span","",t("none")));
  }
  function renderParadigms(){
    const root=$("paradigm-filters");root.replaceChildren();
    root.append(btn("paradigm-pill"+(!st.paradigm?" active":""),t("allParadigms"),()=>{
      st.paradigm=null;renderParadigms();highlight();
    }));
    for(const category of graph.paradigms){
      const b=btn("paradigm-pill"+(st.paradigm===category.id?" active":""),"",()=>{
        st.paradigm=st.paradigm===category.id?null:category.id;
        renderParadigms();highlight();
      });
      b.dataset.paradigmId=category.id;
      b.style.setProperty("--color",category.color);b.style.setProperty("--fill",category.fill);
      b.append(el("i","dot"));b.append(el("span","",tr(category.label)));
      root.append(b);
    }
  }
  function label(root,key,value){
    if(!value)return;
    root.append(el("div","section-label",t(key)));
    root.append(el("p","",value));
  }
  function chip(root,text,color){
    const c=el("span","chip",text);if(color)c.style.borderLeft="3px solid "+color;root.append(c);
  }
  function inspect(){
    const root=$("details-body");root.replaceChildren();
    const choice=st.selected;
    if(!choice){
      root.append(el("div","empty-symbol","↗"));
      root.append(el("h3","",t("selectTitle")));
      root.append(el("p","",t("selectDesc")));
      return;
    }
    if(choice.type==="node"){
      const m=nodes[choice.id],category=paradigms[m.paradigm];
      root.append(el("span","eyelabel",t("method")));
      root.append(el("h3","",tr(m.label)));
      const banner=el("div","note",tr(category.label));
      banner.style.setProperty("--line-color",category.color);banner.style.setProperty("--bg-color",category.fill);root.append(banner);
      root.append(el("p","",tr(m.summary)));
      label(root,"core",tr(m.core));
      label(root,"limits",(m.limitations[st.lang]||[]).slice(0,3).join(" · "));
      root.append(el("div","section-label",t("memberships")));
      for(const fid of m.families)chip(root,fName(fid));
      root.append(el("div","section-label",t("workflowUses")));
      let found=false;
      for(const phase of graph.phases){
        const rs=graph.phase_roles[phase.id]?.[m.id]||[];
        if(!rs.length)continue;found=true;
        const r=rs.find(x=>x.level==="direct")||rs.find(x=>x.level==="family")||rs[0];
        const card=el("div","note");
        card.style.setProperty("--line-color",phase.color);card.style.setProperty("--bg-color",phase.color+"12");
        card.append(el("strong","",tr(phase.name)+" · "+t(r.level==="direct"?"direct":r.level==="family"?"family":"ancestor")));
        card.append(el("p","",tr(r.role)));
        if(r.level!=="direct")card.append(el("small","",t("familyCaution")));
        root.append(card);
      }
      if(!found)root.append(el("p","",t("none")));
      root.append(el("div","section-label",t("reading")));
      if(!m.readings.length)root.append(el("p","",t("noEvidence")));
      for(const s of m.readings)root.append(source(s.url,s.title,s.focus));
      const landmark=m.sources.filter(s=>s.landmark);
      if(landmark.length){
        root.append(el("div","section-label",t("landmark")));
        for(const s of landmark.slice(0,6))root.append(source(s.url,s.title,s.year+" · "+s.role+" · Landmark"));
      }
      root.append(source(repo+m.source_path,t("source")));
    }else if(choice.type==="edge"){
      const e=edges[choice.id];
      root.append(el("span","eyelabel",t("edge")+" · "+t(e.type)));
      root.append(el("h3","",tr(nodes[e.source].label)+" → "+tr(nodes[e.target].label)));
      label(root,"innovation",tr(e.innovation));label(root,"bottleneck",tr(e.bottleneck));
      label(root,"tradeoff",tr(e.tradeoff));
      root.append(el("div","section-label",t("relatedPhases")));
      if(!e.phase_ids.length)root.append(el("p","",t("unrelated")));
      for(const id of e.phase_ids)chip(root,pName(id),phases[id].color);
      if(e.evidence.length){
        root.append(el("div","section-label",t("evidence")));
        for(const s of e.evidence)root.append(source(s.url,s.title));
      }
      root.append(source(repo+e.source_path,t("source")));
    }else if(choice.type==="role"){
      const r=roles[choice.id],ph=phases[st.phase];
      root.append(el("span","eyelabel",t("role")));
      root.append(el("h3","",pName(st.phase)+" → "+(r.type==="family"?fName(r.target):tr(nodes[r.target].label))));
      const box=el("div","note");box.style.setProperty("--line-color",ph.color);box.style.setProperty("--bg-color",ph.color+"12");
      box.append(el("strong","",r.type==="family"?t("familyRole"):t("directRole")));
      box.append(el("p","",tr(r.role)));root.append(box);
      label(root,"scope_"+r.scope,"");
      if(r.type==="family")root.append(el("p","",t("familyCaution")));
      root.append(el("div","section-label",t("methods")));
      const ids=mappedMethods(r);
      for(const id of ids.slice(0,14))chip(root,tr(nodes[id].label));
      if(ids.length>14)root.append(el("p","","+ "+(ids.length-14)));
      if(r.evidence.length){root.append(el("div","section-label",t("evidence")));
        for(const s of r.evidence)root.append(source(s.url,s.title));}
    }
  }
  function select(type,id){st.selected={type,id};highlight();inspect();}
  function attachSvg(){
    svg=$("atlas-dag");if(!svg)throw Error("Missing generated Graphviz SVG");
    for(const g of svg.querySelectorAll("g.atlas-node[data-method-id]")){
      const id=g.dataset.methodId;ng.set(id,g);
      g.addEventListener("click",e=>{e.stopPropagation();select("node",id);});
      g.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();select("node",id);}});
    }
    for(const g of svg.querySelectorAll("g.atlas-edge[data-edge-id]")){
      const id=g.dataset.edgeId;if(!edges[id])continue;eg.set(id,g);
      const path=g.querySelector("path");
      if(path){const hit=path.cloneNode(false);hit.classList.add("edge-hit");
        hit.setAttribute("style","fill:none;stroke:transparent;stroke-width:17");hit.setAttribute("pointer-events","stroke");g.append(hit);}
      g.addEventListener("click",e=>{e.stopPropagation();select("edge",id);});
      g.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();select("edge",id);}});
    }
    if(ng.size!==graph.methods.length)throw Error("Graphviz omitted method nodes");
    const vb=svg.viewBox.baseVal;sizes.width=svg.getBoundingClientRect().width;sizes.height=svg.getBoundingClientRect().height;
    sizes.svgWidth=vb.width;sizes.svgHeight=vb.height;
    $("board").style.width=sizes.width+"px";$("board").style.height=sizes.height+"px";
  }
  function transform(){$("board").style.transform="translate("+st.x+"px,"+st.y+"px) scale("+st.zoom+")";}
  function fitAll(){
    const v=$("viewport");
    st.zoom=Math.min((v.clientWidth-28)/sizes.width,(v.clientHeight-28)/sizes.height,1);
    st.zoom=Math.max(.1,st.zoom);
    st.x=(v.clientWidth-sizes.width*st.zoom)/2;st.y=(v.clientHeight-sizes.height*st.zoom)/2;transform();
  }
  function focusId(id){
    const g=ng.get(id);if(!g)return;
    // Graphviz nests SVG nodes under a graph-level translate/rotate group.
    // getBBox() is in that group's local coordinates and CANNOT be used as
    // root SVG pixels. Actual browser rectangles account for all transforms.
    const before=g.getBoundingClientRect(),board=$("board").getBoundingClientRect();
    const localX=(before.left+before.width/2-board.left)/st.zoom;
    const localY=(before.top+before.height/2-board.top)/st.zoom;
    const view=$("viewport");
    const targetScale=view.clientWidth<520?.88:.95;
    st.x=view.clientWidth/2-localX*targetScale;
    st.y=view.clientHeight/2-localY*targetScale;
    st.zoom=targetScale;
    transform();
  }
  function focusPhase(){
    if(st.selected?.type==="node")return focusId(st.selected.id);
    const id=st.phase==="modeling"?"method.fno":
      st.phase==="twin"?"method.dreamer-latent-imagination":"method.gauss-newton";
    focusId(id);
  }
  function zoom(factor){
    const v=$("viewport"),cx=v.clientWidth/2,cy=v.clientHeight/2;
    const next=Math.max(.11,Math.min(2.5,st.zoom*factor)),ratio=next/st.zoom;
    st.x=cx-(cx-st.x)*ratio;st.y=cy-(cy-st.y)*ratio;st.zoom=next;transform();
  }
  function pan(){
    const v=$("viewport");let drag=null;
    v.addEventListener("pointerdown",e=>{
      if(e.button!==0||e.target.closest("g[role=button],button,a"))return;
      drag={x:e.clientX,y:e.clientY,ox:st.x,oy:st.y};v.setPointerCapture(e.pointerId);
      v.classList.add("dragging");
    });
    v.addEventListener("pointermove",e=>{
      if(!drag)return;st.x=drag.ox+e.clientX-drag.x;st.y=drag.oy+e.clientY-drag.y;transform();
    });
    const stop=e=>{drag=null;v.classList.remove("dragging");
      if(v.hasPointerCapture(e.pointerId))v.releasePointerCapture(e.pointerId);};
    v.addEventListener("pointerup",stop);v.addEventListener("pointercancel",stop);
    v.addEventListener("wheel",e=>{e.preventDefault();zoom(e.deltaY<0?1.12:.89);},{passive:false});
  }
  function translate(){
    document.documentElement.lang=st.lang==="zh"?"zh-CN":"en";
    document.querySelectorAll("[data-i18n]").forEach(e=>e.textContent=t(e.dataset.i18n));
    $("language").textContent=st.lang==="zh"?"EN":"中文";
    $("search").placeholder=t("searchPlaceholder");
    $("total-count").textContent=graph.methods.length+" "+t("methods")+
      " · "+graph.summary.lineage_links+" "+t("links")+
      " · 3 "+(st.lang==="zh"?"个研究阶段":"research phases");
  }
  function render(){translate();renderPhases();renderMappings();renderParadigms();highlight();inspect();}
  function init(){
    try{
      const src=$("atlas-data");if(!src)throw Error("Missing dataset");
      graph=JSON.parse(src.textContent);
      nodes=Object.fromEntries(graph.methods.map(m=>[m.id,m]));
      edges=Object.fromEntries(graph.method_edges.map(e=>[e.id,e]));
      roles=Object.fromEntries(graph.functional.map(r=>[r.id,r]));
      phases=Object.fromEntries(graph.phases.map(p=>[p.id,p]));
      paradigms=Object.fromEntries(graph.paradigms.map(p=>[p.id,p]));
      if(Object.keys(nodes).length!==graph.methods.length)throw Error("Duplicate method IDs");
      for(const e of graph.method_edges){
        if(!neighbor.has(e.source))neighbor.set(e.source,new Set());
        if(!neighbor.has(e.target))neighbor.set(e.target,new Set());
        neighbor.get(e.source).add(e.target);neighbor.get(e.target).add(e.source);
      }
      st.lang=new URLSearchParams(location.search).get("lang")==="en"?"en":"zh";
      attachSvg();
      $("language").addEventListener("click",()=>{st.lang=st.lang==="zh"?"en":"zh";render();});
      $("clear-phase").addEventListener("click",()=>{st.phase=null;st.selected=null;render();fitAll();});
      $("mapping-more").addEventListener("click",()=>{st.showAll=!st.showAll;renderMappings();});
      $("taxonomy").addEventListener("change",e=>{st.taxonomy=e.target.checked;highlight();});
      $("contrasts").addEventListener("change",e=>{st.contrasts=e.target.checked;highlight();});
      $("search").addEventListener("input",e=>{
        // A new query replaces a previous local node/edge focus.
        st.selected=null;
        st.search=e.target.value;highlight();inspect();
        const q=st.search.trim().toLowerCase();
        if(q){const match=graph.methods.find(m=>(tr(m.label)+" "+m.label.en+" "+m.id).toLowerCase().includes(q));if(match)focusId(match.id);}
      });
      $("clear-focus").addEventListener("click",()=>{st.selected=null;st.search="";st.paradigm=null;$("search").value="";render();focusPhase();});
      $("zoom-in").addEventListener("click",()=>zoom(1.2));
      $("zoom-out").addEventListener("click",()=>zoom(.82));
      $("fit-all").addEventListener("click",fitAll);
      $("focus-map").addEventListener("click",focusPhase);
      document.addEventListener("keydown",e=>{
        if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==="k"){e.preventDefault();$("search").focus();}
        if(e.key==="Escape"){st.selected=null;render();}
      });
      pan();render();requestAnimationFrame(focusPhase);
    }catch(err){console.error(err);$("details-body").replaceChildren(el("p","",String(err)));}
  }
  init();
})();
