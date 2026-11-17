"use strict";
(() => {
  const $=id=>document.getElementById(id);
  const WORDS={
    zh:{
      brand:"物理 AI 方法知识图谱",repo:"GitHub 仓库",title:"理解问题，也理解方法为什么演进。",
      subtitle:"三阶段研究主轴 × 一张有证据的方法演化 DAG。节点颜色区分方法范式；演进边的颜色表示它针对的研究阶段。",
      axisTitle:"研究主轴",clearPhase:"取消筛选",
      axisNote:"选择研究阶段，高亮相关方法和这类研究问题推动的演进边。",
      concerns:"贯穿要求：物理一致性 · 可辨识性 · 误差 · 不确定性 · 外部验证",
      mappingTitle:"研究环节如何使用方法？",moreMapping:"展开全部映射",lessMapping:"收起映射",
      mappingNote:"家族级关联是研究线索，并非该家族每一个方法都已经过独立验证。",
      dagTitle:"方法演化 DAG",fitAll:"纵览全图",readingZoom:"阅读比例",
      fullscreen:"全屏查看",exitFullscreen:"退出全屏",taxonomy:"显示分类线",comparisons:"显示对照线",
      lineageFocus:"聚焦前驱与后继",exitLineage:"退出路径聚焦",resetFocus:"清除聚焦",
      graphHint:"节点＝方法范式色 · 演进边＝研究阶段色",
      canvasHint:"拖动平移 · 滚轮缩放 · 点击节点或有向边",
      legendExtends:"方法扩展",legendCombines:"技术融合",
      legendTaxonomy:"灰点线：分类",legendMuted:"淡化：非当前关注",
      miniTitle:"全图导航",showMini:"显示小地图",
      unlinkedTitle:"暂无已记录演化关系的方法",
      unlinkedNote:"此处仅表示尚未收录方法扩展／融合的证据；它们可能仍有分类关系或代表性论文，不应被删除或随意添加演进连线。",
      drawerTitle:"方法与证据",pin:"固定",unpin:"取消固定",
      prototype:"v0.8 为方法演化布局与导航的可交互原型。",
      prototypeDesc:"所有学术事实来自现有权威数据，未编造连接；正式部署和文献完善仍将继续。",
      phaseSelected:"研究阶段",choosePhase:"点击上方任一研究阶段",allMethods:"当前收录方法",
      lineageMethods:"已记录演化关系",unlinkedMethods:"待完善谱系",methods:"方法",links:"关系",components:"演化分支",
      directRole:"直接方法用途",familyRole:"家族级用途",phaseTag:"研究阶段",
      noPhase:"全局视图",noMapping:"选择阶段以查看功能映射",
      core:"核心思想",limits:"局限与代价",families:"方法家族（可以多重归属）",
      reading:"建议优先阅读（非强制）",landmark:"里程碑及相关论文",innovation:"技术变化",
      bottleneck:"针对的技术瓶颈",tradeoff:"适用边界与代价",evidence:"支持论文",source:"打开权威数据记录",
      selectedNode:"方法节点",selectedEdge:"方法关系",selectedRole:"功能映射",
      selectTitle:"点击节点或演进边查看详细解释",selectText:"节点展示方法学背景和文献；有向边展示子方法相对前驱究竟改变了什么。默认画布仅展示有已记录演进证据的分支。",
      noEvidence:"暂无已登记的相关文献",direct:"直接",family:"家族级",ancestor:"上层家族",
      unlinkedStatus:"暂无已记录的扩展／融合关系；此状态不等于该方法缺乏文献或独立创新。",
      familyCaution:"家族级功能关系仅构成研究线索，不是逐方法独立验证。",
      scope_conceptual:"概念适用",scope_literature_supported:"文献支持",
      scope_application_verified:"特定应用已验证",scope_hypothesis:"研究设想",
      memberCount:"个方法",missing:"未找到相关方法",allCategories:"全部范式",
      searchPlaceholder:"搜索方法、中英文术语…",matchedCore:"演化图",matchedShelf:"谱系待完善",
      earlier:"前驱方法",later:"后继方法",stageNoEvidence:"未标记某阶段不等于该方法绝对不适用",
      roleInfo:"研究环节的功能映射不同于方法历史继承",
      related:"相关方法",noChildren:"暂无已记录的后续扩展"
    },
    en:{
      brand:"Physics AI Method Knowledge Atlas",repo:"GitHub repository",title:"Understand the problem—and why methods evolve.",
      subtitle:"Three research phases × one evidence-backed method DAG. Node colors encode paradigms; evolution-edge colors encode research targets.",
      axisTitle:"Research workflow",clearPhase:"Clear filter",
      axisNote:"Select a research phase to highlight relevant methods and innovations motivated by that phase.",
      concerns:"Cross-cutting: physical validity · identifiability · error · uncertainty · external validation",
      mappingTitle:"How does this phase use methods?",moreMapping:"Show all roles",lessMapping:"Show fewer",
      mappingNote:"Family-level applicability is a research lead, not independent validation of all family members.",
      dagTitle:"Method evolution DAG",fitAll:"Fit entire graph",readingZoom:"Reading scale",
      fullscreen:"Fullscreen",exitFullscreen:"Exit fullscreen",taxonomy:"Show taxonomy links",comparisons:"Show comparisons",
      lineageFocus:"Focus predecessors & successors",exitLineage:"Exit path focus",resetFocus:"Reset focus",
      graphHint:"Node = methodological paradigm · edge = research-phase motivation",
      canvasHint:"Drag to pan · scroll to zoom · select method or directed edge",
      legendExtends:"Method extension",legendCombines:"Method fusion",
      legendTaxonomy:"Dotted grey: taxonomy",legendMuted:"Faded: outside focus",
      miniTitle:"Graph minimap",showMini:"Show minimap",
      unlinkedTitle:"Methods without a recorded evolution link",
      unlinkedNote:"This only means there is no registered extends/combines evidence yet. These methods may still have taxonomy relations and important source papers.",
      drawerTitle:"Method evidence",pin:"Dock panel",unpin:"Undock panel",
      prototype:"v0.8 is an interactive evidence-first layout prototype.",
      prototypeDesc:"All scholarly facts derive from canonical records; no artificial lineage links were added.",
      phaseSelected:"Research phase",choosePhase:"Select a research phase above",
      allMethods:"Canonical methods",lineageMethods:"In evolution DAG",unlinkedMethods:"Lineage awaiting curation",
      methods:"methods",links:"links",components:"evolution branches",
      directRole:"Direct method use",familyRole:"Family-derived relevance",phaseTag:"Research phase",
      noPhase:"Global view",noMapping:"Select a phase to see functional roles",
      core:"Core mechanism",limits:"Limits and trade-offs",families:"Method families (nonexclusive)",
      reading:"Suggested reading (optional)",landmark:"Landmark and representative papers",
      innovation:"Technical improvement",bottleneck:"Target bottleneck",tradeoff:"Scope and trade-offs",
      evidence:"Supporting papers",source:"Open canonical source record",
      selectedNode:"Method node",selectedEdge:"Method relation",selectedRole:"Functional mapping",
      selectTitle:"Select a method or evolution edge",
      selectText:"Nodes show background and references; directed edges explain changes relative to predecessors. The default canvas shows documented evolution relationships.",
      noEvidence:"No linked literature at this level",direct:"Direct",family:"Family",ancestor:"Ancestor family",
      unlinkedStatus:"No extends/combines connection is currently recorded. This does not mean the method lacks scholarship.",
      familyCaution:"Family-level relevance is a research lead, not independent validation of each descendant.",
      scope_conceptual:"Conceptual",scope_literature_supported:"Literature-supported",
      scope_application_verified:"Application verified",scope_hypothesis:"Research hypothesis",
      memberCount:"methods",missing:"No matching methods",allCategories:"All paradigms",
      searchPlaceholder:"Search method names and terms…",matchedCore:"Evolution graph",matchedShelf:"Lineage uncurated",
      earlier:"Predecessors",later:"Successors",stageNoEvidence:"Unannotated does not prove a method is irrelevant",
      roleInfo:"Research-stage functionality is not a historical ancestry claim",
      related:"Related methods",noChildren:"No recorded successors"
    }
  };
  const state={lang:"zh",phase:null,paradigm:null,selected:null,pinned:false,fullscreen:false,
    mini:true,shelf:false,rolesAll:false,taxonomy:false,comparisons:false,
    pathFocus:false,search:"",component:null,zoom:1,x:0,y:0};
  let graph,nodeById,edgeById,roleById,phaseById,paradigmById,svg;
  let phaseRoles;
  const nodes=new Map(),edgeEls=new Map(),rects=new Map();
  const forward=new Map(),backward=new Map();
  let natural={w:1,h:1},miniInfo={scale:1,ox:0,oy:0};
  const repository="https://github.com/TianminWang/physics-ai-methods-atlas/blob/main/";
  const t=key=>WORDS[state.lang][key]||key;
  const tr=obj=>obj?.[state.lang]||obj?.en||"";
  const name=id=>tr(nodeById[id]?.label)||id;
  const phaseName=id=>tr(phaseById[id]?.name)||t("noPhase");
  const familyName=id=>tr(graph.families.find(f=>f.id===id)?.name)||id.split(".").pop();
  const make=(tag,cl,value)=>{
    const elem=document.createElement(tag);
    if(cl)elem.className=cl;
    if(value!==undefined&&value!==null)elem.textContent=String(value);
    return elem;
  };
  const button=(cl,value,action)=>{
    const b=make("button",cl,value);b.type="button";b.addEventListener("click",action);return b;
  };
  function sourceLink(url,title,subtitle){
    const a=make("a","source");
    if(typeof url==="string"&&/^https:\/\/[a-z0-9.-]+\//i.test(url)){
      a.href=url;a.target="_blank";a.rel="noopener noreferrer";
    }
    a.append(make("strong","",title));
    if(subtitle)a.append(make("small","",subtitle));
    return a;
  }
  function field(root,key,value){
    if(!value)return;
    root.append(make("div","section-label",t(key)));
    root.append(make("p","",value));
  }
  function chip(root,title,color){
    const item=make("span","chip",title);
    if(color)item.style.borderLeft="3px solid "+color;
    root.append(item);
  }
  function grade(id){
    if(!state.phase)return "all";
    const roles=phaseRoles[state.phase]?.[id]||[];
    if(roles.some(r=>r.level==="direct"))return "direct";
    if(roles.some(r=>r.level==="family"))return "family";
    if(roles.some(r=>r.level==="ancestor_family"))return "ancestor";
    return "none";
  }
  const degree=id=>({direct:4,family:3,ancestor:2,all:3,none:0}[grade(id)]||0);
  function lineageSet(startIds){
    const seen=new Set(startIds),queue=[...startIds];
    while(queue.length){
      const id=queue.shift();
      const neighbors=new Set([...(forward.get(id)||[]),...(backward.get(id)||[])]);
      for(const neighbor of neighbors){
        if(!seen.has(neighbor)){seen.add(neighbor);queue.push(neighbor);}
      }
    }
    return seen;
  }
  function neighbors(ids){
    const result=new Set();
    if(!ids)return result;
    for(const id of ids){
      for(const next of forward.get(id)||[])result.add(next);
      for(const prev of backward.get(id)||[])result.add(prev);
    }
    return result;
  }
  function selectedIds(){
    const selected=state.selected;
    if(!selected)return null;
    if(selected.kind==="node")return new Set([selected.id]);
    if(selected.kind==="edge"){
      const e=edgeById[selected.id];return e?new Set([e.source,e.target]):null;
    }
    if(selected.kind==="role"){
      const r=roleById[selected.id];
      if(!r||!state.phase)return null;
      return new Set(Object.entries(phaseRoles[state.phase]||{})
        .filter(([_,list])=>list.some(item=>item.relation_id===r.id))
        .map(([id])=>id));
    }
    return null;
  }
  function translate(){
    document.documentElement.lang=state.lang==="zh"?"zh-CN":"en";
    document.querySelectorAll("[data-i18n]").forEach(e=>e.textContent=t(e.dataset.i18n));
    $("language").textContent=state.lang==="zh"?"EN":"中文";
    $("search").placeholder=t("searchPlaceholder");
    $("total-count").textContent=graph.summary.methods+" "+t("methods")+
      " · "+graph.summary.evolution_components+" "+t("components")+
      " · "+graph.summary.unlinked_methods+" "+t("unlinkedMethods");
    $("fullscreen").textContent=state.fullscreen?t("exitFullscreen"):t("fullscreen");
    $("pin-drawer").textContent=state.pinned?t("unpin"):t("pin");
    $("mapping-more").textContent=state.rolesAll?t("lessMapping"):t("moreMapping");
    $("lineage-focus").textContent=state.pathFocus?t("exitLineage"):t("lineageFocus");
  }
  function renderPhases(){
    const root=$("phases");root.replaceChildren();
    for(const phase of graph.phases){
      const chosen=state.phase===phase.id;
      const b=button("phase-card"+(chosen?" active":""),"",()=>{
        state.phase=chosen?null:phase.id;
        state.component=null;state.selected=null;state.pathFocus=false;
        closeDrawer();renderUI();
        if(chosen)fitAll();else focusPhase();
      });
      b.dataset.phaseId=phase.id;
      b.style.setProperty("--phase",phase.color);
      b.style.setProperty("--phase-soft",phase.color+"13");
      b.setAttribute("aria-pressed",String(chosen));
      b.append(make("span","phase-number",phase.number+" · "+(state.lang==="zh"?"研究阶段":"RESEARCH PHASE")));
      b.append(make("strong","",tr(phase.name)));
      const steps=make("div","substeps");
      for(const sub of graph.subcapabilities.filter(s=>phase.stage_ids.includes(s.id)))
        steps.append(make("i","",tr(sub.name)));
      b.append(steps);root.append(b);
    }
    $("clear-phase").disabled=!state.phase;
  }
  function phaseMappings(){
    if(!state.phase)return [];
    const ids=new Set(phaseById[state.phase].stage_ids);
    return graph.functional.filter(r=>ids.has(r.stage)).sort((a,b)=>{
      if(a.type!==b.type)return a.type==="direct_method"?-1:1;
      return tr(a.role).localeCompare(tr(b.role));
    });
  }
  function roleMethods(rel){
    if(!state.phase)return [];
    return Object.entries(phaseRoles[state.phase]||{})
      .filter(([_,roles])=>roles.some(r=>r.relation_id===rel.id))
      .map(([id])=>id);
  }
  function renderMapping(){
    const origin=$("phase-origin"),links=$("mapping-links"),phase=phaseById[state.phase];
    origin.replaceChildren();links.replaceChildren();
    origin.style.setProperty("--phase",phase?.color||"#91A2B2");
    origin.style.setProperty("--phase-soft",phase?phase.color+"12":"#f1f5f8");
    origin.append(make("small","",t("phaseSelected")));
    origin.append(make("strong","",phase?tr(phase.name):t("choosePhase")));
    if(phase)origin.append(make("span","",tr(phase.summary)));
    const mapped=phaseMappings();
    $("mapping-more").disabled=!mapped.length;
    $("mapping-more").textContent=state.rolesAll?t("lessMapping"):t("moreMapping");
    if(!mapped.length){links.append(make("p","",t("noMapping")));return;}
    for(const rel of (state.rolesAll?mapped:mapped.slice(0,5))){
      const isFamily=rel.type==="family";
      const title=isFamily?familyName(rel.target):name(rel.target);
      const active=state.selected?.kind==="role"&&state.selected.id===rel.id;
      const b=button("mapping-card"+(isFamily?" secondary":"")+(active?" active":""),"",()=>{
        if(active)clearSelection();
        else{
          state.selected={kind:"role",id:rel.id};state.pathFocus=false;
          openDrawer();refreshHighlight();renderDrawer();
          const first=roleMethods(rel).find(mid=>nodes.has(mid));
          if(first)focusNode(first);
        }
      });
      b.dataset.roleId=rel.id;b.style.setProperty("--phase",phase.color);
      b.append(make("strong","",title));
      b.append(make("span","role",tr(rel.role)));
      const sub=graph.subcapabilities.find(s=>s.id===rel.stage);
      b.append(make("span","meta",(isFamily?t("familyRole"):t("directRole"))+
        " · "+(sub?tr(sub.name):"")+" · "+t("scope_"+rel.scope)));
      b.title=tr(rel.role);links.append(b);
    }
  }
  function renderParadigms(){
    const root=$("paradigm-filters");root.replaceChildren();
    root.append(button("paradigm-pill"+(!state.paradigm?" active":""),t("allCategories"),()=>{
      state.paradigm=null;renderParadigms();refreshHighlight();
    }));
    for(const paradigm of graph.paradigms){
      const b=button("paradigm-pill"+(state.paradigm===paradigm.id?" active":""),"",()=>{
        state.paradigm=state.paradigm===paradigm.id?null:paradigm.id;
        renderParadigms();refreshHighlight();
      });
      b.style.setProperty("--color",paradigm.color);b.style.setProperty("--fill",paradigm.fill);
      b.dataset.paradigmId=paradigm.id;
      b.append(make("i","dot"));b.append(make("span","",tr(paradigm.label)));
      root.append(b);
    }
  }
  function refreshHighlight(){
    const selected=selectedIds();
    const path=state.pathFocus&&selected?lineageSet(selected):selected;
    const context=neighbors(selected);
    const comp=graph.components.find(c=>c.id===state.component);
    const compSet=comp?new Set(comp.method_ids):null;
    const relevant=state.phase?new Set(Object.keys(phaseRoles[state.phase]||{})
      .filter(id=>degree(id)>=2)):null;
    const relevantContext=neighbors(relevant);
    const query=state.search.trim().toLowerCase();
    const match=id=>{
      const method=nodeById[id];
      return !query||(tr(method.label)+" "+method.label.en+" "+method.id+" "+tr(method.summary))
        .toLowerCase().includes(query);
    };
    for(const [id,element] of nodes){
      element.classList.remove("primary","context","dimmed","selected");
      let status="primary";
      if(!match(id)||(state.paradigm&&nodeById[id].paradigm!==state.paradigm))status="dimmed";
      else if(selected){
        status=selected.has(id)?"selected":path?.has(id)?"primary":
          context.has(id)?"context":"dimmed";
      }else if(compSet){
        status=compSet.has(id)?"primary":"dimmed";
      }else if(state.phase){
        status=degree(id)>=3?"primary":
          degree(id)>=2||relevantContext.has(id)?"context":"dimmed";
      }
      element.classList.add(status);
    }
    for(const [id,element] of edgeEls){
      const edge=edgeById[id];
      element.classList.remove("primary","context","dimmed","selected","hidden-edge");
      if(edge.type==="specializes"&&!state.taxonomy ||
         edge.type==="contrasts_with"&&!state.comparisons){
        element.classList.add("hidden-edge");continue;
      }
      let status="primary";
      if(query&&!match(edge.source)&&!match(edge.target) ||
         state.paradigm&&nodeById[edge.source].paradigm!==state.paradigm&&
         nodeById[edge.target].paradigm!==state.paradigm)status="dimmed";
      else if(selected){
        status=state.selected?.kind==="edge"&&state.selected.id===id?"selected":
          path?.has(edge.source)&&path?.has(edge.target)?"primary":
          selected.has(edge.source)||selected.has(edge.target)?"context":"dimmed";
      }else if(compSet){
        status=compSet.has(edge.source)&&compSet.has(edge.target)?"primary":"dimmed";
      }else if(state.phase){
        status=edge.phase_ids.includes(state.phase)?"primary":
          degree(edge.source)>=3&&degree(edge.target)>=3?"context":"dimmed";
      }
      element.classList.add(status);
    }
    $("lineage-focus").disabled=!(state.selected?.kind==="node"||state.selected?.kind==="edge");
    $("lineage-focus").textContent=state.pathFocus?t("exitLineage"):t("lineageFocus");
    $("graph-subtitle").textContent=
      (state.phase?tr(phaseById[state.phase].name):t("noPhase"))+
      " · "+graph.summary.core_methods+" / "+graph.summary.methods+" "+t("lineageMethods");
    $("graph-status").textContent=
      graph.summary.core_methods+" "+t("lineageMethods")+" · "+
      graph.summary.evolution_components+" "+t("components")+" · "+
      graph.summary.unlinked_methods+" "+t("unlinkedMethods");
    drawMinimap();
  }
  // APPEND_V08
