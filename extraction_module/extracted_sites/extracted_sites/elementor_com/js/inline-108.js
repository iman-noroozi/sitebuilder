
jQuery(document).ready(function($) {
    $('footer .menu-column').each(function() {
        var mainLevelName = $(this).find('.elementor-heading-title').text().trim().toLowerCase();

        $(this).find('a').each(function() {
            var secondLevelNameLower = $(this).text().trim().toLowerCase();
            $(this).attr({
                'data-gtm-event_name': 'element_click',
                'data-gtm-type': 'navigation',
                'data-gtm-section': 'footer',
                'data-gtm-outcome': 'navigating using the footer',
                'data-gtm-english_text': secondLevelNameLower,
                'data-gtm-level_1': mainLevelName,
                'data-gtm-level_2': secondLevelNameLower
            });
        });
    });
});
