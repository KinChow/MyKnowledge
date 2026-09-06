import fs from 'node:fs';
import path from 'node:path';

export interface CatalogItem {
	id: string;
	title?: string;
	route?: string;
	links?: string[];
	domain?: string | null;
	kind?: string | null;
	tags?: string[];
	content_sha256?: string;
}
export interface GraphEdge {
	source: string;
	target: string;
	kind: 'rel' | 'tag' | string;
	weight?: number;
}

export interface GraphData {
	nodes: Array<{ id: string; title?: string; route?: string; domain?: string | null; tags?: string[] }>;
	edges: GraphEdge[];
}

export const DOMAIN_META = [
	{ key: 'computer-science', label: '计算机科学', color: '#2563eb' },
	{ key: 'multimedia', label: '多媒体与影像', color: '#0d9488' },
	{ key: 'work-methods', label: '工作方法', color: '#d97706' },
	{ key: 'tools', label: '工具', color: '#7c3aed' },
	{ key: 'reading-notes', label: '读书笔记', color: '#db2777' },
] as const;

export const KIND_LABELS: Record<string, string> = {
	knowledge: '知识',
	reference: '参考',
};

function readJson<T>(name: string, fallback: T): T {
	const file = path.join(process.cwd(), 'public', 'generated', name);
	try {
		return JSON.parse(fs.readFileSync(file, 'utf8')) as T;
	} catch {
		return fallback;
	}
}

export function loadCatalog(): CatalogItem[] {
	const payload = readJson<{ items?: CatalogItem[] }>('catalog.json', { items: [] });
	return Array.isArray(payload.items) ? payload.items : [];
}

export function loadGraph(): GraphData {
	return readJson<GraphData>('graph.json', { nodes: [], edges: [] });
}

export function domainLabel(domain?: string | null): string {
	return DOMAIN_META.find((item) => item.key === domain)?.label || '其他';
}

export function domainColor(domain?: string | null): string {
	return DOMAIN_META.find((item) => item.key === domain)?.color || '#64748b';
}

export function routePath(base: string, routeOrId: string): string {
	const cleanRoute = routeOrId.replace(/^\/+|\/+$/g, '');
	const cleanBase = base === './' ? '.' : base.replace(/\/+$/, '');
	return `${cleanBase}/${cleanRoute}/`;
}

export function degreeMap(edges: GraphEdge[]): Map<string, number> {
	const degrees = new Map<string, number>();
	for (const edge of edges) {
		degrees.set(edge.source, (degrees.get(edge.source) || 0) + 1);
		degrees.set(edge.target, (degrees.get(edge.target) || 0) + 1);
	}
	return degrees;
}
