
document.addEventListener('DOMContentLoaded', () => {
    const locale = document.querySelector('meta[property="og:locale"]');
    if (locale) {
        document.cookie = `elementor_locale=${locale.content}; path=/; max-age=31536000; domain=.${window.location.hostname}`;
    }
});
