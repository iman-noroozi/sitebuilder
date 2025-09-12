
  $(function() {
    // Click tab when clicking corresponding nav button
    $('#nav-sep-16').on('click', function(evt) {
      $('.agenda_tab-link').removeClass("cc-current");
      $(this).addClass("cc-current");
      $('#tab-sep-16').triggerHandler('click');
      // Toggle filter visibility
      $('[data-filter-sept-16]').css('display', 'flex');
      $('[data-filter-sept-17]').css('display', 'none');
      $('[data-filter-sept-18]').css('display', 'none');
    });
    $('#nav-sep-17').on('click', function(evt) {
      $('.agenda_tab-link').removeClass("cc-current");
      $(this).addClass("cc-current");
      $('#tab-sep-17').triggerHandler('click');
      // Toggle filter visibility
      $('[data-filter-sept-16]').css('display', 'none');
      $('[data-filter-sept-17]').css('display', 'flex');
      $('[data-filter-sept-18]').css('display', 'none');
    });
    $('#nav-sep-18').on('click', function(evt) {
      $('.agenda_tab-link').removeClass("cc-current");
      $(this).addClass("cc-current");
      $('#tab-sep-18').triggerHandler('click');
      // Toggle filter visibility
      $('[data-filter-sept-16]').css('display', 'none');
      $('[data-filter-sept-17]').css('display', 'none');
      $('[data-filter-sept-18]').css('display', 'flex');
    });
    // Sync nav state when tabs are triggered
    $('#tab-sep-16').on('click', function(evt) {
      $('.agenda_tab-link').removeClass("cc-current");
      $('#nav-sep-16').addClass("cc-current");
    });
    $('#tab-sep-17').on('click', function(evt) {
      $('.agenda_tab-link').removeClass("cc-current");
      $('#nav-sep-17').addClass("cc-current");
    });
    $('#tab-sep-18').on('click', function(evt) {
      $('.agenda_tab-link').removeClass("cc-current");
      $('#nav-sep-18').addClass("cc-current");
    });
  });
