
  $(document).ready(function () {
    // Function to load nested content based on data attributes
    function loadNestedContent(attribute, target, selector) {
      $("div[" + attribute + "]").each(function () {
        var slug = $(this).data(attribute.replace('data-', ''));
        $(this).load("https://webflow.com/webflowconf/session/" + slug + " " + target, function() {
        });
      });
    }
    loadNestedContent('data-nest-personas', '#nested-personas');
    loadNestedContent('data-nest-tracks', '#nested-tracks');
  });
