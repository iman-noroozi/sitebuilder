
  const ThemeManager = {
    // Array of available themes
    themes: ['wfc25-theme-light', 'wfc25-theme-base'], // Add more themes as needed

    // System themes configuration
    systemThemes: {
      light: 'wfc25-theme-light',  // Theme to use for system "light" mode
      dark: 'wfc25-theme-base'     // Theme to use for system "dark" mode
    },

    // Current theme state
    themePreference: localStorage.getItem('theme') || 'system',

    // Array to store theme change callbacks
    themeChangeCallbacks: [],

    // Method to add theme change callback
    onThemeChange: function(callback) {
      if (typeof callback === 'function') {
        this.themeChangeCallbacks.push(callback);
      }
    },

    // Method to get current resolved theme (resolves 'system' to actual theme)
    getResolvedTheme: function() {
      return this.themePreference === 'system' ? this.getSystemTheme() : this.themePreference;
    },

    // Method to get system theme
    getSystemTheme: function() {
      return window.matchMedia('(prefers-color-scheme: dark)').matches 
        ? this.systemThemes.dark 
      : this.systemThemes.light;
    },

    // Method to programmatically set theme
    setTheme: function(newThemePreference) {
      // Validate theme
      if (newThemePreference === 'system' || this.themes.includes(newThemePreference)) {
        handleThemeChange(newThemePreference);
        return true;
      }
      console.warn(`Invalid theme "${newThemePreference}". Available themes:`, ['system', ...this.themes]);
      return false;
    }
  };

  // Function to apply a theme
  function applyTheme(resolvedTheme) {
    const body = document.body;
    const html = document.documentElement;

    // Remove all theme classes
    ThemeManager.themes.forEach(t => {
      body.classList.remove(t);
      html.classList.remove(t);
    });

    // Add the selected theme class (if it's valid)
    if (ThemeManager.themes.includes(resolvedTheme)) {
      body.classList.add(resolvedTheme);
      html.classList.add(resolvedTheme);
    }
  }

  // Function to apply the system theme
  function applySystemTheme() {
    const systemTheme = ThemeManager.getSystemTheme();
    applyTheme(systemTheme);
  }

  // Function to handle theme changes
  function handleThemeChange(newThemePreference) {
    ThemeManager.themePreference = newThemePreference;

    if (newThemePreference === 'system') {
      localStorage.setItem('theme', 'system');
      applySystemTheme();
    } else {
      localStorage.setItem('theme', newThemePreference);
      applyTheme(newThemePreference);
    }

    // Update all UI controls to match the current theme
    updateThemeControls(newThemePreference);

    // Call all registered callbacks with theme information
    const resolvedTheme = ThemeManager.getResolvedTheme();
    ThemeManager.themeChangeCallbacks.forEach(callback => {
      callback({
        themePreference: newThemePreference,  // 'system', 'light-mode', or 'dark-mode'
        resolvedTheme: resolvedTheme          // actual applied theme ('light-mode' or 'dark-mode')
      });
    });
  }

  // Function to update all theme controls
  function updateThemeControls(themePreference) {
    const resolvedTheme = ThemeManager.getResolvedTheme();

    // Update selectors
    document.querySelectorAll('[data-theme-selector]').forEach(selector => {
      selector.value = themePreference;
    });

    // Update toggle switches
    document.querySelectorAll('[data-theme-toggle]').forEach(toggle => {
      const toggleTheme = toggle.getAttribute('data-theme-toggle');
      if (themePreference === 'system') {
        toggle.checked = resolvedTheme === toggleTheme;
      } else {
        toggle.checked = themePreference === toggleTheme;
      }
    });

    // Update click-based theme buttons
    document.querySelectorAll('[data-theme]').forEach(button => {
      const buttonTheme = button.getAttribute('data-theme');

      // Set aria-pressed
      button.setAttribute('aria-pressed', themePreference === buttonTheme);

      // Handle active state
      button.classList.toggle('active', themePreference === buttonTheme);

      // For system theme buttons, also check resolved theme
      if (buttonTheme === 'system' && themePreference === 'system') {
        button.classList.add('active');
      }
    });
  }

  // Function to initialize the theme
  function initializeTheme() {
    // Initial theme check
    try {
      const savedThemePreference = localStorage.getItem('theme') || 'system';
      if (savedThemePreference === 'system') {
        const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark-mode' : 'light-mode';
        document.documentElement.classList.add(systemTheme);
      } else {
        document.documentElement.classList.add(savedThemePreference);
      }
    } catch (e) {
      console.warn('Failed to set initial theme:', e);
    }

    // Set up system theme change listener
    const systemThemeQuery = window.matchMedia('(prefers-color-scheme: dark)');

    // Remove old listener if it exists (prevents duplicate listeners)
    systemThemeQuery.removeEventListener('change', handleSystemThemeChange);

    // Add new listener
    systemThemeQuery.addEventListener('change', handleSystemThemeChange);

    // Apply saved theme
    const savedThemePreference = localStorage.getItem('theme') || 'system';
    handleThemeChange(savedThemePreference);
  }

  // Handler for system theme changes
  function handleSystemThemeChange() {
    const currentThemePreference = localStorage.getItem('theme');
    if (currentThemePreference === 'system') {
      applySystemTheme();
      updateThemeControls('system');

      // Notify callbacks of the theme change
      const resolvedTheme = ThemeManager.getResolvedTheme();
      ThemeManager.themeChangeCallbacks.forEach(callback => {
        callback({
          themePreference: 'system',
          resolvedTheme: resolvedTheme
        });
      });
    }
  }

  // Event listener for theme selectors
  document.addEventListener('change', (event) => {
    const target = event.target;

    // Handle dropdown selectors
    if (target.matches('[data-theme-selector]')) {
      handleThemeChange(target.value);
    }

    // Handle toggle switches
    if (target.matches('[data-theme-toggle]')) {
      const toggleTheme = target.getAttribute('data-theme-toggle');

      // If the toggle is checked, apply its theme
      // If unchecked, apply the opposite theme or system theme
      if (target.checked) {
        handleThemeChange(toggleTheme);
      } else {
        // If we're toggling between light/dark, choose the opposite
        const oppositeTheme = toggleTheme === ThemeManager.systemThemes.dark 
        ? ThemeManager.systemThemes.light 
        : ThemeManager.systemThemes.dark;
        handleThemeChange(oppositeTheme);
      }
    }
  });

  // Event listener for click-based theme toggles
  document.addEventListener('click', (event) => {
    const target = event.target;

    if (target.matches('[data-theme]')) {
      handleThemeChange(target.getAttribute('data-theme'));
    }
  });

  // Initialize the theme on page load
  initializeTheme();

  // Export ThemeManager to make it globally available
  window.ThemeManager = ThemeManager;

  // Theme toggle button functionality
  document.addEventListener('DOMContentLoaded', () => {
    const lightBtn = document.querySelector('.theme-toggle_button[data-theme="wfc25-theme-light"]');
    const darkBtn = document.querySelector('.theme-toggle_button[data-theme="wfc25-theme-base"]');

    const showButton = (btn) => {
      if (!btn) return;
      const icon = btn.querySelector('.theme-toggle_icon');
      if (!icon) return;
      btn.classList.add('active');
      btn.style.display = 'flex';
      icon.classList.remove('icon-out');
      icon.classList.add('icon-in');
    };

    const hideButton = (btn) => {
      if (!btn) return;
      const icon = btn.querySelector('.theme-toggle_icon');
      if (!icon) return;
      icon.classList.remove('icon-in');
      icon.classList.add('icon-out');
      setTimeout(() => {
        btn.classList.remove('active');
        btn.style.display = 'none';
        icon.classList.remove('icon-out');
      }, 400);
    };

    const initialTheme = ThemeManager.getResolvedTheme();

    if (initialTheme === 'wfc25-theme-light') {
      if (lightBtn) {
        lightBtn.classList.remove('active');
        lightBtn.style.display = 'none';
      }
      if (darkBtn) {
        darkBtn.classList.add('active');
        darkBtn.style.display = 'flex';
      }
    } else {
      if (darkBtn) {
        darkBtn.classList.remove('active');
        darkBtn.style.display = 'none';
      }
      if (lightBtn) {
        lightBtn.classList.add('active');
        lightBtn.style.display = 'flex';
      }
    }

    ThemeManager.onThemeChange((themeData) => {
      if (themeData.resolvedTheme === 'wfc25-theme-light') {
        hideButton(lightBtn);
        showButton(darkBtn);
      } else {
        hideButton(darkBtn);
        showButton(lightBtn);
      }
    });
  });
