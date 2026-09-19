const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { JSDOM } = require('jsdom');
const themeSource = fs.readFileSync('assets/js/theme.js', 'utf8');
const siteSource = fs.readFileSync('assets/js/site.js', 'utf8');
const storyPages = fs.readdirSync('_site/beyond-physics', { withFileTypes: true })
 .filter(entry => entry.isDirectory() && fs.existsSync(path.join('_site/beyond-physics', entry.name, 'index.html')))
 .map(entry => `beyond-physics/${entry.name}/index.html`);
const pages = ['index.html', 'research/index.html', 'cv/index.html', 'research/laser-tissue/index.html', 'beyond-physics/index.html', ...storyPages];
let checks = 0;
function check(condition, message) { assert.ok(condition, message); checks++; }
for (const page of pages) {
 for (const saved of [null, 'light', 'dark', 'invalid']) {
  for (const systemDark of [false, true]) {
   const dom = new JSDOM(fs.readFileSync(path.join('_site', page), 'utf8'), {url: `http://127.0.0.1:4000/${page}`, runScripts: 'outside-only'});
   const { window: w } = dom;
   const queries = new Map();
   w.matchMedia = query => {
    if (!queries.has(query)) queries.set(query, {matches: query.includes('dark') && systemDark, listeners: [], addEventListener(type, callback) {this.listeners.push(callback);}});
    return queries.get(query);
   };
   if (saved) w.localStorage.setItem('rahil-theme', saved);
   let printed = 0; w.print = () => { printed++; };
   w.eval(themeSource); w.eval(siteSource);
   const root = w.document.documentElement;
   const initial = saved === 'dark' || (saved !== 'light' && systemDark) ? 'dark' : 'light';
   check(root.dataset.theme === initial, 'initial theme');
   const theme = w.document.querySelector('.theme-toggle');
   check(!theme.hidden && theme.getAttribute('aria-label').includes(initial === 'dark' ? 'light' : 'dark'), 'accessible theme button');
   theme.click();
   const changed = initial === 'dark' ? 'light' : 'dark';
   check(root.dataset.theme === changed && w.localStorage.getItem('rahil-theme') === changed, 'persisted toggle');
   queries.get('(prefers-color-scheme: dark)').listeners.forEach(fn => fn({matches: changed !== 'dark'}));
   check(root.dataset.theme === changed, 'manual preference preserved');
   const menu = w.document.querySelector('.menu-toggle');
   menu.click();
   check(menu.getAttribute('aria-expanded') === 'true' && w.document.querySelector('#site-links').classList.contains('is-open'), 'menu opens');
   w.document.dispatchEvent(new w.KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
   check(menu.getAttribute('aria-expanded') === 'false' && w.document.activeElement === menu, 'escape closes and restores focus');
   menu.click(); w.document.querySelector('#main').click();
   check(menu.getAttribute('aria-expanded') === 'false', 'outside click closes');
   menu.click(); queries.get('(min-width: 761px)').listeners.forEach(fn => fn({matches: true}));
   check(menu.getAttribute('aria-expanded') === 'false', 'desktop resize closes menu');
   w.dispatchEvent(new w.StorageEvent('storage', {key: 'rahil-theme', newValue: 'dark'}));
   check(root.dataset.theme === 'dark', 'cross-tab preference');
   const print = w.document.querySelector('.print-button');
   if (print) { check(!print.hidden, 'print shown'); print.click(); check(printed === 1, 'print invoked'); }
   check(w.document.querySelectorAll('.site-links [aria-current]').length === 1, 'current nav');
   dom.window.close();
  }
 }
}
// Privacy modes may deny localStorage; controls must still work.
const privateDom = new JSDOM(fs.readFileSync('_site/index.html','utf8'), {url:'https://site.test/',runScripts:'outside-only'});
privateDom.window.matchMedia = () => ({matches:false,addEventListener(){}});
Object.defineProperty(privateDom.window,'localStorage',{get(){throw new Error('blocked');}});
privateDom.window.eval(themeSource);privateDom.window.eval(siteSource);
privateDom.window.document.querySelector('.theme-toggle').click();
check(privateDom.window.document.documentElement.dataset.theme === 'dark','storage denial fallback');
privateDom.window.close();
console.log(`PASS: ${checks} DOM assertions across ${pages.length} page types, both system themes, saved preferences, navigation, printing, and blocked storage. This does not verify rendering.`);
