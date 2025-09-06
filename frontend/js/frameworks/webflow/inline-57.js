
  // Wait for the DOM to be fully loaded before executing
  document.addEventListener('DOMContentLoaded', function() {
    // Check if the current URL contains either "webflow.io" or "markup.io"
    if (window.location.href.includes("webflow.io") || window.location.href.includes("markup.io")) {
      // Find all anchor elements on the page
      const anchorElements = document.querySelectorAll('a');

      // Process each anchor element
      anchorElements.forEach(anchor => {
        const href = anchor.getAttribute('href');

        // Skip if there's no href attribute
        if (!href) return;

        // Create a pattern to match "webflowconf/" in the middle of a URL
        // This will match the directory whether it's after domain or in the middle of the path
        const pattern = /([^\/])(\/webflowconf\/)([^\/])/g;

        // Replace the pattern if found, preserving the characters before and after
        const updatedHref = href.replace(pattern, '$1/$3');

        // Alternative pattern to catch webflowconf/ at the beginning of the path or end of the path
        const startPattern = /^\/webflowconf\//;
        const endPattern = /\/webflowconf\/$/;

        // Apply additional replacements if needed
        let finalHref = updatedHref
        .replace(startPattern, '/')
        .replace(endPattern, '/');

        // Update the href attribute if it was changed
        if (finalHref !== href) {
          anchor.setAttribute('href', finalHref);
        }
      });
    }
  });
