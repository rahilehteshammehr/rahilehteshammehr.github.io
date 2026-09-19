(() => {
  const root = document.documentElement;
  const theme = document.querySelector('.theme-toggle');
  const menu = document.querySelector('.menu-toggle');
  const links = document.querySelector('#site-links');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  let manualTheme = false;
  try { manualTheme = ['light', 'dark'].includes(localStorage.getItem('rahil-theme')); } catch (_) {}
  function syncTheme() {
    const label = `Switch to ${root.dataset.theme === 'dark' ? 'light' : 'dark'} theme`;
    theme.setAttribute('aria-label', label);
    theme.title = label;
    document.querySelectorAll('meta[name="theme-color"]').forEach(meta => {
      meta.content = root.dataset.theme === 'dark' ? '#30373e' : '#ffffff';
    });
  }
  theme.hidden = false;
  syncTheme();
  theme.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    manualTheme = true;
    try { localStorage.setItem('rahil-theme', root.dataset.theme); } catch (_) {}
    syncTheme();
  });
  systemTheme.addEventListener('change', event => {
    if (!manualTheme) {
      root.dataset.theme = event.matches ? 'dark' : 'light';
      syncTheme();
    }
  });
  window.addEventListener('storage', event => {
    if (event.key !== 'rahil-theme') return;
    manualTheme = ['light', 'dark'].includes(event.newValue);
    root.dataset.theme = manualTheme ? event.newValue : (systemTheme.matches ? 'dark' : 'light');
    syncTheme();
  });
  function setMenu(open, restoreFocus = false) {
    links.classList.toggle('is-open', open);
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    if (restoreFocus) menu.focus();
  }
  menu.hidden = false;
  menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') setMenu(false, true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-navigation')) setMenu(false);
  });
  window.matchMedia('(min-width: 761px)').addEventListener('change', event => {
    if (event.matches) setMenu(false);
  });
  const print = document.querySelector('.print-button');
  if (print) {
    print.hidden = false;
    print.addEventListener('click', () => window.print());
  }
})();
