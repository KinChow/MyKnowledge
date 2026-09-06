const STORAGE_KEY = 'myknowledge:workbench:v1';
const VERSION = 1;
const MAX_RECENT = 12;

function emptyState() {
	return { version: VERSION, favorites: [], recent: [], view: 'list' };
}
function uniqueStrings(values) {
	return [...new Set(values.filter((value) => typeof value === 'string' && value.trim()))];
}

function normalizeState(value) {
	if (!value || typeof value !== 'object') return emptyState();
	const recent = Array.isArray(value.recent)
		? value.recent
				.filter((item) => item && typeof item.id === 'string' && Number.isFinite(item.visitedAt))
				.map((item) => ({ id: item.id, visitedAt: item.visitedAt }))
				.sort((a, b) => b.visitedAt - a.visitedAt)
				.slice(0, MAX_RECENT)
		: [];
	return {
		version: VERSION,
		favorites: uniqueStrings(Array.isArray(value.favorites) ? value.favorites : []),
		recent,
		view: value.view === 'compact' ? 'compact' : 'list',
	};
}

function notify() {
	if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent('myknowledge:state-change'));
}

export function readWorkbenchState() {
	try {
		const raw = window.localStorage.getItem(STORAGE_KEY);
		return { state: normalizeState(raw ? JSON.parse(raw) : null), available: true };
	} catch {
		return { state: emptyState(), available: false };
	}
}

export function writeWorkbenchState(state) {
	try {
		window.localStorage.setItem(STORAGE_KEY, JSON.stringify(normalizeState(state)));
		notify();
		return true;
	} catch {
		return false;
	}
}

export function toggleFavorite(id) {
	const { state } = readWorkbenchState();
	const favorites = new Set(state.favorites);
	if (favorites.has(id)) favorites.delete(id);
	else favorites.add(id);
	return writeWorkbenchState({ ...state, favorites: [...favorites] });
}

export function isFavorite(id) {
	return readWorkbenchState().state.favorites.includes(id);
}

export function recordRecent(id) {
	const { state } = readWorkbenchState();
	const recent = [{ id, visitedAt: Date.now() }, ...state.recent.filter((item) => item.id !== id)].slice(
		0,
		MAX_RECENT,
	);
	return writeWorkbenchState({ ...state, recent });
}

export function setWorkbenchView(view) {
	const { state } = readWorkbenchState();
	return writeWorkbenchState({ ...state, view });
}

export function subscribeToWorkbenchState(listener) {
	window.addEventListener('myknowledge:state-change', listener);
	window.addEventListener('storage', listener);
	return () => {
		window.removeEventListener('myknowledge:state-change', listener);
		window.removeEventListener('storage', listener);
	};
}
