import { defineConfig } from 'astro/config';
import fs from 'node:fs';
import path from 'node:path';
import starlight from '@astrojs/starlight';
import { fileURLToPath } from 'node:url';

const frontendDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(frontendDir, '..');

export default defineConfig({
	output: 'static',
	vite: {
		server: {
			proxy: {
				'/local-api': {
					target: 'http://127.0.0.1:8765',
					rewrite: (requestPath) => requestPath.replace(/^\/local-api/, '/api'),
					configure: (proxy) => {
						proxy.on('proxyReq', (proxyReq) => {
							const tokenPath = path.join(projectRoot, 'var', 'state', 'capability-token');
							if (fs.existsSync(tokenPath)) {
								proxyReq.setHeader('X-MyKnowledge-Capability', fs.readFileSync(tokenPath, 'utf8').trim());
							}
						});
					},
				},
			},
		},
	},
	integrations: [
		starlight({
			title: 'MyKnowledge',
			defaultLocale: 'root',
			locales: { root: { label: '中文', lang: 'zh-CN' } },
			customCss: ['./src/styles/workbench.css'],
			components: {
				PageTitle: './src/components/PageTitle.astro',
				PageSidebar: './src/components/PageSidebar.astro',
			},
			sidebar: [
				{
					label: '知识',
					items: [
						{ label: '首页', link: '/' },
						{ label: '知识文章', items: [{ autogenerate: { directory: 'wiki' } }] },
						{ label: '知识图谱', link: '/graph/' },
					],
				},
			],
		}),
	],
});
