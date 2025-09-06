
  (function(h,o,u,n,d) {
    h=h[d]=h[d]||{q:[],onReady:function(c){h.q.push(c)}}
    d=o.createElement(u);d.async=1;d.src=n
    n=o.getElementsByTagName(u)[0];n.parentNode.insertBefore(d,n)
  })(window,document,'script','https://www.datadoghq-browser-agent.com/us1/v5/datadog-rum.js','DD_RUM')
  window.DD_RUM.onReady(function() {
    window.DD_RUM.init({
      clientToken: 'pubcc1a0f0d10b59ea2dbe4b09b2e4f3fd1',
      applicationId: 'e8e849db-5e64-4418-bc8c-79aa92e82a9a',
      // `site` refers to the Datadog site parameter of your organization
      // see https://docs.datadoghq.com/getting_started/site/
      site: 'datadoghq.com',
      service: 'webflow.com',
      env: 'prod',
      // Specify a version number to identify the deployed version of your application in Datadog
      // version: '1.0.0',
      sessionSampleRate: 20,
      sessionReplaySampleRate: 0,
      trackUserInteractions: true,
      trackResources: true,
      trackLongTasks: true,
      defaultPrivacyLevel: 'mask-user-input',
    });
  })
