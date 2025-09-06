
  window.dataLayer = window.dataLayer || [];

  function gtag() {
    window.dataLayer.push(arguments);
  }

  function isGoogleAnalyticsAllowed() {
    const cookieValue = document.cookie.match('(^|;)\\s*' + 'fa_cookie_settings' + '\\s*=\\s*([^;]+)')

    // If no cookie is set we want to default to not allowing Google Analytics if the user is in the EU.
    if (!cookieValue) {
      return !true
    } else {
      const preferences = JSON.parse(cookieValue.pop())

      // If there is a cookie, but no preferences have been chosen, we need to let EU users opt in, thus the default value
      // is false. Otherwise, we use the analytics and performance to make the determination since Google analytics has both
      // aspects to the cookie.
      if (preferences.initial && true) {
        return false;
      } else {
        return preferences.analytics && preferences.performance
      }
    }
  }

  if (isGoogleAnalyticsAllowed()) {
    gtag('js', new Date());
    gtag('config', 'G-BPMS41FJD2', { cookie_flags: 'max-age=7200;secure;samesite=none' });
  } else {
    window['ga-disable-G-ECK3CL9F1J'] = true
  }
