
  document.addEventListener('DOMContentLoaded', function () {
    const speakerNamesSlider = new Swiper('#speaker-names-slider', {
      effect: 'fade',
      loop: true,
      loopAdditionalSlides: 1,
      fadeEffect: {
        crossFade: true,
      },
      speed: 500,
      allowTouchMove: false, // Prevent direct interaction with this slider
    });

    const speakerImageSlider = new Swiper('#speaker-imgs-slider', {
      loop: true,
      loopAdditionalSlides: 1,
      slidesPerView: 1,
      spaceBetween: 20,
      keyboard: true,
      grabCursor: true,
      speed: 500,
      navigation: {
        nextEl: "#speaker-slider-right",
        prevEl: "#speaker-slider-left",
      },
      breakpoints: {
        640: {
          slidesPerView: 1,
        },
        768: {
          slidesPerView: 1,
        },
        1024: {
          slidesPerView: 2.5,
        },
      },
    });

    // Use events to synchronize sliders instead of bidirectional controller
    speakerImageSlider.on('slideChange', function () {
      speakerNamesSlider.slideTo(speakerImageSlider.realIndex);
    });
  });
