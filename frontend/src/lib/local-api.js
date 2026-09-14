const DEFAULT_BASE = '/local-api';
const DEFAULT_INTERVAL_MS = 3000;

export async function probeLocalApi(base = DEFAULT_BASE) {
	const url = `${String(base || DEFAULT_BASE).replace(/\/$/, '')}/health`;
	try {
		const response = await fetch(url, { method: 'GET', headers: { Accept: 'application/json' } });
		if (!response.ok) {
			return { available: false, reason: `http_${response.status}` };
		}
		const body = await response.json();
		if (body?.schema_version !== 'health/v1' || body?.status !== 'ok') {
			return { available: false, reason: 'health_invalid' };
		}
		return { available: true, reason: 'ok' };
	} catch {
		return { available: false, reason: 'unreachable' };
	}
}

export async function practicePageAvailable(base = '') {
	const prefix = String(base || '').replace(/\/$/, '');
	const url = `${prefix}/practice/`;
	try {
		const response = await fetch(url, { method: 'GET', headers: { Accept: 'text/html' } });
		return response.ok;
	} catch {
		return false;
	}
}

export function localApiStatusText(result) {
	if (result?.available) return '本地 API 已连接';
	if (result?.reason === 'unreachable') return '本地 API 未启动';
	return '本地 API 不可用';
}

export function watchLocalApi(onChange, options = {}) {
	const getBase = typeof options.base === 'function' ? options.base : () => options.base || DEFAULT_BASE;
	const intervalMs = Number(options.intervalMs) > 0 ? Number(options.intervalMs) : DEFAULT_INTERVAL_MS;
	let stopped = false;
	let timer = 0;
	let lastKey = '';

	async function tick(force = false) {
		if (stopped) return;
		const result = await probeLocalApi(getBase());
		if (stopped) return;
		const key = `${result.available}:${result.reason}`;
		if (result.available) {
			lastKey = key;
			onChange(result);
			return;
		}
		if (!force && key === lastKey) return;
		lastKey = key;
		onChange(result);
	}

	function onVisible() {
		if (!document.hidden) tick(true);
	}

	tick(true);
	timer = window.setInterval(() => tick(false), intervalMs);
	document.addEventListener('visibilitychange', onVisible);
	return () => {
		stopped = true;
		window.clearInterval(timer);
		document.removeEventListener('visibilitychange', onVisible);
	};
}
