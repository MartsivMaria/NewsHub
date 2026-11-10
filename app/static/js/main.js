const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");
const categoryButtons = document.querySelectorAll(".category-button");
const newsCards = document.querySelectorAll(".news-card");
const emptyState = document.getElementById("emptyState");
const resetButton = document.getElementById("resetFilters");

const menuToggle = document.getElementById("menuToggle");
const mainNav = document.querySelector(".main-nav");

let selectedCategory = "Усі новини";


function filterNews() {
    const query = searchInput.value.trim().toLowerCase();
    let visibleCount = 0;

    newsCards.forEach((card) => {
        const category = card.dataset.category;
        const title = card.dataset.title;
        const description = card.dataset.description;
        const author = card.dataset.author;

        const matchesCategory =
            selectedCategory === "Усі новини" ||
            category === selectedCategory;

        const searchableText =
            `${title} ${description} ${author} ${category}`;

        const matchesSearch = searchableText.includes(query);

        const isVisible = matchesCategory && matchesSearch;

        card.hidden = !isVisible;

        if (isVisible) {
            visibleCount++;
        }
    });

    emptyState.hidden = visibleCount !== 0;
}


categoryButtons.forEach((button) => {
    button.addEventListener("click", () => {
        selectedCategory = button.dataset.category;

        categoryButtons.forEach((item) => {
            item.classList.toggle("selected", item === button);
        });

        filterNews();
    });
});


searchInput.addEventListener("input", filterNews);


searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    filterNews();

    document.getElementById("latest").scrollIntoView({
        behavior: "smooth"
    });
});


resetButton.addEventListener("click", () => {
    searchInput.value = "";
    selectedCategory = "Усі новини";

    categoryButtons.forEach((button, index) => {
        button.classList.toggle("selected", index === 0);
    });

    filterNews();
});


menuToggle.addEventListener("click", () => {
    const isOpen = mainNav.classList.toggle("open");

    menuToggle.setAttribute("aria-expanded", String(isOpen));
    menuToggle.setAttribute(
        "aria-label",
        isOpen ? "Закрити меню" : "Відкрити меню"
    );
});


mainNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
        mainNav.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.setAttribute("aria-label", "Відкрити меню");
    });
});
