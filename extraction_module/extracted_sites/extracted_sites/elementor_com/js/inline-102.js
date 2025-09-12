

document.addEventListener('DOMContentLoaded', function() {
const tabTitles = document.querySelectorAll('.dsm-tabs--top .e-n-tab-title');
const videoContainers = document.querySelectorAll('.dsm-tabs--top .e-n-tabs-content > div');

let activeIndex = 0;

tabTitles.forEach(tabTitle => {
    const progressBar = document.createElement('span');
    progressBar.classList.add('progress-bar');
    tabTitle.appendChild(progressBar);

    const tabTitleName = tabTitle.querySelector('.e-n-tab-title-text b').textContent.toLowerCase().trim();
    tabTitle.setAttribute('data-gtm-event_name', 'element_click');
    tabTitle.setAttribute('data-gtm-type', 'ui');
    tabTitle.setAttribute('data-gtm-section', 'hero');
    tabTitle.setAttribute('data-gtm-outcome', 'change video');
    tabTitle.setAttribute('data-gtm-english_text', tabTitleName);
});

function smoothScroll(element, target, duration) {
    const start = element.scrollLeft;
    const change = target - start;
    const startTime = performance.now();
    
    function animation(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const easeProgress = progress < .5 ? 
            4 * progress * progress * progress : 
            1 - Math.pow(-2 * progress + 2, 3) / 2;
        
        element.scrollLeft = start + (change * easeProgress);
        
        if (progress < 1) {
            requestAnimationFrame(animation);
        }
    }
    
    requestAnimationFrame(animation);
}

function setActiveTab(index) {
    tabTitles.forEach(tabTitle => {
        tabTitle.setAttribute('aria-selected', 'false');
        tabTitle.setAttribute('tabindex', '-1');
        tabTitle.querySelector('.progress-bar').classList.remove('active');
    });
    videoContainers.forEach(container => container.classList.remove('e-active'));

    tabTitles[index].setAttribute('aria-selected', 'true');
    tabTitles[index].setAttribute('tabindex', '0');
    tabTitles[index].querySelector('.progress-bar').classList.add('active');
    videoContainers[index].classList.add('e-active');

    const activeVideo = videoContainers[index].querySelector('video');
    if (activeVideo) {
        activeVideo.currentTime = 0;
    }

    activeIndex = index;

    updateProgressBar();
}

function updateProgressBar() {
    const activeVideo = videoContainers[activeIndex].querySelector('video');
    if (!activeVideo) return;

    const activeProgressBar = tabTitles[activeIndex].querySelector('.progress-bar.active');
    if (!activeProgressBar) return;

    const progress = (activeVideo.currentTime / activeVideo.duration) * 100;
    activeProgressBar.style.width = `${progress}%`;
    requestAnimationFrame(updateProgressBar);
}

videoContainers.forEach((container, index) => {
    const video = container.querySelector('video');
    if (video) {
        video.addEventListener('ended', () => {
            if (video.currentTime === video.duration) {
                const nextIndex = (index + 1) % tabTitles.length;
                setActiveTab(nextIndex);
            }
        });
    }
});

setActiveTab(activeIndex);

updateProgressBar();

tabTitles.forEach(tabTitle => {
    tabTitle.addEventListener('click', function() {
        const clickedIndex = Array.from(tabTitles).indexOf(this);
        setActiveTab(clickedIndex);
    });
});

// Play / Pause Video
const videoWrappers = document.querySelectorAll('.dsm-tabs--top .dsm-video-wrapper');

videoWrappers.forEach(wrapper => {
    const video = wrapper.querySelector('.elementor-video');
    const control = wrapper.querySelector('.dsm-video-control');
    
    control.addEventListener('click', function() {
        if (video.paused) {
            video.play();
            this.classList.remove('pause');
        } else {
            video.pause();
            this.classList.add('pause');
        }
    });
});

// Safari Fallback
const canPlayType = document.createElement("video").canPlayType('video/webm; codecs="vp8, vorbis"');
document.querySelectorAll("video").forEach(video => {
    if (!canPlayType) {
        const parent = video.closest(".elementor-widget-video");
        if (!parent) return;

        const mp4Src = parent.getAttribute("safari-src");
        if (!mp4Src) return;

        video.setAttribute('src', mp4Src);
    }
});
});

	
	// ----- GSAP -----

	
    gsap.registerPlugin(ScrollTrigger,SplitText);
	
	
	// Text Split

	const textSplit = new SplitText('.text-split .elementor-heading-title', {type: 'words, chars'});
	
	gsap.from(textSplit.chars, {
				opacity: 0.2,
				stagger: 0.2,
				scrollTrigger: {
					trigger: '#host',
					start: 'top 40%',
					end: '+=100vh',
					scrub: 1,
					fastScrollEnd: true
			}
	});
	
	
	// Sticky Nav

	const stickyNav = document.querySelector('.bottom-sticky-nav');

	ScrollTrigger.create({
			trigger: stickyNav,
			start: '70px bottom',
			endTrigger: '.features-wrapper',
			end: 'top bottom',
			onEnter: () => stickyNav.classList.add('fixed'),
			onLeave: () => gsap.to(stickyNav, {yPercent: 130, duration: 0.2}),
			onEnterBack: () => gsap.to(stickyNav, {yPercent: 0, ease: 'back.in'}),
			onLeaveBack: () => stickyNav.classList.remove('fixed'),
			invalidateOnRefresh: true
	});
	
	
	// Features Section

	
	document.addEventListener('DOMContentLoaded', () => {

		const featureImages = gsap.utils.toArray('.feature-img');

		const targetCoords = [
				{ xPercent: 168, yPercent: -40 }, 
				{ xPercent: 68, yPercent: -108 },
				{ xPercent: -40, yPercent: -108 },
				{ xPercent: -140, yPercent: 0 },
				{ xPercent: -16, yPercent: 90 },
				{ xPercent: 140, yPercent: 52 }
			];

		featureImages.forEach((element, index) => {
				// Set initial positions
				gsap.set(element, { xPercent: targetCoords[index].xPercent, yPercent: targetCoords[index].yPercent });
		});

		let featuresTl = gsap.timeline({ paused: true });

		featuresTl.from(featureImages, { xPercent: 0, yPercent: 0, duration: 1, stagger: 0.2, ease: 'none' })
							.from('.features-title', {yPercent: -240, duration: 1.5}, 0)
							.set('.features-btn', {zIndex: 10}, '>-0.05')

		ScrollTrigger.create({
			trigger: '.features-wrapper',
			start: 'top 50%',
			end: 'bottom 100%',
			animation: featuresTl,
			scrub: true
		});
	});
	
	
	// Resources Section

	gsap.to('#resources', {
		borderRadius: 0,
		ease: 'none',
		scrollTrigger: {
			trigger: '#resources',
			start: 'bottom +=50%',
			end: '+=200px',
			scrub: true
		}
	})

