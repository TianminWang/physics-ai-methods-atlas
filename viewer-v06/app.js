"use strict";
(() => {
  const $=id=>document.getElementById(id);
  const lex={
    zh:{
      brandNote:"统一方法图谱 · v0.6 设计原型",repo:"GitHub 仓库",
      heading:"一条研究主轴，一张方法图谱。",
      lead:"选择一个科学研究环节，查看它如何连接不同的方法家族；方法演进边说明针对这一环节解决了什么技术瓶颈。",
      axisTitle:"研究主轴",allStages:"清除环节筛选",axisNote:"研究环节是功能链路，不是方法的分类父节点。选择环节后，下方仍保留完整方法图。",
      mapTitle:"研究环节如何调用方法？",moreRoles:"查看全部映射",fewerRoles:"收起映射",
      selectedStage:"当前研究环节",mappedMethodFamilies:"相关方法家族与直接方法",
      scopeNote:"虚线表示用途映射，不代表历史演化。家族级关联是研究线索，不等同于每个子方法都经单独验证。",
      graphTitle:"统一方法网络",fit:"适应窗口",taxonomy:"显示分类边",contrast:"显示对照边",
      expandAll:"展开全部方法",collapseAll:"恢复精简布局",panHint:"拖动平移 · 滚轮缩放 · 点击方法或关系",
      legendDirect:"直接关联",legendInherited:"家族级关联",legendMuted:"其他方法（淡化）",
      legendEvolution:"方法扩展",legendFusion:"方法融合",legendTaxonomy:"分类联系",
      visualNote:"分区只帮助定位，绝不限定方法唯一的学术归属；其余家族标签及跨区关系均被保留。",
      inspectorTitle:"关系与证据",prototypeDisclaimer:"v0.6 为全局布局验证版本。",
      prototypeMore:"全部方法来自同一份权威数据，仍需继续评估大图布局与真实阅读体验；尚未替代正式网站。",
      zoomOut:"缩小",zoomIn:"放大",more:"更多",less:"收起",
      methods:"方法",links:"关系",stageFocus:"聚焦",noFocus:"全局总览",
      directlyMapped:"直接方法",familyMapped:"家族推及",unmapped:"其他/待整理",
      mapped:"关联",of:"共",notVerified:"家族级适用性不等于每个子方法已经单独验证",
      roleDirect:"方法级功能关联",roleFamily:"方法家族的功能关联",
      noRole:"未建立这一环节的功能映射",clearRole:"取消方法家族聚焦",
      highlightRule:"亮色：直接或家族映射；浅色：仅上层家族；淡色：其他方法。演进边必须单独记录其目标研究环节。",
      emptyTitle:"点击方法、功能映射或演进边",emptyBody:"每个方法仍只有一个权威实体；右侧可以检查所属家族、它服务哪些研究环节，以及论文证据。",
      noLiterature:"暂无这一层级的文献",start:"优先阅读（非强制）",
      papers:"里程碑和其他论文",core:"核心方法",limits:"适用边界",
      memberships:"相关方法家族（可多个）",stageUsage:"与研究主轴的联系",
      evidence:"证据论文",innovation:"技术变化",bottleneck:"针对的瓶颈",
      tradeoff:"代价与局限",affected:"演进边关联环节",
      source:"打开权威记录",direct:"直接",family:"家族级",ancestor:"上层家族级",
      caution:"应用的研究线索，不是自动的逐方法实证结论",
      primary:"主要环节",other:"其他环节",role:"功能说明",
      scope_conceptual:"概念上的适用性",scope_literature_supported:"已有文献支持",
      scope_application_verified:"特定应用已验证",scope_hypothesis:"候选研究设想",
      noStage:"未选研究环节",allFamilies:"所有方法家族",zoneHint:"点选区域聚焦，展开可见其余方法",
      noStageRoles:"请从上方研究主轴选择环节，以显示指向方法家族的功能关系。",
      failed:"无法载入 v0.6 图谱数据。请运行构建脚本并打开生成的离线页面。",
      methodType:"具体方法",familyType:"方法家族",edgeType:"方法之间的关系",
      paradigmNote:"区域为非排他的视觉布局，不是学术上的单一父类。"
    },
    en:{
      brandNote:"Unified method graph · v0.6 prototype",repo:"GitHub repository",
      heading:"One research workflow. One method graph.",
      lead:"Select a research stage to see its functional links to method families. Method-evolution edges explain the technical bottlenecks they address.",
      axisTitle:"Research workflow",allStages:"Clear stage selection",axisNote:"Stages denote functional needs, not parents of methods. Selecting a stage keeps the entire map visible.",
      mapTitle:"How does a stage use methods?",moreRoles:"Show all mappings",fewerRoles:"Fewer mappings",
      selectedStage:"Selected research stage",mappedMethodFamilies:"Linked method families and direct methods",
      scopeNote:"Dashed links represent functional use, not historical descent. Family-level relevance is a research lead, not separate validation of every method.",
      graphTitle:"One unified method network",fit:"Fit view",taxonomy:"Show taxonomy edges",contrast:"Show contrast edges",
      expandAll:"Expand all methods",collapseAll:"Use compact layout",panHint:"Drag to pan · scroll to zoom · select method or link",
      legendDirect:"Direct mapping",legendInherited:"Family-based mapping",legendMuted:"Other methods (faded)",
      legendEvolution:"Method extension",legendFusion:"Method combination",legendTaxonomy:"Taxonomic relation",
      visualNote:"Zones are only navigational aids, not exclusive scholarly parents. All family membership and cross-zone edges remain preserved.",
      inspectorTitle:"Methods & evidence",prototypeDisclaimer:"v0.6 is a global layout prototype.",
      prototypeMore:"All methods derive from one canonical dataset, but full-graph readability needs further review before production deployment.",
      zoomOut:"Zoom out",zoomIn:"Zoom in",more:"More",less:"Less",
      methods:"methods",links:"links",stageFocus:"Focused on",noFocus:"Global overview",
      directlyMapped:"Direct methods",familyMapped:"Family-derived",unmapped:"Other/unmapped",
      mapped:"related",of:"of",notVerified:"Family relevance does not individually verify every descendant method",
      roleDirect:"Direct method role",roleFamily:"Method family role",
      noRole:"No functional relation recorded for this stage",clearRole:"Clear family focus",
      highlightRule:"Bright: direct/family mapping; softer: ancestor family; muted: others. Evolution links require separately recorded stage targets.",
      emptyTitle:"Choose a method, role or lineage link",emptyBody:"Methods are not duplicated. Inspect their multiple family memberships, research-stage roles and evidence here.",
      noLiterature:"No source at this level",start:"Suggested reading (optional)",
      papers:"Landmarks and related papers",core:"Core mechanism",limits:"Limits and trade-offs",
      memberships:"Method families (nonexclusive)",stageUsage:"Workflow links",
      evidence:"Evidence papers",innovation:"What changed",bottleneck:"Target technical bottleneck",
      tradeoff:"Trade-offs",affected:"Research stages linked to this innovation",
      source:"Open canonical record",direct:"Direct",family:"Family-level",ancestor:"Ancestor-family",
      caution:"Research lead, not automatic method-specific empirical validation",
      primary:"Primary stage",other:"Other stages",role:"Functional role",
      scope_conceptual:"Conceptual applicability",scope_literature_supported:"Literature supported",
      scope_application_verified:"Validated in specific application",scope_hypothesis:"Research hypothesis",
      noStage:"No stage selected",allFamilies:"All method families",zoneHint:"Select region to focus; expand for more methods",
      noStageRoles:"Select a research stage above to display its functional mapping to methods.",
      failed:"Failed to load v0.6 data. Build the source graph and open its generated offline page.",
      methodType:"Method",familyType:"Method family",edgeType:"Method relation",
      paradigmNote:"Presentation zones are nonexclusive visual groupings, never single scholarly parents."
    }
  };
  const shortStage={
    "stage.physics-forward":["正向模拟","Forward simulation"],
    "stage.observation":["观测建模","Observation model"],
    "stage.inverse-calibration":["参数与状态反演","Inverse calibration"],
    "stage.prediction-uq":["可信预测","Prediction & UQ"],
    "stage.intervention-planning":["干预决策","Intervention"],
    "stage.continual-update":["持续更新","Continual update"]
  };
  const state={
    lang:"zh",stage:"stage.inverse-calibration",role:null,selected:null,
    showAll:false,moreRoles:false,expanded:new Set(),search:"",
    taxonomy:false,contrasts:false,zoom:.86,panX:8,panY:10,
    activeZone:null
  };
  let graph,methodById,familyById,stageById,edgeById,funcById,layout,displayed=new Set();
  const repo="https://github.com/TianminWang/physics-ai-methods-atlas/blob/main/";
  const NODE_W=218,NODE_H=66,ZONE_W=485,COL_GAP=34,NODE_GAP=9;
  function t(key){return lex[state.lang][key]||key;}
  function tr(obj){return (obj&&obj[state.lang]) || (obj&&obj.en) || "";}
  function textEl(tag,cl,value){
    const x=document.createElement(tag);if(cl)x.className=cl;
    if(value!==undefined)x.textContent=String(value);return x;
  }
  function button(cl,value,onClick){
    const b=textEl("button",cl,value);b.type="button";b.addEventListener("click",onClick);return b;
  }
  function link(url,text,cl){
    const a=textEl("a",cl,text);
    if(typeof url==="string"&&/^https:\/\/[a-z0-9.-]+\//i.test(url)){
      a.href=url;a.target="_blank";a.rel="noopener noreferrer";
    }
    return a;
  }
  function name(id){
    return tr(methodById[id]?.label||familyById[id]?.name||stageById[id]?.name)||id;
  }
  function currentRoles(id){
    return graph.stage_roles[state.stage]?.[id]||[];
  }
  function bestRole(id){
    const role=currentRoles(id);
    if(!role.length)return null;
    const direct=role.find(x=>x.level==="direct");
    if(direct)return {grade:"direct",roles:role};
    const family=role.find(x=>x.level==="family");
    if(family)return {grade:"family",roles:role};
    return {grade:"ancestor",roles:role};
  }
  function matchesRole(mid){
    if(!state.role)return true;
    if(state.role.target.startsWith("method."))return mid===state.role.target;
    return methodById[mid]?.ancestor_families[state.role.target]!==undefined;
  }
  function relevance(mid){
    if(!state.stage)return 1;
    const b=bestRole(mid);
    if(!b)return 0;
    return {direct:4,family:3,ancestor:2}[b.grade];
  }
  function nodeFaded(mid){
    const m=methodById[mid];
    if(!m)return true;
    const query=state.search.trim().toLowerCase();
    if(query&&!(tr(m.label)+" "+m.label.en+" "+tr(m.summary)).toLowerCase().includes(query))return true;
    if(state.role&&!matchesRole(mid))return true;
    return !!state.stage&&relevance(mid)===0;
  }
  function familyFaded(mid){
    if(state.role&&!matchesRole(mid))return true;
    return !nodeFaded(mid)?false:true;
  }
  function edgeFaded(edge){
    if(state.role&&!matchesRole(edge.source)&&!matchesRole(edge.target))return true;
    if(state.search&&nodeFaded(edge.source)&&nodeFaded(edge.target))return true;
    if(!state.stage)return false;
    if(edge.stages.includes(state.stage))return false;
    if(relevance(edge.source)>=3&&relevance(edge.target)>=3)return false;
    return true;
  }
  function setLanguage(){
    document.documentElement.lang=state.lang==="zh"?"zh-CN":"en";
    document.querySelectorAll("[data-t]").forEach(el=>el.textContent=t(el.dataset.t));
    $("lang").textContent=state.lang==="zh"?"EN":"中文";
    $("search").placeholder=state.lang==="zh"?"搜索方法、中英文术语…":"Search methods or terminology…";
    $("meta").textContent=state.lang==="zh"?
      graph.summary.methods+" 个唯一方法 · "+graph.summary.families+" 个家族 · "+graph.summary.genealogy_edges+" 条方法联系":
      graph.summary.methods+" unique methods · "+graph.summary.families+" families · "+graph.summary.genealogy_edges+" method links";
    $("toggle-all").textContent=state.showAll?t("collapseAll"):t("expandAll");
    $("more-roles").textContent=state.moreRoles?t("fewerRoles"):t("moreRoles");
  }
  function renderAxis(){
    const root=$("stage-cards");root.replaceChildren();
    graph.stages.forEach(s=>{
      const active=state.stage===s.id;
      const b=button("stage-card"+(active?" active":""),"",()=>{
        state.stage=active?null:s.id;state.role=null;state.selected=null;
        refresh(true);
      });
      b.style.setProperty("--stage",s.color);
      b.style.setProperty("--stage-soft",s.color+"15");
      b.dataset.stageId=s.id;
      b.setAttribute("aria-pressed",String(active));
      b.title=tr(s.summary);
      b.append(textEl("div","stage-index",String(s.order).padStart(2,"0")));
      b.append(textEl("div","stage-label",shortStage[s.id][state.lang==="zh"?0:1]));
      b.append(textEl("span","corner","↗"));
      root.append(b);
    });
    $("clear-stage").disabled=!state.stage;
  }
  function rolesForStage(){
    return graph.functional.filter(r=>r.stage===state.stage)
      .sort((a,b)=>Number(a.target.startsWith("method."))-Number(b.target.startsWith("method."))
            || name(a.target).localeCompare(name(b.target)));
  }
  function mappedMethodsForRelation(rel){
    if(rel.target.startsWith("method."))return [rel.target];
    return graph.methods.filter(m=>m.ancestor_families[rel.target]!==undefined).map(m=>m.id);
  }
  function renderBridge(){
    const root=$("role-cards");root.replaceChildren();
    const stage=stageById[state.stage];
    $("bridge-source").style.setProperty("--focus",stage?.color||"#7c8898");
    $("bridge-source").style.setProperty("--focus-soft",stage?stage.color+"12":"#f4f7fa");
    $("source-stage-name").textContent=stage?shortStage[stage.id][state.lang==="zh"?0:1]:t("noStage");
    const direct=Object.values(graph.stage_roles[state.stage]||{}).filter(roles=>roles.some(r=>r.level==="direct")).length;
    const total=Object.keys(graph.stage_roles[state.stage]||{}).length;
    $("source-stage-count").textContent=state.stage?
      direct+" "+t("directlyMapped")+" · "+(total-direct)+" "+t("familyMapped"):t("noStageRoles");
    $("bridge-arrow").style.setProperty("--focus",stage?.color||"#7c8898");
    const links=rolesForStage();
    $("more-roles").disabled=!links.length;
    const limit=state.moreRoles?links.length:Math.min(6,links.length);
    links.slice(0,limit).forEach(rel=>{
      const selected=state.role?.id===rel.id;
      const b=button("role-card"+(selected?" active":"")+(rel.type==="family"?" supplement":""),"",()=>{
        state.role=selected?null:rel;state.selected=selected?null:{kind:"role",id:rel.id};
        refresh(true);
      });
      b.style.setProperty("--focus",stage.color);
      b.dataset.roleId=rel.id;
      b.append(textEl("strong","",name(rel.target)));
      const meaning=tr(rel.role);b.append(textEl("span","",meaning.length>82?meaning.slice(0,82)+"…":meaning));
      const scope=rel.type==="family"?t("roleFamily"):t("roleDirect");
      b.append(textEl("em","",scope+" · "+mappedMethodsForRelation(rel).length+" "+t("methods")));
      b.title=meaning;
      b.setAttribute("aria-pressed",String(selected));root.append(b);
    });
    if(!links.length)root.append(textEl("div","role-card",t("noStageRoles")));
    $("more-roles").textContent=state.moreRoles?t("fewerRoles"):t("moreRoles");
  }
  function renderZoneNav(){
    const root=$("zone-nav");root.replaceChildren();
    graph.zones.forEach(z=>{
      const hits=z.method_ids.filter(id=>relevance(id)>0).length;
      const caption=tr(z.label)+" · "+(state.stage?hits+" / ":"")+z.method_ids.length;
      const b=button("zone-chip"+(state.activeZone===z.id?" active":""),caption,()=>{
        state.activeZone=z.id;const box=layout?.zoneBoxes[z.id];
        if(box){state.zoom=.9;state.panX=Math.max(8,($("viewport").clientWidth-ZONE_W*.9)/2)-box.x*.9;
          state.panY=22-box.y*.9;applyTransform();}
        renderZoneNav();
      });root.append(b);
    });
  }
  function visibleForZone(zone){
    const mids=zone.method_ids;
    if(state.showAll||state.expanded.has(zone.id))return mids;
    const matchQuery=state.search.trim();
    const degrees={};
    graph.method_edges.forEach(e=>{
      degrees[e.source]=(degrees[e.source]||0)+1;
      degrees[e.target]=(degrees[e.target]||0)+1;
    });
    const sorted=[...mids].sort((a,b)=>{
      const r=relevance(b)-relevance(a);
      return r||((degrees[b]||0)-(degrees[a]||0))||name(a).localeCompare(name(b));
    });
    const featured=sorted.slice(0,4);
    if(matchQuery){
      for(const mid of mids)if(!nodeFaded(mid)&&!featured.includes(mid))featured.push(mid);
    }
    return featured;
  }
  function makeLayout(){
    const boardWidth=1030;let cursorY=42;
    const boxes={};const positions={};const visibleByZone={};
    for(let row=0;row<3;row++){
      const pair=graph.zones.slice(row*2,row*2+2);
      let rowMax=0;const rowHeights={};
      for(const z of pair){
        const mids=visibleForZone(z);
        visibleByZone[z.id]=mids;
        const h=79+Math.ceil(mids.length/2)*75+43;
        rowHeights[z.id]=Math.max(250,h);
        rowMax=Math.max(rowMax,rowHeights[z.id]);
      }
      for(let col=0;col<pair.length;col++){
        const z=pair[col],xx=28+col*(ZONE_W+COL_GAP);
        boxes[z.id]={x:xx,y:cursorY,width:ZONE_W,height:rowHeights[z.id]};
        visibleByZone[z.id].forEach((mid,i)=>{
          const x=xx+16+(i%2)*(NODE_W+NODE_GAP),y=cursorY+79+Math.floor(i/2)*75;
          positions[mid]={x,y,zone:z.id};
        });
      }
      cursorY+=rowMax+30;
    }
    return {width:boardWidth,height:cursorY+25,positions,zoneBoxes:boxes,visibleByZone};
  }
  function svg(tag){return document.createElementNS("http://www.w3.org/2000/svg",tag);}
  function lineGeometry(edge){
    const a=layout.positions[edge.source],b=layout.positions[edge.target];
    if(!a||!b)return null;
    const ax=a.x+NODE_W/2,ay=a.y+NODE_H/2,bx=b.x+NODE_W/2,by=b.y+NODE_H/2;
    const dx=bx-ax,dy=by-ay;
    const side=Math.abs(dx)>Math.abs(dy)*.7;
    let x1,y1,x2,y2;
    if(side){
      x1=ax+Math.sign(dx)*NODE_W*.49;y1=ay;
      x2=bx-Math.sign(dx)*NODE_W*.49;y2=by;
    }else{
      x1=ax;y1=ay+Math.sign(dy)*NODE_H*.49;
      x2=bx;y2=by-Math.sign(dy)*NODE_H*.49;
    }
    const len=Math.max(35,Math.min(170,Math.abs(side?x2-x1:y2-y1)*.5));
    const c1x=side?x1+Math.sign(dx)*len:x1;
    const c1y=side?y1:y1+Math.sign(dy)*len;
    const c2x=side?x2-Math.sign(dx)*len:x2;
    const c2y=side?y2:y2-Math.sign(dy)*len;
    return {d:"M "+x1+" "+y1+" C "+c1x+" "+c1y+" "+c2x+" "+c2y+" "+x2+" "+y2,
      mx:(x1+x2)/2,my:(y1+y2)/2};
  }
  function graphEdgesVisible(){
    return graph.method_edges.filter(e=>
      displayed.has(e.source)&&displayed.has(e.target)&&
      (state.taxonomy||e.type!=="specializes")&&
      (state.contrasts||e.type!=="contrasts_with"));
  }
  function renderGraph(){
    layout=makeLayout();
    displayed=new Set(Object.keys(layout.positions));
    const scene=$("scene"),area=$("zone-layer"),nodes=$("method-layer"),edges=$("edge-layer"),lines=$("graph-lines");
    scene.style.width=layout.width+"px";scene.style.height=layout.height+"px";
    area.replaceChildren();nodes.replaceChildren();edges.replaceChildren();lines.replaceChildren();
    lines.setAttribute("width",String(layout.width));lines.setAttribute("height",String(layout.height));
    lines.setAttribute("viewBox","0 0 "+layout.width+" "+layout.height);
    const defs=svg("defs");lines.append(defs);
    graph.zones.forEach(z=>{
      const b=layout.zoneBoxes[z.id],listed=layout.visibleByZone[z.id];
      const match=z.method_ids.filter(mid=>relevance(mid)>0).length;
      const box=textEl("section","zone-panel"+(state.stage&&match===0?" dimmed":""),"");
      box.style.left=b.x+"px";box.style.top=b.y+"px";
      box.style.width=b.width+"px";box.style.height=b.height+"px";
      const head=textEl("div","zone-head");
      const title=textEl("div","");
      title.append(textEl("div","category","VISUAL REGION / "+String(graph.zones.indexOf(z)+1).padStart(2,"0")));
      title.append(textEl("h3","",tr(z.label)));
      title.append(textEl("div","zone-counter",(state.stage?match+" "+t("mapped")+" / ":"")+z.method_ids.length+" "+t("methods")));
      head.append(title);
      head.append(textEl("small","",listed.length+" / "+z.method_ids.length));
      box.append(head);
      if(!state.showAll){
        const expanded=state.expanded.has(z.id);
        const toggle=button("zone-toggle",(expanded?t("less"):t("more"))+" · "+(z.method_ids.length-listed.length),()=>{
          if(expanded)state.expanded.delete(z.id);else state.expanded.add(z.id);
          state.activeZone=z.id;renderGraph();renderZoneNav();
        });
        if(!expanded||listed.length<z.method_ids.length)box.append(toggle);
      }
      area.append(box);
      listed.forEach(mid=>{
        const m=methodById[mid],p=layout.positions[mid];
        const b=button("method-node","",()=>select("method",mid));
        let cls="";
        const grade=bestRole(mid)?.grade;
        if(state.stage&&grade)cls=grade==="direct"?" direct":grade==="family"?" family-match":" ancestor-match";
        if(nodeFaded(mid))cls+=" dimmed";
        if(state.selected?.kind==="method"&&state.selected.id===mid)cls+=" selected";
        b.className+=cls;
        b.style.left=p.x+"px";b.style.top=p.y+"px";
        b.style.setProperty("--focus",stageById[state.stage]?.color||"#305f83");
        b.style.setProperty("--focus-soft",(stageById[state.stage]?.color||"#305f83")+"13");
        b.append(textEl("strong","",tr(m.label)));
        b.append(textEl("small","",state.stage?(
          grade==="direct"?t("direct"):grade==="family"?t("family"):grade==="ancestor"?t("ancestor"):"—"
        ):m.families.length+" "+t("family")));
        b.append(textEl("i","status-dot",""));
        b.dataset.methodId=mid;
      b.setAttribute("aria-label",tr(m.label));b.title=tr(m.summary);
        nodes.append(b);
      });
    });
    const visibleEdges=graphEdgesVisible();
    visibleEdges.forEach((edge,i)=>{
      const shape=lineGeometry(edge);if(!shape)return;
      const color=edge.type==="specializes"?"#a4b3c2":edge.type==="contrasts_with"?"#b0baca":edge.color;
      const markerId="m-"+String(i);
      const marker=svg("marker");marker.setAttribute("id",markerId);
      marker.setAttribute("viewBox","0 0 10 10");marker.setAttribute("markerWidth","5");marker.setAttribute("markerHeight","5");
      marker.setAttribute("refX","8");marker.setAttribute("refY","5");marker.setAttribute("orient","auto");
      const arrow=svg("path");arrow.setAttribute("d","M 0 0 L 10 5 L 0 10 z");arrow.setAttribute("fill",color);
      marker.append(arrow);defs.append(marker);
      const path=svg("path");
      path.setAttribute("d",shape.d);path.setAttribute("stroke",color);
      path.setAttribute("marker-end","url(#"+markerId+")");
      path.classList.add("edge-line");
      path.classList.add(edge.type);
      if(edgeFaded(edge))path.classList.add("dimmed");
      if(state.selected?.kind==="edge"&&state.selected.id===edge.id)path.classList.add("selected");
      lines.append(path);
      const hit=svg("path");hit.setAttribute("d",shape.d);hit.classList.add("edge-hit");
      hit.dataset.edgeId=edge.id;
      hit.addEventListener("click",()=>select("edge",edge.id));lines.append(hit);
      if(edge.type==="extends"||edge.type==="combines"){
        if(state.stage&&!edge.stages.includes(state.stage)&&state.selected?.id!==edge.id)return;
        if(state.role&&edgeFaded(edge))return;
        const label=(edge.type==="combines"?(state.lang==="zh"?"融合：":"Fusion: "):"")
          +(tr(edge.innovation).slice(0,state.lang==="zh"?10:16));
        const b=button("edge-mini"+(edgeFaded(edge)?" dimmed":"")+
          (state.selected?.id===edge.id?" selected":""),label,()=>select("edge",edge.id));
        b.style.left=shape.mx+"px";b.style.top=(shape.my-9)+"px";
        b.style.setProperty("--edge-color",color);
        b.title=tr(edge.innovation);
        b.dataset.edgeId=edge.id;
        edges.append(b);
      }
    });
    $("lens-info").replaceChildren();
    const s=stageById[state.stage];const summary=$("lens-info");
    const focusLabel=textEl("strong","",s?t("stageFocus")+"："+shortStage[s.id][state.lang==="zh"?0:1]:t("noFocus"));
    summary.append(focusLabel);
    const active=state.stage?Object.keys(graph.stage_roles[state.stage]).length:graph.methods.length;
    summary.append(document.createTextNode(" · "+active+" / "+graph.methods.length+" "+t("mapped")));
    $("display-count").textContent=displayed.size+" / "+graph.methods.length+" "+t("methods")+" · "+visibleEdges.length+" "+t("links");
    $("toggle-all").textContent=state.showAll?t("collapseAll"):t("expandAll");
    applyTransform();
  }
  function field(root,title,description){
    if(description){root.append(textEl("div","section-label",title));root.append(textEl("p","",description));}
  }
  function badge(root,text,color){
    const b=textEl("span","badge",text);
    if(color)b.style.borderLeft="3px solid "+color;root.append(b);
  }
  function renderInspector(){
    const root=$("inspect");root.replaceChildren();
    if(!state.selected){
      root.append(textEl("div","empty-symbol","↗"));
      root.append(textEl("h3","",t("emptyTitle")));
      field(root,"",t("emptyBody"));return;
    }
    const chosen=state.selected;
    if(chosen.kind==="method"){
      const m=methodById[chosen.id];
      if(!m)return;
      root.append(textEl("span","category",t("methodType")));
      root.append(textEl("h3","",tr(m.label)));
      field(root,"",tr(m.summary));
      field(root,t("core"),tr(m.core));
      field(root,t("limits"),m.limitations[state.lang].slice(0,3).join(" · "));
      root.append(textEl("div","section-label",t("memberships")));
      m.families.forEach(fid=>badge(root,name(fid)));
      root.append(textEl("div","section-label",t("stageUsage")));
      const roles=[];
      for(const stage of graph.stages){
        for(const role of graph.stage_roles[stage.id]?.[m.id]||[]){
          if(role.level==="direct"||role.level==="family"){
            roles.push({stage,role});
          }
        }
      }
      if(!roles.length)root.append(textEl("p","small-note",t("noRole")));
      roles.slice(0,8).forEach(item=>{
        const b=textEl("div","explanation");
        b.style.setProperty("--focus",item.stage.color);
        b.style.setProperty("--focus-soft",item.stage.color+"12");
        b.append(textEl("strong","",shortStage[item.stage.id][state.lang==="zh"?0:1]+" · "+(item.role.level==="direct"?t("direct"):t("family"))));
        b.append(textEl("div","detail-pair",tr(item.role.role)));
        if(item.role.level!=="direct")b.append(textEl("div","small-note",t("caution")));
        root.append(b);
      });
      root.append(textEl("div","section-label",t("start")));
      if(!m.readings.length)root.append(textEl("p","small-note",t("noLiterature")));
      m.readings.forEach(src=>{
        const a=link(src.url,src.title,"evidence");
        a.append(textEl("small","",src.focus));a.title=src.why;root.append(a);
      });
      const landmarks=m.sources.filter(s=>s.landmark);
      if(landmarks.length){
        root.append(textEl("div","section-label",t("papers")));
        landmarks.slice(0,5).forEach(s=>{
          const a=link(s.url,s.title,"evidence");a.append(textEl("small","",s.year+" · "+s.role+" · Landmark"));root.append(a);
        });
      }
      root.append(link(repo+m.source_path,t("source"),"evidence"));
    }else if(chosen.kind==="role"){
      const role=funcById[chosen.id];if(!role)return;
      const stage=stageById[role.stage];
      root.append(textEl("span","category",t("role")));
      root.append(textEl("h3","",shortStage[role.stage][state.lang==="zh"?0:1]+" → "+name(role.target)));
      const block=textEl("div","explanation");
      block.style.setProperty("--focus",stage.color);block.style.setProperty("--focus-soft",stage.color+"15");
      block.append(textEl("strong","",role.type==="family"?t("roleFamily"):t("roleDirect")));
      block.append(textEl("p","",tr(role.role)));root.append(block);
      field(root,t("role"),t("scope_"+role.scope));
      if(role.type==="family")field(root,"",t("caution"));
      const applicable=role.target.startsWith("method.")?[role.target]:
        graph.methods.filter(m=>m.ancestor_families[role.target]!==undefined).map(m=>m.id);
      root.append(textEl("div","section-label",applicable.length+" "+t("methods")));
      applicable.slice(0,14).forEach(id=>badge(root,name(id)));
      if(applicable.length>14)root.append(textEl("p","small-note","+"+(applicable.length-14)+" "+t("more")));
      if(role.evidence.length){
        root.append(textEl("div","section-label",t("evidence")));
        role.evidence.forEach(p=>root.append(link(p.url,p.title,"evidence")));
      }
    }else if(chosen.kind==="edge"){
      const e=edgeById[chosen.id];if(!e)return;
      root.append(textEl("span","category",t("edgeType")+" · "+e.type));
      root.append(textEl("h3","",name(e.source)+" → "+name(e.target)));
      field(root,t("innovation"),tr(e.innovation));
      field(root,t("bottleneck"),tr(e.bottleneck));
      field(root,t("tradeoff"),tr(e.tradeoff));
      if(e.stages.length){
        root.append(textEl("div","section-label",t("affected")));
        e.stages.forEach(sid=>badge(root,shortStage[sid][state.lang==="zh"?0:1],stageById[sid]?.color));
      }
      if(e.evidence.length){
        root.append(textEl("div","section-label",t("evidence")));
        e.evidence.forEach(p=>root.append(link(p.url,p.title,"evidence")));
      }
      root.append(link(repo+e.source_path,t("source"),"evidence"));
    }
  }
  function select(kind,id){
    state.selected={kind,id};
    renderGraph();renderInspector();
  }
  function applyTransform(){
    $("scene").style.transform="translate("+state.panX+"px,"+state.panY+"px) scale("+state.zoom+")";
  }
  function fit(){
    if(!layout)return;
    const v=$("viewport"),s=Math.min(1.0,(v.clientWidth-32)/layout.width,(v.clientHeight-32)/layout.height);
    if(v.clientWidth<580){
      state.zoom=.8;state.panX=12;state.panY=15;
    }else{
      state.zoom=Math.max(.57,s);
      state.panX=(v.clientWidth-layout.width*state.zoom)/2;
      state.panY=(v.clientHeight-layout.height*state.zoom)/2;
    }
    applyTransform();
  }
  function zoom(k){
    const v=$("viewport"),cx=v.clientWidth/2,cy=v.clientHeight/2;
    const scale=Math.max(.35,Math.min(2.2,state.zoom*k));
    const ratio=scale/state.zoom;
    state.panX=cx-(cx-state.panX)*ratio;
    state.panY=cy-(cy-state.panY)*ratio;state.zoom=scale;applyTransform();
  }
  function drag(){
    const v=$("viewport");let start=null;
    v.addEventListener("pointerdown",e=>{
      if(e.button!==0||e.target.closest("button,a"))return;
      start={x:e.clientX,y:e.clientY,panX:state.panX,panY:state.panY};
      v.classList.add("dragging");v.setPointerCapture(e.pointerId);
    });
    v.addEventListener("pointermove",e=>{
      if(!start)return;
      state.panX=start.panX+(e.clientX-start.x);state.panY=start.panY+(e.clientY-start.y);
      applyTransform();
    });
    const stop=e=>{
      start=null;v.classList.remove("dragging");
      if(v.hasPointerCapture(e.pointerId))v.releasePointerCapture(e.pointerId);
    };
    v.addEventListener("pointerup",stop);v.addEventListener("pointercancel",stop);
    v.addEventListener("wheel",e=>{
      if(!e.ctrlKey&&!e.metaKey)return;e.preventDefault();zoom(e.deltaY<0?1.10:.90);
    },{passive:false});
  }
  function refresh(refit=false){
    setLanguage();renderAxis();renderBridge();renderGraph();renderZoneNav();renderInspector();
    if(refit)requestAnimationFrame(fit);
  }
  function init(){
    try{
      const embedded=$("atlas-data");
      if(!embedded)throw Error("Embedded data is missing");
      graph=JSON.parse(embedded.textContent);
      methodById=Object.fromEntries(graph.methods.map(m=>[m.id,m]));
      familyById=Object.fromEntries(graph.families.map(f=>[f.id,f]));
      stageById=Object.fromEntries(graph.stages.map(s=>[s.id,s]));
      edgeById=Object.fromEntries(graph.method_edges.map(e=>[e.id,e]));
      funcById=Object.fromEntries(graph.functional.map(f=>[f.id,f]));
      if(Object.keys(methodById).length!==graph.methods.length)throw Error("Duplicate method IDs");
      state.lang=new URLSearchParams(location.search).get("lang")==="en"?"en":"zh";
      $("lang").addEventListener("click",()=>{
        state.lang=state.lang==="zh"?"en":"zh";refresh();
      });
      $("clear-stage").addEventListener("click",()=>{
        state.stage=null;state.role=null;state.selected=null;refresh();
      });
      $("more-roles").addEventListener("click",()=>{
        state.moreRoles=!state.moreRoles;renderBridge();
      });
      $("search").addEventListener("input",e=>{
        state.search=e.target.value;renderGraph();renderZoneNav();
      });
      $("toggle-all").addEventListener("click",()=>{
        state.showAll=!state.showAll;state.expanded.clear();renderGraph();renderZoneNav();requestAnimationFrame(fit);
      });
      $("show-taxonomy").addEventListener("change",e=>{state.taxonomy=e.target.checked;renderGraph();});
      $("show-contrasts").addEventListener("change",e=>{state.contrasts=e.target.checked;renderGraph();});
      $("zoom-plus").addEventListener("click",()=>zoom(1.18));
      $("zoom-minus").addEventListener("click",()=>zoom(.84));
      $("zoom-fit").addEventListener("click",fit);
      document.addEventListener("keydown",e=>{
        if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==="k"){e.preventDefault();$("search").focus();}
        if(e.key==="Escape"){state.role=null;state.selected=null;refresh();}
      });
      drag();refresh(true);
    }catch(error){
      console.error(error);
      $("inspect").replaceChildren(textEl("p","",lex.zh.failed));
    }
  }
  init();
})();
