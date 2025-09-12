
	// Nav Active Check

document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.main-header');
    const menuItems = document.querySelectorAll('.e-n-menu-item');
    menuItems.forEach(item => {
      item.addEventListener('click', () => {
        header.classList.add('active');
      });
    });
    document.querySelector('.e-n-menu-toggle').addEventListener('click', () => {
        header.classList.toggle('active');
    });
    document.addEventListener('click', (e) => {
        if (e.target.className === 'e-n-menu-content e-active' ) {
            e.stopPropagation();
            header.classList.remove('active');
        }
        if (!header.contains(e.target)) {
            header.classList.remove('active');
        }
    });
});	
	
(function() {

	// Nav WPML language switcher script
  
	
    const toggleElement = document.querySelector('.dsm-nav-lang-desktop .wpml-ls-item-toggle');
    const subMenu = document.querySelector('.dsm-nav-lang-desktop .wpml-ls-sub-menu');
		const mobileToggle = document.querySelector('.dsm-nav .e-n-menu-item:has(#dsm-nav-lang)')

    // Check if submenu exists and has children
    if (!subMenu || subMenu.children.length === 0) {
        if (toggleElement) {
            toggleElement.style.display = 'none';
						mobileToggle.style.display = 'none';
        }
        return;
    }

    const clonedToggle = toggleElement.cloneNode(true);

    const svgElement = document.createElement('div');
    svgElement.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><path fill="currentColor" d="M12.323 2.255a9.749 9.749 0 0 1 8.172 4.958h.001A9.71 9.71 0 0 1 21.75 12l-.005.315a9.778 9.778 0 0 1-.303 2.125v.001a9.755 9.755 0 0 1-9.038 7.3L12 21.75a9.754 9.754 0 0 1-9.442-7.309v-.002A9.768 9.768 0 0 1 2.25 12c0-1.628.4-3.166 1.108-4.518l.146-.268A9.747 9.747 0 0 1 12 2.25l.323.005ZM9.061 17.02c.13.36.273.698.428 1.008.726 1.453 1.59 2.135 2.359 2.214l.152.008c.805 0 1.736-.673 2.51-2.222.156-.31.298-.647.428-1.006-.968.152-1.95.229-2.938.227v.001c-1 0-1.982-.08-2.94-.23Zm-4.409-1.267a8.253 8.253 0 0 0 3.965 3.77 8.615 8.615 0 0 1-.47-.824 11.826 11.826 0 0 1-.774-2.027 18.608 18.608 0 0 1-2.72-.92Zm14.695 0a18.66 18.66 0 0 1-2.721.92c-.211.738-.47 1.42-.774 2.026a8.598 8.598 0 0 1-.47.824 8.25 8.25 0 0 0 1.67-1 8.253 8.253 0 0 0 2.295-2.77ZM6.75 12c0-.627.03-1.243.09-1.84a12.739 12.739 0 0 1-2.424-1.413A8.222 8.222 0 0 0 3.75 12v.001c0 .589.063 1.175.187 1.75.97.514 1.993.938 3.061 1.26A18.106 18.106 0 0 1 6.75 12ZM12 3.75c-.805 0-1.736.673-2.51 2.222-.442.882-.792 1.979-1.006 3.218A11.24 11.24 0 0 0 12 9.75h.001l.505-.01a11.2 11.2 0 0 0 3.008-.552C15.3 7.95 14.95 6.853 14.51 5.972 13.736 4.422 12.805 3.75 12 3.75Zm-3.38.724a8.247 8.247 0 0 0-3.479 2.94c.597.46 1.241.863 1.925 1.197.24-1.24.609-2.365 1.081-3.31a8.62 8.62 0 0 1 .472-.827Zm6.76 0c.17.262.329.539.472.827.473.945.84 2.07 1.08 3.31a11.197 11.197 0 0 0 1.927-1.197 8.247 8.247 0 0 0-3.48-2.94ZM8.25 12c0 1.223.128 2.377.353 3.414 1.098.22 2.234.336 3.397.336h.001l.548-.008c.96-.029 1.912-.14 2.848-.328.224-1.037.353-2.191.353-3.414 0-.443-.017-.877-.049-1.3-1.191.361-2.437.55-3.701.549v.001c-1.288 0-2.53-.194-3.702-.55-.032.423-.048.857-.048 1.3Zm9 0c0 1.047-.088 2.06-.249 3.012a17.16 17.16 0 0 0 3.061-1.262A8.298 8.298 0 0 0 20.25 12v-.001l-.004-.266a8.208 8.208 0 0 0-.663-2.986 12.693 12.693 0 0 1-2.424 1.412c.06.598.091 1.213.091 1.841Z"/></svg>';

    toggleElement.appendChild(svgElement.firstElementChild);

    const newListItem = document.createElement('li');
    newListItem.className = 'wpml-ls-slot-shortcode_actions wpml-ls-item wpml-ls-item-nl';

    newListItem.appendChild(clonedToggle);
    subMenu.insertBefore(newListItem, subMenu.firstChild);


})();

