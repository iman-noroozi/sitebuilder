(function() {
try {
  let colorScheme = '';
  const mode = localStorage.getItem('joy-mode') || 'system';
  const dark = localStorage.getItem('joy-color-scheme-dark') || 'dark';
  const light = localStorage.getItem('joy-color-scheme-light') || 'light';
  if (mode === 'system') {
    // handle system mode
    const mql = window.matchMedia('(prefers-color-scheme: dark)');
    if (mql.matches) {
      colorScheme = dark
    } else {
      colorScheme = light
    }
  }
  if (mode === 'light') {
    colorScheme = light;
  }
  if (mode === 'dark') {
    colorScheme = dark;
  }
  if (colorScheme) {
    document.documentElement.setAttribute('data-joy-color-scheme', colorScheme);
  }
} catch(e){}})();