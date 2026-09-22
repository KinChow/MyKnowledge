import { defineConfig } from 'astro/config';
import path from 'node:path';
import starlight from '@astrojs/starlight';
import { fileURLToPath } from 'node:url';
import { localApiProxy } from './src/lib/local-api-proxy.mjs';

const frontendDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(frontendDir, '..');

// 项目页部署在 https://kinchow.github.io/<repo>/ 子路径下，需要 base 前缀。
// 本地开发与私有构建默认根路径 '/'；CI 发布项目页时用 PUBLIC_BASE_PATH 注入（如 /MyKnowledge/）。
// 站内链接与资源已统一走 import.meta.env.BASE_URL，设置 base 后整体生效，无需改组件。
const base = process.env.PUBLIC_BASE_PATH || '/';

export default defineConfig({
	base,
	output: 'static',
	vite: {
		server: {
			proxy: {
				'/local-api': localApiProxy(
					'http://127.0.0.1:8765',
					path.join(projectRoot, 'var', 'state', 'capability-token'),
				),
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
