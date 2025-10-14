
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

  //slideshow -----------------------------------------------------------------

  let slideIndex = 0;
const slides = document.querySelectorAll(".slide");
const dots   = document.querySelectorAll(".dot");
const title  = document.getElementById("slideshow-title");

const titles = ["First Title", "Second Title", "Third Title"];

function showSlide(n) {
  slides.forEach((slide, i) => {
    slide.classList.remove("active");
    dots[i].classList.remove("active");
  });

  slides[n].classList.add("active");
  dots[n].classList.add("active");

  if (title) {
    title.style.opacity = 0;
    setTimeout(() => {
      title.textContent = titles[n];
      title.style.opacity = 1;
    }, 1000); 
  }
}

function nextSlide() {
  slideIndex = (slideIndex + 1) % slides.length;
  showSlide(slideIndex);
}

// init
showSlide(slideIndex);
setInterval(nextSlide, 5000);


