
  document.querySelectorAll('[data-speaker-company-name] a').forEach(function (link) {
    link.setAttribute('target', '_blank');
    link.setAttribute('rel', 'noopener noreferrer');
  });
