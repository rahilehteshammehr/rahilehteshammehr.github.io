// Apply before CSS paints. Default to the visitor's system theme.
(() => {
  let saved;
  try { saved = localStorage.getItem('rahil-theme'); } catch (_) {}
  const dark = saved === 'dark' || (saved !== 'light' && window.matchMedia('(prefers-color-scheme: dark)').matches);
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  document.documentElement.classList.replace('no-js', 'js');
})();
