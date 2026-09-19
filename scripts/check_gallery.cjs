const fs = require('node:fs');
const assert = require('node:assert/strict');
const { JSDOM } = require('jsdom');
const source = fs.readFileSync('assets/js/post-gallery.js', 'utf8');
const html = fs.readFileSync('_site/beyond-physics/chess-with-sharif/index.html', 'utf8');
let checks = 0;
function check(value, message) { assert.ok(value, message); checks++; }
function setup({supported = true, single = false} = {}) {
 const dom = new JSDOM(html, {url: 'https://site.test/beyond-physics/chess-with-sharif/', runScripts: 'outside-only'});
 const w = dom.window;
 // jsdom does not implement native dialog modality: stub only its open/close API.
 if (supported) {
  w.HTMLDialogElement.prototype.showModal = function () { this.open = true; };
  w.HTMLDialogElement.prototype.close = function () { this.open = false; this.dispatchEvent(new w.Event('close')); };
 } else w.HTMLDialogElement.prototype.showModal = undefined;
 if (single) [...w.document.querySelectorAll('[data-post-photo]')].slice(1).forEach(link => link.closest('figure').remove());
 w.eval(source);
 return {dom, w, d: w.document, links: [...w.document.querySelectorAll('[data-post-photo]')]};
}
const {dom, w, d, links} = setup();
const dialog = d.querySelector('dialog');
const counter = () => dialog.querySelector('.photo-viewer__counter').textContent;
const img = dialog.querySelector('img');
check(links.length === 8 && !dialog.open, 'eight photos; viewer initially closed');
links[3].click();
check(dialog.open && counter() === 'Photo 4 of 8', 'selected thumbnail opens correct slide');
check(w.location.pathname === '/beyond-physics/chess-with-sharif/', 'page URL unchanged');
check(img.src === links[3].href && img.alt === links[3].querySelector('img').alt, 'full photo and descriptive alt');
check(d.activeElement === dialog.querySelector('.photo-viewer__close'), 'close receives focus');
check(d.documentElement.classList.contains('photo-viewer-open'), 'background scrolling locked');
img.dispatchEvent(new w.Event('load'));
check(!img.hidden && !dialog.querySelector('[role=status]').textContent, 'successful load clears status');
dialog.querySelector('.photo-viewer__next').click();
check(counter() === 'Photo 5 of 8', 'next moves across gallery groups');
check(dialog.querySelector('.photo-viewer__caption a').href === 'https://olympiad16.iut.ac.ir/fa/node/1714', 'credit link matches slide');
function key(key) { dialog.dispatchEvent(new w.KeyboardEvent('keydown', {key, bubbles: true, cancelable: true})); }
key('End'); check(counter() === 'Photo 8 of 8', 'End reaches last slide');
key('ArrowRight'); check(counter() === 'Photo 1 of 8', 'next wraps');
key('ArrowLeft'); check(counter() === 'Photo 8 of 8', 'previous wraps');
key('Home'); check(counter() === 'Photo 1 of 8', 'Home reaches first slide');
img.dispatchEvent(new w.Event('error'));
check(img.hidden && dialog.querySelector('[role=status]').textContent.includes('could not load'), 'image error state');
dialog.querySelector('.photo-viewer__next').click(); img.dispatchEvent(new w.Event('load'));
check(!img.hidden, 'navigation recovers from image failure');
dialog.querySelector('.photo-viewer__close').click();
check(!dialog.open && d.activeElement === links[3] && !d.documentElement.classList.contains('photo-viewer-open'), 'close restores opener and scrolling');
links[0].click();
const stage = dialog.querySelector('.photo-viewer__stage');
function pointer(type, x, y) {
 const event = new w.Event(type); Object.assign(event, {pointerType: 'touch', isPrimary: true, clientX: x, clientY: y});stage.dispatchEvent(event);
}
pointer('pointerdown',200,50);pointer('pointerup',100,52);
check(counter()==='Photo 2 of 8','horizontal touch swipe advances');
pointer('pointerdown',200,50);pointer('pointerup',198,180);
check(counter()==='Photo 2 of 8','vertical gesture does not advance');
dialog.dispatchEvent(new w.MouseEvent('click', {bubbles:true}));
check(!dialog.open && d.activeElement===links[0], 'backdrop closes and restores focus');
let defaultAtTarget;
links[0].addEventListener('click', event => {defaultAtTarget=event.defaultPrevented;event.preventDefault();}, {once:true});
links[0].dispatchEvent(new w.MouseEvent('click',{bubbles:true,cancelable:true,ctrlKey:true}));
check(defaultAtTarget===false && !dialog.open,'modified clicks retain normal link behavior');
dom.window.close();
const solo=setup({single:true});solo.links[0].click();
check(solo.d.querySelector('.photo-viewer__next').hidden && solo.d.querySelector('.photo-viewer__previous').hidden, 'one photo hides carousel controls');solo.dom.window.close();
const fallback=setup({supported:false});
check(!fallback.d.querySelector('dialog') && fallback.links.every(link=>link.href && !link.hasAttribute('aria-haspopup')), 'unsupported dialog keeps ordinary image links');fallback.dom.window.close();
console.log(`PASS: ${checks} gallery behavior assertions. Native focus trapping, Escape, gestures, and rendering still require a real browser.`);
