
  $(document).ready(function () {
    $("[data-agenda-search]").on("input", function () {
      const key = $(this).attr("data-agenda-search");

      // 1. Click the matching [data-agenda-show-all="{key}"] link
      const $link = $(`[data-agenda-show-all="${key}"]`);
      if ($link.length) {
        $link[0].click();
      } else {
        console.warn(`No link found for [data-agenda-show-all="${key}"]`);
      }

      // 2. Hide all elements with [data-agenda-show-all="btn-wrapper"]
      $(`[data-agenda-show-all="btn-wrapper"]`).css("display", "none");
    });
  });
