
  //load and play video
  const whiteHeroVideo = document.querySelector('video[data-video="hero-2"]');
  const source = whiteHeroVideo.querySelector('source');
  source.setAttribute('src', source.getAttribute('data-src'));
  whiteHeroVideo.load();
  whiteHeroVideo.play();
