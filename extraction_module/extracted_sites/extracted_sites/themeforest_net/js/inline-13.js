
//<![CDATA[
  (function() {
    function normalizeAttributeValue(value) {
      if (value === undefined) return undefined
      if (value === null) return undefined

      let normalizedValue

      if (Array.isArray(value)) {
        normalizedValue = normalizedValue || value
          .map(normalizeAttributeValue)
          .filter(Boolean)
          .join(', ')
      }

      normalizedValue = normalizedValue || value
        .toString()
        .toLowerCase()
        .trim()
        .replace(/&amp;/g, '&')
        .replace(/&#39;/g, "'")
        .replace(/\s+/g, ' ')

      if (normalizedValue === '') return undefined
      return normalizedValue
    }

    function parseSignedInUserIdsFromCookie() {
      if (!document.cookie) return { envatoId: undefined, marketId: undefined };

      var prefix = "statistics_info=";
      var cookie = document.cookie.split('; ').find(function(part) {
        return part.startsWith(prefix);
      })

      if (cookie === undefined) return { envatoId: undefined, marketId: undefined };

      var ids = decodeURIComponent(cookie.substring(prefix.length)).split(":");

      return { envatoId: ids[0], marketId: ids[1] };
    }

    if (document.documentElement.hasAttribute('data-turbo-preview')) return

    window.dataLayer = window.dataLayer || [];

    var gaParam = (new URL(window.location)).searchParams.get("_ga")
    var signedInUserIds = parseSignedInUserIdsFromCookie();
    var categoryAttributes = JSON.parse('{}');
    var pageAttributes = {
      app_name: normalizeAttributeValue('market-storefront'),
      app_env: normalizeAttributeValue('production'),
      app_version: normalizeAttributeValue('0349d0dd664af9a6f8b6427cd66849574327f504'),
      page_type: normalizeAttributeValue('home'),
      page_location: window.location.href,
      page_referrer: document.referrer,
      page_title: document.title,
      ga_param: normalizeAttributeValue(gaParam ? '_ga='+gaParam : undefined),
      event_attributes: null,
      user_attributes: {
        user_id: normalizeAttributeValue(signedInUserIds.envatoId),
        market_user_id: normalizeAttributeValue(signedInUserIds.marketId),
      },
      ...categoryAttributes
    };
    dataLayer.push(pageAttributes)

    dataLayer.push({
      event: 'analytics_ready',
      event_attributes: {
        event_type: 'user',
        custom_timestamp: Date.now()
      }
    })
  })();

//]]>
