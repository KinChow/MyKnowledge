import fs from 'node:fs';
// graph/v1：节点带 tags；边两类——
//   kind:'rel'  显式 related 双链（真源：wiki front matter related，目标须在 catalog 内）
//   kind:'tag'  同标签软关联（构建时确定性派生：每节点取共享标签数 top-3 且 ≥2 的邻居，
//               (score desc, id asc) 排序保证确定性；用于弥补 related 覆盖率不足）
// 软关联只读已发布内容，不回写 wiki，不参与任何 hash/确认链。
const catalog=JSON.parse(fs.readFileSync('public/generated/catalog.json','utf8'));
const ids=new Set(catalog.items.map(x=>x.id));
const nodes=catalog.items.map(x=>({id:x.id,title:x.title,route:x.route||`wiki/${x.id}`,domain:x.domain||null,tags:x.tags||[]}));
const edges=[];
for(const item of catalog.items) for(const target of item.links||[]) if(ids.has(target)) edges.push({source:item.id,target,kind:'rel',weight:1});

// ---- 同标签软关联 ----
const tagIndex=new Map(); // tag -> [nodeId]
for(const n of nodes) for(const t of n.tags){
  if(!tagIndex.has(t)) tagIndex.set(t,[]);
  tagIndex.get(t).push(n.id);
}
const pairScore=new Map(); // 'a\u0000b' (a<b) -> 共享标签数
for(const members of tagIndex.values()){
  if(members.length<2) continue; // 单篇标签不产生共现
  for(let i=0;i<members.length;i++) for(let j=i+1;j<members.length;j++){
    const [a,b]=members[i]<members[j]?[members[i],members[j]]:[members[j],members[i]];
    const key=a+'\u0000'+b;
    pairScore.set(key,(pairScore.get(key)||0)+1);
  }
}
// 每节点收集候选（score≥2），取 (score desc, id asc) top-3；边按节点对去重
const perNode=new Map();
for(const [key,score] of pairScore){
  if(score<2) continue;
  const [a,b]=key.split('\u0000');
  for(const [self,other] of [[a,b],[b,a]]){
    if(!perNode.has(self)) perNode.set(self,[]);
    perNode.get(self).push({other,score});
  }
}
const seen=new Set(edges.map(e=>[e.source,e.target].sort().join('\u0000')));
for(const [ownId,cands] of perNode){
  cands.sort((x,y)=>y.score-x.score||(x.other<y.other?-1:1));
  for(const {other,score} of cands.slice(0,3)){
    const key=[ownId,other].sort().join('\u0000');
    if(seen.has(key)) continue;
    seen.add(key);
    edges.push({source:ownId,target:other,kind:'tag',weight:score});
  }
}
fs.writeFileSync('public/generated/graph.json',JSON.stringify({schema_version:'graph/v1',generated_from:catalog.generated_from,nodes,edges},null,2));
console.log(`graph: ${nodes.length} nodes, ${edges.length} edges (rel: ${edges.filter(e=>e.kind==='rel').length}, tag: ${edges.filter(e=>e.kind==='tag').length})`);
