
  //-- Amplitude initialize
  wf_analytics.init({
    pageView: {
      name: 'Website Viewed',
      data: {
        redirect: false // not a redirect to dashboard
      }
    },
    trackScroll: true,
    page: 'website'
  });

  // ---- Custom intellimize audiences ----
  // User is logged in/out
  intellimize.ready(() => {
    wf_utils.getUser((user) => {
      const isLoggedIn = user ? 'true' : 'false';
      const scope = 'user'; // or 'pageview'
      const attributes = { loggedIn: isLoggedIn };

      intellimize.setAttributes(scope, attributes);
    });
  });
  // User device type (mac, pc, etc.)
  intellimize.ready(() => {
    const userAgent = navigator.userAgent.toLowerCase();
    let deviceType = 'Other';

    if (userAgent.includes('mac')) deviceType = 'Mac';
    else if (userAgent.includes('windows')) deviceType = 'Windows';
    else if (userAgent.includes('linux')) deviceType = 'Linux';
    else if (userAgent.includes('android')) deviceType = 'Android';
    else if (userAgent.includes('iphone') || userAgent.includes('ipad')) deviceType = 'iOS';

    const scope = 'user'; // or 'pageview'
    const attributes = { userAgent: deviceType };

    intellimize.setAttributes(scope, attributes);
  });

