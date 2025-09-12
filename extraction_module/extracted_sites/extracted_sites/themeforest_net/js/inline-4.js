
  window.addEventListener("CookiebotOnDialogDisplay", (event) => {
    const cookieDialog = event.srcElement.CookieConsentDialog.DOM
    cookieDialog.dataset.turbo = false
  })
