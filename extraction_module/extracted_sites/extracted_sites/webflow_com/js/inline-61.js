

  document.addEventListener("DOMContentLoaded", (event) => {
    // --- Accessibility: Check for prefers-reduced-motion ---
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (prefersReducedMotion) {
      console.log(
        "User prefers reduced motion. Videos will not be loaded or played."
      );
    }

    // --- Remove desktop-only videos on small screens ---
    function removeDesktopOnlyVideos() {
      if (window.innerWidth <= 991) {
        document
          .querySelectorAll('video[data-video-playback="desktop-only"]')
          .forEach((video) => {
          video.remove();
        });
      }
    }

    removeDesktopOnlyVideos();

    // ------------------------------------------------------------
    // --- Video lazy loading -------------------------------------
    // ------------------------------------------------------------

    const videos = document.querySelectorAll("video[data-video]");

    const observerOptions = {
      root: null,
      rootMargin: "300px",
      threshold: 0,
    };

    // Lazy load videos when they intersect
    const videoObserverCallback = (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const video = entry.target;
          lazyLoadVideo(video)
            .then(() => observer.unobserve(video)) // Stop observing after load
            .catch(console.error);
        }
      });
    };

    // Initialize IntersectionObserver
    const videoObserver = new IntersectionObserver(
      videoObserverCallback,
      observerOptions
    );

    const lazyLoadVideo = (video) => {
      return new Promise((resolve, reject) => {
        const source = video.querySelector("source[data-src]");
        if (source && !source.src) {
          source.src = source.getAttribute("data-src");
          video.load();

          video.addEventListener("canplaythrough", function onCanPlayThrough() {
            video.removeEventListener("canplaythrough", onCanPlayThrough);
            resolve();
          });

          video.addEventListener("error", function onError() {
            video.removeEventListener("error", onError);
            reject(new Error(`Error loading video: ${source.src}`));
          });
        } else {
          resolve(); // Already loaded or source missing
        }
      });
    };

    // Start observing videos for lazy loading
    videos.forEach((video) => videoObserver.observe(video));

    // ----------------------------------------------------------------
    // --- Video play/pause buttons -----------------------------------
    // ----------------------------------------------------------------

    const handlePlaybackButtons = (video) => {
      const videoPlaybackType = video.getAttribute("data-video-playback");

      // Find container and buttons
      const playbackPosition = document
      .querySelector(
        `.features_video-playback-position [data-video="${video.getAttribute(
          "data-video"
        )}"]`
      )
      ?.closest(".features_video-playback-position");
      if (!playbackPosition) return; // Safety check

      const playButton = playbackPosition.querySelector(
        '[data-video-playback="play"]'
      );
      const pauseButton = playbackPosition.querySelector(
        '[data-video-playback="pause"]'
      );
      if (!playButton || !pauseButton) return;

      // Helper function to toggle button visibility
      const toggleButtonVisibility = (isPlaying) => {
        playButton.style.display = isPlaying ? "none" : "flex";
        pauseButton.style.display = isPlaying ? "flex" : "none";
      };

      // Set initial button state
      toggleButtonVisibility(!video.paused);

      // Event listener for play button
      playButton.addEventListener("click", async (event) => {
        event.stopPropagation();
        try {
          await lazyLoadVideo(video, true);
          video.play();
          toggleButtonVisibility(true);
        } catch (error) {
          console.error(error);
        }
      });

      // Event listener for pause button
      pauseButton.addEventListener("click", (event) => {
        event.stopPropagation();
        video.pause();
        toggleButtonVisibility(false);
      });

      // Sync button state with video play/pause events
      video.addEventListener("play", () => toggleButtonVisibility(true));
      video.addEventListener("pause", () => toggleButtonVisibility(false));
    };

    // Scroll-triggered video play
    const handleScrollTrigger = (video, trigger) => {
      const triggerType = trigger.getAttribute("data-video-trigger");

      const observer = new IntersectionObserver(
        async (entries) => {
          entries.forEach(async (entry) => {
            if (entry.isIntersecting) {
              try {
                // Always lazy load the video
                await lazyLoadVideo(video, true);

                // If reduced motion is preferred, don't play the video, just show the poster
                if (!prefersReducedMotion) {
                  video.currentTime = 0;
                  video.play();
                }

                // Only unobserve if it's not a scroll-in trigger
                if (triggerType !== "scroll-in") {
                  observer.unobserve(trigger);
                }
              } catch (error) {
                console.error(error);
              }
            } else if (triggerType === "scroll-in") {
              // Only pause on scroll out if it's a scroll-in trigger
              video.pause();
            }
          });
        },
        { threshold: 0.5 }
      );

      observer.observe(trigger);
    };

    // Iterate over each video element and handle controls
    videos.forEach((video) => {
      if (prefersReducedMotion) {
        video.pause(); // Ensure all videos are paused if reduced motion is preferred
      } else {
        videoObserver.observe(video); // Observe videos for lazy loading
      }

      // Initialize play/pause button handling
      handlePlaybackButtons(video);

      // Handle scroll/tab triggers
      const videoId = video.getAttribute("data-video");
      const trigger = document.querySelector(
        `[data-video="${videoId}"][data-video-trigger]`
      );

      if (trigger) {
        const triggerType = trigger.getAttribute("data-video-trigger");
        if (triggerType === "tab" || triggerType === "scroll-in") {
          handleScrollTrigger(video, trigger);
        }
      }
    });

    // ----------------------------------------------------------------
    // --- Autoplay Feature Tabs --------------------------------------
    // ----------------------------------------------------------------

    document.querySelectorAll(".feature-tabs_menu").forEach((tabsMenu) => {
      if (prefersReducedMotion) {
        console.log(
          "Autoplay feature tabs disabled due to reduced motion preference."
        );
        return;
      }

      let tabTimeout;
      const INTERVAL = 10000;

      function handleTabChange(newActiveTab) {
        clearTimeout(tabTimeout);
        resetTabTimers(tabsMenu);

        const timerBar = newActiveTab.querySelector(".feature-tabs_bar-timer");
        animateTimerBar(timerBar);

        const videoId = newActiveTab.getAttribute("data-video");
        const video = document.querySelector(`video[data-video="${videoId}"]`);
        if (video) {
          video.currentTime = 0;
          video.play();
        }

        tabTimeout = setTimeout(moveToNextTab, INTERVAL);
      }

      function moveToNextTab() {
        if (
          document.querySelector(".w-nav-button").classList.contains("w--open")
        ) {
          tabTimeout = setTimeout(moveToNextTab, INTERVAL);
          return;
        }

        const current = tabsMenu.querySelector(".feature-tabs_link.w--current");
        const next =
              current?.nextElementSibling ||
              tabsMenu.querySelector(".feature-tabs_link:first-of-type");

        if (next) {
          next.removeAttribute("href");
          next.click();
        }
      }

      function resetTabTimers(tabsMenu) {
        tabsMenu.querySelectorAll(".feature-tabs_bar-timer").forEach((timer) => {
          timer.style.transition = "none";
          timer.style.height = "0%";
        });
      }

      function animateTimerBar(timerBar) {
        timerBar.style.transition = "none";
        timerBar.style.height = "0%";
        void timerBar.offsetHeight; // Force reflow
        timerBar.style.transition = "height 10s linear";
        timerBar.style.height = "100%";
      }

      const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
          if (
            mutation.type === "attributes" &&
            mutation.attributeName === "class" &&
            mutation.target.classList.contains("w--current")
          ) {
            handleTabChange(mutation.target);
            break;
          }
        }
      });

      tabsMenu.querySelectorAll(".feature-tabs_link").forEach((tab) => {
        observer.observe(tab, { attributes: true, attributeFilter: ["class"] });
      });

      const intersectionObserver = new IntersectionObserver(
        (entries) => {
          const isIntersecting = entries[0].isIntersecting;
          if (isIntersecting) {
            // Start the autoplay when the tabs come into view
            const currentTab = tabsMenu.querySelector(
              ".feature-tabs_link.w--current"
            );
            if (currentTab) {
              handleTabChange(currentTab);
            } else {
              moveToNextTab();
            }
          } else {
            clearTimeout(tabTimeout);
            resetTabTimers(tabsMenu);
          }
        },
        { threshold: 0.1 }
      );

      intersectionObserver.observe(tabsMenu);
    });

    // ----------------------------------------------------------------
    // --- Customers Accordion Slider ---------------------------------
    // ----------------------------------------------------------------

    const transitionDuration = 800; // Duration of CSS transition in milliseconds
    let isTransitioning = false;
    let isFirstLoad = true;
    let lastInteractionWasKeyboard = false;

    const isMobileDevice = () =>
    typeof window.orientation !== "undefined" ||
          navigator.userAgent.indexOf("IEMobile") !== -1;

    const toggleFocusableElements = (slide, enable) => {
      const focusableSelectors =
            'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])';
      slide.querySelectorAll(focusableSelectors).forEach((el) => {
        if (enable) {
          const originalTabindex = el.getAttribute("data-original-tabindex");
          if (originalTabindex !== null) {
            originalTabindex === ""
              ? el.removeAttribute("tabindex")
            : el.setAttribute("tabindex", originalTabindex);
            el.removeAttribute("data-original-tabindex");
          }
          el.disabled = false;
        } else {
          if (!el.hasAttribute("data-original-tabindex")) {
            el.setAttribute(
              "data-original-tabindex",
              el.getAttribute("tabindex") || ""
            );
          }
          el.setAttribute("tabindex", "-1");
          el.disabled = true;
        }
      });
    };

    const updateSliderPosition = async () => {
      const slides = Array.from(
        document.querySelectorAll(".customers-slider_slide")
      );
      const activeSlide = document.querySelector(
        ".customers-slider_slide.cc-active"
      );
      const activeIndex = slides.indexOf(activeSlide);

      document.querySelector(
        ".customers-slider"
      ).style.transform = `translateX(-${(5 + 1) * activeIndex}rem)`;

      slides.forEach(async (slide) => {
        const isActive = slide === activeSlide;
        slide.setAttribute("aria-hidden", !isActive);
        toggleFocusableElements(slide, isActive);

        const video = slide.querySelector("video");
        if (video) {
          if (isActive && !prefersReducedMotion) {
            try {
              await lazyLoadVideo(video, true);
              video.play();
            } catch (error) {
              console.error(error);
            }
          } else {
            video.pause();
          }
        }
      });

      activeSlide.setAttribute("aria-hidden", "false");

      if (!isFirstLoad && !isMobileDevice() && lastInteractionWasKeyboard) {
        setTimeout(() => {
          activeSlide.focus();
        }, transitionDuration); // Use transitionDuration for the focus delay
      }
    };

    const goToSlide = (nextSlide) => {
      if (isTransitioning) return;
      isTransitioning = true;
      isFirstLoad = false;

      document
        .querySelector(".customers-slider_slide.cc-active")
        .classList.remove("cc-active");
      nextSlide.classList.add("cc-active");

      updateSliderPosition();

      setTimeout(() => {
        isTransitioning = false;
      }, transitionDuration);
    };

    const getAdjacentSlide = (direction) => {
      const slides = Array.from(
        document.querySelectorAll(".customers-slider_slide")
      );
      const currentIndex = slides.findIndex((slide) =>
                                            slide.classList.contains("cc-active")
                                           );
      const newIndex = (currentIndex + direction + slides.length) % slides.length;
      return slides[newIndex];
    };

    document.querySelectorAll(".customers-slider_slide").forEach((slide) => {
      slide.addEventListener("keydown", (e) => {
        if (slide.classList.contains("cc-active")) {
          if (e.key === "ArrowRight") {
            lastInteractionWasKeyboard = true;
            goToSlide(getAdjacentSlide(1));
          }
          if (e.key === "ArrowLeft") {
            lastInteractionWasKeyboard = true;
            goToSlide(getAdjacentSlide(-1));
          }
        }
        if (
          (e.key === "Enter" || e.key === " ") &&
          !slide.classList.contains("cc-active")
        ) {
          lastInteractionWasKeyboard = true;
          goToSlide(slide);
        }
      });

      slide.addEventListener("click", () => {
        lastInteractionWasKeyboard = false;
        if (!isTransitioning) goToSlide(slide);
      });
    });

    document
      .getElementById("customers-accordion-right")
      .addEventListener("click", () => {
      lastInteractionWasKeyboard = false;
      goToSlide(getAdjacentSlide(1));
    });
    document
      .getElementById("customers-accordion-left")
      .addEventListener("click", () => {
      lastInteractionWasKeyboard = false;
      goToSlide(getAdjacentSlide(-1));
    });

    updateSliderPosition(); // Initialize slider position
  });
