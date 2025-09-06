
  wf_utils.getUser((user) => {
    if (user) {
      const nameElements = document.querySelectorAll('[data-name="true"]');
      const firstName = user.fullName.split(' ')[0]; // This will get just the first word

      nameElements.forEach(element => {
        element.textContent = firstName;
      });
    }
  });
