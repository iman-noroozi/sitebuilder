
  $(function () {

    // Helper: Check if .autoplay-tabs is inside a visible .u-test-wrap
    function isInActiveTest($autoplayTabs) {
      var $testWrap = $autoplayTabs.closest('.u-test-wrap');
      if ($testWrap.length === 0) return false;
      return $testWrap.is(':visible');
    }

    // Main initialization logic for a single .autoplay-tabs instance
    function initAutoplayTabs($autoplayTabs) {
      // Prevent double-initialization
      if ($autoplayTabs.data('autoplay-initialized')) return;
      $autoplayTabs.data('autoplay-initialized', true);

      // Find the menu within this instance
      var $tabsMenu = $autoplayTabs.find('[tab-function="autoplay"], [tab-function="static"]');
      if ($tabsMenu.length === 0) return;

      // AUTOPLAY TABS
      $tabsMenu.filter('[tab-function="autoplay"]').each(function () {
        var $menu = $(this);
        var timing = parseInt($menu.attr('tab-timing'), 10);

        function autoplayTabs($menu) {
          var $activeTab = $menu.find('.autoplay-tabs_menu-item.cc-active');
          var $nextTab = $activeTab.next('.autoplay-tabs_menu-item');
          if ($nextTab.length === 0) {
            $nextTab = $menu.find('.autoplay-tabs_menu-item:first');
          }
          $nextTab.trigger('click');
        }

        function startTimer($menu, timing) {
          var interval = timing;
          var timer = setInterval(function () {
            autoplayTabs($menu);
          }, interval);
          $menu.data('timer', timer);
        }

        function resetTimer($menu, timing) {
          var timer = $menu.data('timer');
          clearInterval(timer);
          startTimer($menu, timing);
        }

        // Autoplay tab change
        $menu.find('.autoplay-tabs_menu-item').on('click', function () {
          $menu.find('.autoplay-tabs_menu-item').removeClass('cc-active');
          $(this).addClass('cc-active');
          resetTimer($menu, timing);
          $menu.find('.autoplay-tabs_progress-bar').stop().css({ width: '100%' });
          $(this).find('.autoplay-tabs_progress-bar').css({ width: 0 })
            .animate({ width: '100%' }, timing);
        });

        var startType = $menu.attr('tab-function-start');
        if (startType === 'scroll-into-view') {
          // Check if tabs are in view and start autoplay
          var options = {
            root: null,
            rootMargin: '0px',
            threshold: 0.5
          };

          var observer = new IntersectionObserver(function (entries, observer) {
            entries.forEach(function (entry) {
              if (entry.isIntersecting) {
                // Start timer and play active tab animation
                startTimer($menu, timing);
                $menu.find('.autoplay-tabs_menu-item.cc-active').find(
                  '.autoplay-tabs_progress-bar')
                  .css({ width: 0 })
                  .animate({ width: '100%' }, timing);

                observer.unobserve(entry.target);
              }
            });
          }, options);

          observer.observe($autoplayTabs[0]);
        } else {
          // Start autoplay on page load
          startTimer($menu, timing);
          $menu.find('.autoplay-tabs_menu-item.cc-active').find('.autoplay-tabs_progress-bar')
            .css({ width: 0 })
            .animate({ width: '100%' }, timing);
        }
      });

      // STATIC TABS
      $tabsMenu.filter('[tab-function="static"]').each(function () {
        var $menu = $(this);
        $menu.find('.autoplay-tabs_menu-item').on('click', function () {
          $menu.find('.autoplay-tabs_menu-item').removeClass('cc-active');
          $(this).addClass('cc-active');
        });
      });
    }

    // Observe .u-test-wrap visibility and initialize .autoplay-tabs when visible
    function observeVisibility($autoplayTabs) {
      var $testWrap = $autoplayTabs.closest('.u-test-wrap');
      if ($testWrap.length === 0) {
        // If not inside .u-test-wrap, initialize immediately
        initAutoplayTabs($autoplayTabs);
        return;
      }

      // If already visible, initialize immediately
      if ($testWrap.is(':visible')) {
        initAutoplayTabs($autoplayTabs);
        return;
      }

      // Otherwise, observe for visibility changes
      var observer = new MutationObserver(function() {
        if ($testWrap.is(':visible')) {
          initAutoplayTabs($autoplayTabs);
          observer.disconnect();
        }
      });

      observer.observe($testWrap[0], { attributes: true, attributeFilter: ['style', 'class'] });
    }

    // For each .autoplay-tabs instance, set up observer or initialize
    $('.autoplay-tabs').each(function () {
      observeVisibility($(this));
    });

  });
