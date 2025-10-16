// header-------------------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('#header .container');
    const links = container.querySelectorAll('ul li a');
  
    function clearActive() {
      links.forEach(a => a.classList.remove('is-active'));
    }
  
    links.forEach(a => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        const wasActive = a.classList.contains('is-active');
        clearActive();
        if (!wasActive) a.classList.add('is-active');
      });
    });
  
    document.addEventListener('click', (e) => {
      if (!container.contains(e.target)) clearActive();
    });
  });

  // dropdown---------------------------------------------------------

  document.addEventListener("DOMContentLoaded", () => {
    const dropdown = document.getElementById("nav-category");
    const toggle = dropdown.querySelector(".dropdown-toggle");
  
    toggle.addEventListener("click", (e) => {
      e.preventDefault();
      dropdown.classList.toggle("open");
    });
  
    // close if click outside
    document.addEventListener("click", (e) => {
      if (!dropdown.contains(e.target)) {
        dropdown.classList.remove("open");
      }
    });
  });
  

  // -----------------------------------------------------------------



// 動画アップロードpopup ---------------------------------------------

(function () {
  const openBtn = document.querySelector('.upload_button');
  const modal = document.getElementById('uploadModal');
  if (!openBtn || !modal) return;

  const closeSelectors = '[data-close], .modal__backdrop';
  const closeTargets = () => modal.querySelectorAll(closeSelectors);

  let lastFocused = null;

  function openModal() {
    lastFocused = document.activeElement;
    modal.classList.add('is-open');
    document.body.classList.add('modal-open');
    modal.setAttribute('aria-hidden', 'false');

    const focusable = modal.querySelector('input, button, [href], select, textarea, [tabindex]:not([tabindex="-1"])');
    (focusable || modal).focus();
  }

  function closeModal() {
    modal.classList.remove('is-open');
    document.body.classList.remove('modal-open');
    modal.setAttribute('aria-hidden', 'true');
    if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
  }

  openBtn.addEventListener('click', (e) => {
    e.preventDefault();
    openModal();
  });

  modal.addEventListener('click', (e) => {
    if (e.target.matches(closeSelectors)) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('is-open')) {
      closeModal();
    }
  });

  const form = modal.querySelector('#uploadForm');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('アップロード処理のフックに到達しました！');
      closeModal();
    });
  }
})();

const fileInput = document.getElementById('videoFile');
const previewContainer = document.getElementById('videoPreview');
const previewPlayer = document.getElementById('previewPlayer');

if (fileInput) {
  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      previewPlayer.src = url;
      previewContainer.style.display = 'block';
    } else {
      previewPlayer.src = '';
      previewContainer.style.display = 'none';
    }
  });
}


// 動画アップロードpopup ---------------------------------------------