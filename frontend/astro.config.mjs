import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
export default defineConfig({ output: 'static', integrations: [starlight({ title: 'MyKnowledge', defaultLocale: 'root', locales: { root: { label: '中文', lang: 'zh-CN' } }, sidebar: [{ label: '知识', items: [{ label: '首页', link: '/' }] }] })] });
