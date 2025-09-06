
  // Add reduced motion IX to <body>
  const observer = new MutationObserver(function (m, mo) {
    const body = document.body;
    if (body) {
      body.setAttribute("data-wf-ix-vacation", "1");
      mo.disconnect();
    }
  });

  observer.observe(document, {
    childList: true,
    subtree: true,
  });

	// Load all of this after the whole page (and jquery) has loaded
  window.onload = function() {

    // Set footer copyright year
    $('.brand-boilerplate-components--footer-copyright_year, .footer-copyright_year').text(new Date().getFullYear());

    // "Skip to main" script
    var skipLinkEle = document.getElementById('skip-link');
    if (skipLinkEle) {
      skipLinkEle.addEventListener('click keydown', function (e) {
        if (e.type === "keydown" && e.which !== 13) {
          return;
        }

        e.preventDefault();
        var target = document.getElementById('main');
        target.setAttribute('tabindex', '-1');
        target.focus();
      });
    }

    // Trap modal focus and enable ESC key for accessibility
    var buttonThatOpenedModal;
    var findModal = function (elem) {
      var tabbable = elem.find('select, input, textarea, button, a').filter(':visible');
      var firstTabbable = tabbable.first();
      var lastTabbable = tabbable.last();

      firstTabbable.focus();

      lastTabbable.on('keydown', function (e) {
        if ((e.which === 9 && !e.shiftKey)) {
          e.preventDefault();
          firstTabbable.focus();
        }
      });

      firstTabbable.on('keydown', function (e) {
        if ((e.which === 9 && e.shiftKey)) {
          e.preventDefault();
          lastTabbable.focus();
        }
      });

      elem.on('keydown', function (e) {
        if (e.keyCode === 27) {
          $(elem).find('[class$="modal-close_btn"]').click();
        };
      });
    };

    var modalOpenButton = $('[class$="modal-open_btn"]');
    modalOpenButton.on('keydown', function (e) {
      if (e.which !== 13 && e.which !== 32) {
        return;
      }

      e.preventDefault();
      var evt = document.createEvent("MouseEvents");
      evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
      $(this).get(0).dispatchEvent(evt);
    });
    modalOpenButton.on('click', function () {
      $(this).next().show();
      findModal($(this).next());
      buttonThatOpenedModal = $(this);
    });

    var modalCloseButton = $('[class$="modal-close_btn"], [class$="modal-close_area"]');
    modalCloseButton.on('keydown', function (e) {
      if (e.which !== 13 && e.which !== 32) {
        return;
      }

      e.preventDefault();
      var evt = document.createEvent("MouseEvents");
      evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
      $(this).get(0).dispatchEvent(evt);
    });
    modalCloseButton.on('click', function () {
      $(this).closest('[class$="modal-wrapper"]').hide();
      if (buttonThatOpenedModal) {
        buttonThatOpenedModal.focus();
        buttonThatOpenedModal = null;
      }
    });

    // Toggle accordion attributes for accessibility
    var accordionToggleButton = $('.accordion-trigger');
    accordionToggleButton.on('keydown', function (e) {
      if (e.which !== 13 && e.which !== 32) {
        return;
      }
      e.preventDefault();

      var evt = document.createEvent("MouseEvents");
      evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
      $(this).get(0).dispatchEvent(evt);
    });

    accordionToggleButton.on('click', function (e) {
      $(this).toggleAttrVal('aria-expanded', "false", "true");
      $(this).parent().find('.accordion-content').toggleAttrVal('aria-hidden', "true", "false");
    });

    // jQuery method to toggle attribute value
    $.fn.toggleAttrVal = function (attr, val1, val2) {
      var test = $(this).attr(attr);
      if (test === val1) {
        $(this).attr(attr, val2);
        return this;
      }
      if (test === val2) {
        $(this).attr(attr, val1);
        return this;
      }
      $(this).attr(attr, val1);
      return this;
    };
  };
