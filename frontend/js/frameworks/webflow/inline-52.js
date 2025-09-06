
  //Close modal when pressing the Esc key
  window.addEventListener('keyup', function(event) {
    if (event.which === 27) {
      wf_utils.signupModalUtils.closeModal();
    }
  });

  //Lock body scroll when nav is open
  window.addEventListener('DOMContentLoaded', (event) => {
    $('.brand-boilerplate-components--g-nav_menu-button, .w-nav-overlay').click(function() {
      if ($('body').css('overflow') !== 'hidden') {
        $('body').css('overflow', 'hidden');
      } else {
        $('body').css('overflow', 'auto');
      }
    });
  });

  // Global nav - Changes subnav height and width in a very flowy way
  window.onload = function() {
    $('.brand-boilerplate-components--g-nav_menu-dropdown_toggle').on('click', function () {
      const containerElement = $(this).next().find('.brand-boilerplate-components--g-nav_menu_container');

      setTimeout(function () {
        const containerWidth = containerElement.outerWidth();
        $('.brand-boilerplate-components--g-nav_menu-container-bg').width(containerWidth);

        const containerHeight = containerElement.outerHeight();
        $('.brand-boilerplate-components--g-nav_menu-container-bg').height(containerHeight);
      }, 50);
    });
  };

