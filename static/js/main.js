// Client-side search: filters the link cards already rendered by Flask,
// so the page still works fully with JavaScript disabled.

const search = document.getElementById("search");
const cards = Array.from(document.querySelectorAll(".link-card"));
const categories = Array.from(document.querySelectorAll("[data-category]"));
const noResults = document.getElementById("no-results");

function applyFilter() {
  const query = search.value.trim().toLowerCase();
  let visible = 0;

  for (const card of cards) {
    const match = !query || card.dataset.search.includes(query);
    card.hidden = !match;
    if (match) visible++;
  }

  // Hide a category heading when none of its links match.
  for (const category of categories) {
    const anyVisible = Array.from(category.querySelectorAll(".link-card"))
      .some((card) => !card.hidden);
    category.hidden = !anyVisible;
  }

  noResults.hidden = visible > 0;
}

search.addEventListener("input", applyFilter);

// Press "/" anywhere to jump to the search box.
document.addEventListener("keydown", (event) => {
  if (event.key === "/" && document.activeElement !== search) {
    event.preventDefault();
    search.focus();
  }
});

// Footer status line, fetched from the server's own API.
fetch("/api/info")
  .then((res) => res.json())
  .then((data) => {
    document.getElementById("server-info").textContent =
      `Served by ${data.app} on Python ${data.python}.`;
  })
  .catch(() => { /* Non-essential: leave the footer as-is. */ });
