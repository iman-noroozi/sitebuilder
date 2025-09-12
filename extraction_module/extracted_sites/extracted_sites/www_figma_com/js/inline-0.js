
(function() {
  const homepagePattern = new RegExp("^/((de-de|es-es|es-la|fr-fr|it-it|nl-nl|pl-pl|pt-br|ja-jp|ko-kr)/)?$")
  const hasStateCookie = /(^|; *)(__host-)?figma\.authn-state=1(;|$)/i.test(document.cookie)
  window.isHomepage = homepagePattern.test(window.location.pathname)
  window.redirectToApp = () => { window.location.href = "/redirect_home" }

  if (window.isHomepage && hasStateCookie) {
    window.redirectToApp()
  }
})()
