// -------------------------
// HEADER: Auth UI (demo only)
// -------------------------

// Demo auth state (no server yet):
// false = guest, true = logged-in user.
// Read auth state from localStorage (demo)
const isLoggedIn = sessionStorage.getItem('bookclub_isAuthed') === 'true';



// Grab all nav <li> elements that are marked for "auth-only" or "guest-only"
const authItems = document.querySelectorAll('[data-show="auth"]');
const guestItems = document.querySelectorAll('[data-show="guest"]');

// Toggle visibility by adding/removing the CSS class "hidden".
// (CSS .hidden => display: none)
if (isLoggedIn) {
  // Logged-in → show auth links, hide guest link
  authItems.forEach(item => item.classList.remove('hidden'));
  guestItems.forEach(item => item.classList.add('hidden'));
} else {
  // Guest → hide auth links, show guest link
  authItems.forEach(item => item.classList.add('hidden'));
  guestItems.forEach(item => item.classList.remove('hidden'));
}

// -------------------------
// SEARCH: Autocomplete dropdown (demo data)
// -------------------------

// Temporary book list (until we have DB/API).
// Each book should have a title and a link to its book page.
const BOOKS = BookData.getAllBooks().map((b) => ({
  id: b.id,
  title: b.title,
}));



// Cache the search input element.
const searchInput = document.querySelector('.search-bar input[type="search"]');

// Create the dropdown <ul> dynamically and attach it under the search bar.
const dropdown = document.createElement('ul');
dropdown.className = 'search-dropdown hidden';
document.querySelector('.search-bar').appendChild(dropdown);

// Keep the latest matches so Enter can use them.
let lastMatches = [];

// Index of the currently highlighted suggestion (keyboard navigation).
// -1 means: nothing is selected.
let activeIndex = -1;

// Helper: hide the dropdown and clear its content.
function closeDropdown() {
  dropdown.classList.add('hidden');
  dropdown.innerHTML = '';
  lastMatches = [];
  activeIndex = -1; // reset keyboard selection
}

// Adds "active" class to the currently selected item (for keyboard highlight)
function updateActiveItem(items) {
  items.forEach((item, index) => {
    item.classList.toggle('active', index === activeIndex);
  });
}

// Render the dropdown suggestions based on the matches array.
function renderSuggestions(matches) {
  dropdown.innerHTML = '';
  lastMatches = matches;
  activeIndex = -1; // reset selection every time we re-render

  // If no matches, show a single "No books found" row (polish).
  if (matches.length === 0) {
    const li = document.createElement('li');
    li.textContent = 'No books found';
    li.classList.add('no-results'); // optional styling hook
    dropdown.appendChild(li);
    dropdown.classList.remove('hidden');
    return;
  }

  // Create a clickable <li> for each matched book.
  matches.forEach((book) => {
    const li = document.createElement('li');
    li.textContent = book.title;

    // On click, navigate to the book page.
    li.addEventListener('click', () => {
      window.location.href = `../book/book.html?id=${book.id}`;
    });

    dropdown.appendChild(li);
  });

  dropdown.classList.remove('hidden');
}

// 1) Input event: update suggestions on every keystroke.
searchInput.addEventListener('input', () => {
  const q = searchInput.value.trim().toLowerCase();

  // If the input is empty, close the dropdown (polish).
  if (q === '') {
    closeDropdown();
    return;
  }

  // Filter by "startsWith" so results must begin with the typed text.
  const matches = BOOKS.filter((b) =>
    b.title.toLowerCase().startsWith(q)
  );

  renderSuggestions(matches);
});

// 2) Close dropdown when clicking anywhere outside the search bar (polish).
document.addEventListener('click', (e) => {
  const searchBar = document.querySelector('.search-bar');

  // If the click target is NOT inside the search bar, close the dropdown.
  if (!searchBar.contains(e.target)) {
    closeDropdown();
  }
});

// 3) Close dropdown on page navigation/unload (polish).
window.addEventListener('beforeunload', () => {
  closeDropdown();
});

// 4) Keyboard behavior (polish):
// - ArrowDown / ArrowUp: move through suggestions
// - Enter:
//    * if an item is highlighted → open that book
//    * else if exactly one match → open it
//    * else → go to Library with the query
// - Escape: close dropdown
searchInput.addEventListener('keydown', (e) => {
  // If dropdown is closed, only Enter behavior might still be relevant,
  // but we keep it simple: do nothing unless dropdown is open or key is Enter.
  const isDropdownOpen = !dropdown.classList.contains('hidden');

  // Handle Arrow navigation only when dropdown is open
  if (isDropdownOpen && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
    e.preventDefault();

    const items = dropdown.querySelectorAll('li');

    // If there are no real results (e.g., "No books found"), do nothing
    if (items.length === 0 || lastMatches.length === 0) return;

    if (e.key === 'ArrowDown') {
      activeIndex = (activeIndex + 1) % lastMatches.length;
    } else {
      activeIndex = (activeIndex - 1 + lastMatches.length) % lastMatches.length;
    }

    updateActiveItem(items);
    return;
  }

  // Escape closes the dropdown (when open)
  if (isDropdownOpen && e.key === 'Escape') {
    closeDropdown();
    return;
  }

  // Enter behavior (works whether dropdown is open or not)
  if (e.key !== 'Enter') return;

  const q = searchInput.value.trim();
  if (q === '') return;

  if (activeIndex >= 0 && lastMatches[activeIndex]?.id) {
    window.location.href = `../book/book.html?id=${lastMatches[activeIndex].id}`;
    return;
  }

  if (lastMatches.length === 1 && lastMatches[0].id) {
    window.location.href = `../book/book.html?id=${lastMatches[0].id}`;
    return;
}


  // Otherwise, go to Library and pass the query in the URL.
  // Your library page can later read this with:
  // new URLSearchParams(location.search).get('q')
  window.location.href = `../library/library.html?q=${encodeURIComponent(q)}`;
});
const logoutBtn = document.querySelector('#logout-btn');

if (logoutBtn) {
  logoutBtn.addEventListener('click', (e) => {
    e.preventDefault(); 
    sessionStorage.removeItem('bookclub_isAuthed');
    sessionStorage.removeItem('bookclub_userName');
    window.location.href = '../landing/index.html';
  });
}
