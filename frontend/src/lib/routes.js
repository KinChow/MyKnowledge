/** Shared by Astro components, browser code, and release scripts. */
export function routePath(base, route = '') {
  const prefix = '/' + String(base || '/').replace(/^\/+|\/+$/g, '');
  const normalizedBase = prefix === '/' ? '/' : prefix + '/';
  let value = String(route).replace(/^\/+/, '');
  const basePart = normalizedBase.slice(1);
  if (basePart && value.startsWith(basePart)) value = value.slice(basePart.length);
  const boundary = value.search(/[?#]/);
  const pathname = boundary < 0 ? value : value.slice(0, boundary);
  const suffix = boundary < 0 ? '' : value.slice(boundary);
  return normalizedBase + pathname.replace(/\/+$/, '') + (pathname ? '/' : '') + suffix;
}
