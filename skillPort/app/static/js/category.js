// category.js (Safari-hardened)
(function () {
  'use strict';

  // Helpers
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return (root || document).querySelectorAll(sel); }

  function clearActive(links) {
    for (var i = 0; i < links.length; i++) links[i].classList.remove('is_active');
  }

  document.addEventListener('DOMContentLoaded', function () {
    // ---------------- Header active state ----------------
    var container = $('#header .container');
    if (container) {
      var links = container.querySelectorAll('ul li a');

      for (var i = 0; i < links.length; i++) {
        (function (a) {
          a.addEventListener('click', function (e) {
            e.preventDefault();
            var wasActive = a.classList.contains('is_active');
            clearActive(links);
            if (!wasActive) a.classList.add('is_active');
          });
        })(links[i]);
      }

      document.addEventListener('click', function (e) {
        // guard e.target and container
        if (container && e && e.target && !container.contains(e.target)) {
          clearActive(links);
        }
      });
    }

    // ---------------- Dropdown menu ----------------
    var dropdown = document.getElementById('nav_category');
    if (dropdown) {
      var toggle = dropdown.querySelector('.dropdown_toggle');
      if (toggle) {
        toggle.addEventListener('click', function (e) {
          e.preventDefault();
          dropdown.classList.toggle('open');
        });
      }
      document.addEventListener('click', function (e) {
        var t = e && e.target ? e.target : null;
        if (!t) return;
        // Close if click is outside dropdown
        if (!dropdown.contains(t)) dropdown.classList.remove('open');
      });
    }

    // ---------------- Upload modal ----------------
    var openBtn = $('.upload_button');
    var modal = document.getElementById('upload_modal');
    var body = document.body;
    var lastFocused = null;

    function openModal() {
      if (!modal) return;
      lastFocused = document.activeElement;
      modal.classList.add('is_open');
      modal.setAttribute('aria-hidden', 'false');
      body.classList.add('modal_open');
    }
    function closeModal() {
      if (!modal) return;
      modal.classList.remove('is_open');
      modal.setAttribute('aria-hidden', 'true');
      body.classList.remove('modal_open');

      // stop preview + revoke blob
      var player = document.getElementById('preview_player');
      if (player) {
        try { player.pause(); } catch (err) {}
        try { if (player.src && player.src.indexOf('blob:') === 0) URL.revokeObjectURL(player.src); } catch (err) {}
        player.removeAttribute('src');
        player.load();
      }

      if (lastFocused && typeof lastFocused.focus === 'function') {
        try { lastFocused.focus(); } catch (err) {}
      }
    }

    if (openBtn && modal) {
      if (!openBtn.hasAttribute('type')) openBtn.setAttribute('type', 'button');
      openBtn.addEventListener('click', function (e) {
        e.preventDefault();
        openModal();
      });

      // use closest() so clicks on children still close
      modal.addEventListener('click', function (e) {
        var t = e && e.target ? e.target : null;
        if (!t) return;
        if (t.closest('[data-close]') || t.closest('.modal__backdrop')) {
          closeModal();
        }
      });

      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('is_open')) closeModal();
      });

      var form = $('#upload_form', modal);
      if (form) {
        form.addEventListener('submit', function (e) {
          e.preventDefault();
          alert('投稿しました！');
          closeModal();
        });
      }
    }

    // ---------------- File preview ----------------
    var fileInput = document.getElementById('video_file');
    var previewContainer = document.getElementById('video_preview');
    var previewPlayer = document.getElementById('preview_player');

    if (fileInput && previewContainer && previewPlayer) {
      fileInput.addEventListener('change', function () {
        var file = fileInput.files && fileInput.files[0];
        // console.log without optional chaining
        try { console.log('Selected file:', file ? file.name : '(none)'); } catch (err) {}

        if (file) {
          try {
            var url = URL.createObjectURL(file);
            previewPlayer.muted = true;          // Safari autoplay-safe
            previewPlayer.setAttribute('playsinline', '');
            previewPlayer.src = url;
            previewContainer.style.display = 'block';
          } catch (err) {
            previewPlayer.removeAttribute('src');
            previewContainer.style.display = 'none';
          }
        } else {
          previewPlayer.removeAttribute('src');
          previewContainer.style.display = 'none';
        }
      });
    }
  });
})();
