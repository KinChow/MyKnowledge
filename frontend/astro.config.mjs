import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
	output: 'static',
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
