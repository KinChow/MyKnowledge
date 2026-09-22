import fs from 'node:fs'; import path from 'node:path';
import {routePath} from '../src/lib/routes.js';
const base=process.env.PUBLIC_BASE_PATH || '/';
const target=process.argv[2]||'dist';
const catalog=JSON.parse(fs.readFileSync('public/generated/catalog.json','utf8'));
const graph=JSON.parse(fs.readFileSync('public/generated/graph.json','utf8'));
if(catalog.items.length!==graph.nodes.length||graph.edges.some(e=>!catalog.items.some(x=>x.id===e.source)||!catalog.items.some(x=>x.id===e.target))) throw new Error('graph_catalog_not_closed');
if(!fs.existsSync(path.join(target,'index.html'))) throw new Error('dist_missing');
const html=[]; const walk=(dir)=>{for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const full=path.join(dir,entry.name); if(entry.isDirectory()) walk(full); else if(entry.name.endsWith('.html')) html.push(full);}}; walk(target);
const pagefind=path.join(target,'pagefind','pagefind-entry.json');
if(fs.existsSync(pagefind)) { const entry=JSON.parse(fs.readFileSync(pagefind,'utf8')); const pageCount=Object.values(entry.languages||{}).reduce((sum,value)=>sum+Number(value.page_count||0),0); /* pagefind 只索引 Starlight 文档页（带 data-pagefind-body），不含 index/graph/404 等自定义页；闭包对象是 catalog 而非全部 html */ if(pageCount!==catalog.items.length) throw new Error('pagefind_catalog_not_closed'); }
const sitemapFiles=[]; const collectSitemap=(dir)=>{for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const full=path.join(dir,entry.name); if(entry.isDirectory()) collectSitemap(full); else if(entry.name.endsWith('.xml')) sitemapFiles.push(full);}}; collectSitemap(target);
if(sitemapFiles.length) {
  const sitemap=sitemapFiles.map(file=>fs.readFileSync(file,'utf8')).join('\n');
  const urls=[...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match)=>match[1]);
  const expected=new Set([routePath(base,''),routePath(base,'graph')]);
  for(const item of catalog.items){const route=String(item.route||'').replace(/^\//,'').replace(/\/$/,''); if(route) expected.add(routePath(base,route));}
  if(urls.length!==new Set(urls).size || urls.length!==expected.size || urls.some((url)=>!expected.has(url))) throw new Error('sitemap_catalog_not_closed');
}
for(const file of html) {
  const text=fs.readFileSync(file,'utf8');
  if(base!=='/' && /(?:href|src)=["']\/wiki\//.test(text)) throw new Error(`unprefixed_wiki_link:${file}`);
  for(const match of text.matchAll(/href=["']([^"']+)["']/g)) {
    const url=match[1].split(/[?#]/)[0];
    const prefix=routePath(base,'wiki');
    if(url.startsWith(prefix)) {
      const relative=url.slice(routePath(base,'').length).replace(/\/$/,'');
      if(!fs.existsSync(path.join(target,relative,'index.html'))) throw new Error(`broken_wiki_link:${url}`);
    }
  }
}
console.log('build_valid');
