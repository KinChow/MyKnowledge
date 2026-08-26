import fs from 'node:fs'; import path from 'node:path';
const target=process.argv[2]||'dist';
const catalog=JSON.parse(fs.readFileSync('public/generated/catalog.json','utf8'));
const graph=JSON.parse(fs.readFileSync('public/generated/graph.json','utf8'));
if(catalog.items.length!==graph.nodes.length||graph.edges.some(e=>!catalog.items.some(x=>x.id===e.source)||!catalog.items.some(x=>x.id===e.target))) throw new Error('graph_catalog_not_closed');
if(!fs.existsSync(path.join(target,'index.html'))) throw new Error('dist_missing');
const html=[]; const walk=(dir)=>{for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const full=path.join(dir,entry.name); if(entry.isDirectory()) walk(full); else if(entry.name.endsWith('.html')) html.push(full);}}; walk(target);
const pagefind=path.join(target,'pagefind','pagefind-entry.json');
if(fs.existsSync(pagefind)) { const entry=JSON.parse(fs.readFileSync(pagefind,'utf8')); const pageCount=Object.values(entry.languages||{}).reduce((sum,value)=>sum+Number(value.page_count||0),0); if(pageCount!==html.length) throw new Error('pagefind_html_count_mismatch'); if(catalog.items.length>pageCount) throw new Error('pagefind_catalog_not_closed'); }
const sitemapFiles=[]; const collectSitemap=(dir)=>{for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const full=path.join(dir,entry.name); if(entry.isDirectory()) collectSitemap(full); else if(entry.name.endsWith('.xml')) sitemapFiles.push(full);}}; collectSitemap(target);
if(sitemapFiles.length && catalog.items.length) { const sitemap=sitemapFiles.map(file=>fs.readFileSync(file,'utf8')).join('\n'); for(const item of catalog.items){const route=String(item.route||'').replace(/^\//,''); if(route && !sitemap.includes(`>${route}<`) && !sitemap.includes(`/${route}<`)) throw new Error('sitemap_catalog_not_closed');} }
console.log('build_valid');
