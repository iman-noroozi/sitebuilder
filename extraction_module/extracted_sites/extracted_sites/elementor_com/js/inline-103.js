
document.addEventListener('DOMContentLoaded', function () {
	
	// Bottom Sticky Nav
	
	  const stickyNavLinks = document.querySelectorAll('.bottom-sticky-nav .elementor-item');
	
    stickyNavLinks.forEach(link => {
        const linkName = link.textContent.toLowerCase().trim();
        link.setAttribute('data-gtm-event_name', 'element_click');
        link.setAttribute('data-gtm-type', 'ui');
        link.setAttribute('data-gtm-section', 'everything you need');
			  link.setAttribute('data-gtm-element_name', 'more info buttons');
			  link.setAttribute('data-gtm-outcome', 'go to ' + linkName + ' area');
        link.setAttribute('data-gtm-english_text', linkName);
    });
	
	// Build - Tabs
	
	  const buildTabs = document.querySelectorAll('.dsm-tabs--side .e-n-tab-title');
	
    buildTabs.forEach(tab => {
        const tabTitle = tab.querySelector('.e-n-tab-title-text b').textContent.toLowerCase().trim();
        tab.setAttribute('data-gtm-event_name', 'element_click');
        tab.setAttribute('data-gtm-type', 'ui');
        tab.setAttribute('data-gtm-section', 'builder section');
			  tab.setAttribute('data-gtm-element_name', 'feature description');
			  tab.setAttribute('data-gtm-outcome', 'clicking feature description');
        tab.setAttribute('data-gtm-english_text', tabTitle);
    });
	
	
	// Carousel Arrows
	
	  const carouselButtons = document.querySelectorAll('.elementor-swiper-button');
	
    carouselButtons.forEach(button => {
				const arrowDirection = button.classList.contains('elementor-swiper-button-next') ? 'forward' : 'backward';
        button.setAttribute('data-gtm-event_name', 'element_click');
        button.setAttribute('data-gtm-type', 'ui');
        button.setAttribute('data-gtm-section', 'carousel');
			  button.setAttribute('data-gtm-element_name', 'arrows');
			  button.setAttribute('data-gtm-outcome', arrowDirection);
    });
	
	
	
		// Resources Cards
	
    const learnMoreCards = document.querySelectorAll('.learn-more-cards .elementor-cta');
	
    learnMoreCards.forEach(card => {
        const cardName = card.querySelector('.elementor-cta__title').textContent.toLowerCase().trim();
        card.setAttribute('data-gtm-event_name', 'element_click');
        card.setAttribute('data-gtm-type', 'ui');
        card.setAttribute('data-gtm-section', 'helpful articles');
			  card.setAttribute('data-gtm-element_name', 'card click');
			  card.setAttribute('data-gtm-outcome', 'proceeding to ' + cardName);
        card.setAttribute('data-gtm-level_1', cardName);
    });
	
});
