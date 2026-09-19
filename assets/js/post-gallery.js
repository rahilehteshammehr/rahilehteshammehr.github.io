(() => {
  const links = [...document.querySelectorAll('[data-post-photo]')];
  if (!links.length || typeof HTMLDialogElement === 'undefined' ||
      typeof HTMLDialogElement.prototype.showModal !== 'function') return;

  const dialog = document.createElement('dialog');
  dialog.className = 'photo-viewer';
  dialog.setAttribute('aria-label', 'Photo viewer');
  dialog.innerHTML = `
    <div class="photo-viewer__panel">
      <div class="photo-viewer__header">
        <p class="photo-viewer__counter" aria-live="polite" aria-atomic="true"></p>
        <button type="button" class="photo-viewer__close" autofocus>Close<span class="visually-hidden"> photo viewer</span></button>
      </div>
      <div class="photo-viewer__stage">
        <p class="photo-viewer__status" role="status"></p>
      </div>
      <div class="photo-viewer__caption"></div>
      <div class="photo-viewer__controls">
        <button type="button" class="photo-viewer__previous" aria-label="Previous photograph">Previous</button>
        <button type="button" class="photo-viewer__next" aria-label="Next photograph">Next</button>
      </div>
    </div>`;
  document.body.append(dialog);
  const image = document.createElement('img');
  image.className = 'photo-viewer__image';
  image.alt = '';
  const caption = dialog.querySelector('.photo-viewer__caption');
  const counter = dialog.querySelector('.photo-viewer__counter');
  const status = dialog.querySelector('.photo-viewer__status');
  const stage = dialog.querySelector('.photo-viewer__stage');
  stage.prepend(image);
  const close = dialog.querySelector('.photo-viewer__close');
  const previous = dialog.querySelector('.photo-viewer__previous');
  const next = dialog.querySelector('.photo-viewer__next');
  previous.hidden = next.hidden = links.length < 2;
  let index = 0;
  let opener = null;
  let swipeStart = null;

  function show(position) {
    index = (position + links.length) % links.length;
    const link = links[index];
    const thumbnail = link.querySelector('img');
    const sourceCaption = link.closest('figure').querySelector('figcaption');
    image.hidden = true;
    status.textContent = 'Loading photograph…';
    image.onload = () => { image.hidden = false; status.textContent = ''; };
    image.onerror = () => { image.hidden = true; status.textContent = links.length > 1 ? 'This photograph could not load. Try another using Previous or Next.' : 'This photograph could not load. Close the viewer and try again.'; };
    image.alt = thumbnail.alt;
    image.src = link.href;
    counter.textContent = `Photo ${index + 1} of ${links.length}`;
    caption.replaceChildren(...(sourceCaption ? [...sourceCaption.childNodes].map(node => node.cloneNode(true)) : []));
    caption.hidden = !sourceCaption;
  }

  links.forEach((link, position) => {
    link.setAttribute('aria-haspopup', 'dialog');
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = link;
      show(position);
      dialog.showModal();
      document.documentElement.classList.add('photo-viewer-open');
      close.focus();
    });
  });
  close.addEventListener('click', () => dialog.close());
  previous.addEventListener('click', () => show(index - 1));
  next.addEventListener('click', () => show(index + 1));
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => {
    document.documentElement.classList.remove('photo-viewer-open');
    swipeStart = null;
    opener?.focus({ preventScroll: true });
  });
  dialog.addEventListener('keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    const moves = { ArrowLeft: index - 1, ArrowRight: index + 1, Home: 0, End: links.length - 1 };
    if (Object.hasOwn(moves, event.key)) { event.preventDefault(); show(moves[event.key]); }
    // Escape and modal focus containment are handled by the native dialog.
  });
  stage.addEventListener('pointerdown', event => {
    swipeStart = event.pointerType === 'touch' && event.isPrimary ? { x: event.clientX, y: event.clientY } : null;
  });
  stage.addEventListener('pointercancel', () => { swipeStart = null; });
  stage.addEventListener('pointerup', event => {
    if (!swipeStart) return;
    const dx = event.clientX - swipeStart.x;
    const dy = event.clientY - swipeStart.y;
    swipeStart = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 2) show(index + (dx < 0 ? 1 : -1));
  });
})();
