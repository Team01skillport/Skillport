let categories_from_db = [];

function handleFilterToggle(event) {
  const button = event.currentTarget;
  const filterSection = button.closest(".filter-section");
  const content = filterSection.querySelector(".filter-content");

  if (!content) return;

  button.classList.toggle("open");

  const isOpenNow = button.classList.contains("open");
  if (
    isOpenNow &&
    filterSection.id === "categoryFilter" &&
    content.innerHTML.trim() === ""
  ) {
    renderCategories(categories_from_db, content);
  }
}

function renderCategories(categories, container) {
  if (!Array.isArray(categories) || categories.length === 0) {
    container.innerHTML =
      '<p style="font-size: 13px; color: #777; padding-left: 5px;">カテゴリーが見つかりません。</p>';
    return;
  }

  const checkboxGroup = document.createElement("div");
  checkboxGroup.className = "filter-checkbox-group";

  const html = categories
    .map(
      (cat) => `
        <label>
            <input type="checkbox" name="category" value="${cat.id}" /> ${cat.name}
        </label>
    `
    )
    .join("");

  checkboxGroup.innerHTML = html;
  container.appendChild(checkboxGroup);
}

function updatePriceDisplay(event) {
  const priceValueSpan = document.getElementById("priceValue");
  const maxPriceInput = document.querySelector(
    '.price-inputs input[name="max_price"]'
  );

  const numericValue = parseInt(event.target.value);
  const formattedValue = numericValue.toLocaleString();

  if (priceValueSpan) {
    priceValueSpan.textContent = formattedValue;
  }
  if (maxPriceInput) {
    maxPriceInput.value = numericValue;
  }

  const minPriceInput = document.querySelector(
    '.price-inputs input[name="min_price"]'
  );
  if (minPriceInput && minPriceInput.value === "") {
    minPriceInput.value = event.target.min;
  }
}

function initMarketPage() {
  const sidebarElement = document.querySelector(".sidebar");
  if (sidebarElement && sidebarElement.dataset.categories) {
    try {
      const parsedData = JSON.parse(sidebarElement.dataset.categories);
      if (Array.isArray(parsedData)) {
        categories_from_db = parsedData;
      } else {
        categories_from_db = [];
      }
    } catch (e) {
      console.error("カテゴリーデータの読み込みに失敗しました:", e);
      categories_from_db = [];
    }
  }

  const allToggleButtons = document.querySelectorAll(".toggle-filter-btn");
  const priceRangeSlider = document.getElementById("priceRange");
  const minPriceInput = document.querySelector(
    '.price-inputs input[name="min_price"]'
  );
  const maxPriceInput = document.querySelector(
    '.price-inputs input[name="max_price"]'
  );

  allToggleButtons.forEach((button) => {
    button.type = "button";
    button.addEventListener("click", handleFilterToggle);
  });

  if (priceRangeSlider) {
    const priceValueSpan = document.getElementById("priceValue");
    const initialNumericValue = parseInt(priceRangeSlider.value);

    if (priceValueSpan) {
      priceValueSpan.textContent = initialNumericValue.toLocaleString();
    }

    priceRangeSlider.addEventListener("input", updatePriceDisplay);

    priceRangeSlider.addEventListener("mousedown", () => {
      priceRangeSlider.classList.add("slider-active");
    });
    priceRangeSlider.addEventListener("mouseup", () => {
      priceRangeSlider.classList.remove("slider-active");
    });
    priceRangeSlider.addEventListener("mouseleave", () => {
      priceRangeSlider.classList.remove("slider-active");
    });
  }
}

document.addEventListener("DOMContentLoaded", initMarketPage);
