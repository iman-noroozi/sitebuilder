
  // Utility to validate time format
  function isValidTimeFormat(timeStr) {
    return /^(\d{1,2}:\d{2} [APap][Mm])$/.test(timeStr.trim());
  }

  // Convert ET string (e.g. "8:00 am") to user's local time
  function convertETToLocal(etTimeString) {
    let [hour, minutePart] = etTimeString.split(':');
    const [minute, meridiem] = minutePart.trim().split(' ');

    hour = parseInt(hour, 10);
    if (meridiem.toUpperCase() === 'PM' && hour !== 12) {
      hour += 12;
    } else if (meridiem.toUpperCase() === 'AM' && hour === 12) {
      hour = 0;
    }

    // Use a consistent ET offset to create Date object
    const isoString = `2025-05-16T${String(hour).padStart(2, '0')}:${minute}:00-04:00`;
    const date = new Date(isoString);

    return date.toLocaleTimeString([], {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  }

  // Store original ET time if not already stored
  document.querySelectorAll('[data-session-time]').forEach(el => {
    const time = el.textContent.trim();
    if (!el.hasAttribute('data-original-time') && isValidTimeFormat(time)) {
      el.setAttribute('data-original-time', time);
    }
  });

  // Function to apply timezone preference
  function applyTimezonePreference(targetTimezone) {
    document.querySelectorAll('[data-session-time]').forEach(el => {
      const originalTime = el.getAttribute('data-original-time');
      if (!originalTime || !isValidTimeFormat(originalTime)) return;

      if (targetTimezone === 'local') {
        el.textContent = convertETToLocal(originalTime);
      } else {
        el.textContent = originalTime;
      }
    });

    document.querySelectorAll('[data-timezone-label]').forEach(label => {
      label.textContent = targetTimezone === 'local' ? 'LOCAL' : 'ET';
    });

    console.log(`🕒 Timezone set to ${targetTimezone.toUpperCase()}`);
  }

  // Event listener for radios
  document.querySelectorAll('[data-timezone]').forEach(radio => {
    radio.addEventListener('change', () => {
      if (radio.checked) {
        const selectedZone = radio.getAttribute('data-timezone');
        applyTimezonePreference(selectedZone);
      }
    });
  });

  // Initial timezone preference on load
  window.addEventListener('DOMContentLoaded', () => {
    const active = document.querySelector('[data-timezone]:checked');
    if (active) {
      applyTimezonePreference(active.getAttribute('data-timezone'));
    }
  });
