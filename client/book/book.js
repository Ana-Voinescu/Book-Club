/*******************************************************
 * book.js
 *
 * Page logic for the Book page.
 * Responsible for:
 * - Reading the book id from the URL
 * - Loading the book data
 * - Rendering the book details into the DOM
 *******************************************************/

/**
 * getBookIdFromUrl
 * ----------------
 * Reads the "id" query parameter from the URL.
 *
 * Example:
 *   book.html?id=romeo-juliet
 */
function getBookIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

/**
 * loadBook
 * --------
 * Loads the book data using the id from the URL.
 * If no book is found, returns null.
 */
function loadBook() {
  const bookId = getBookIdFromUrl();

  if (!bookId) {
    return null;
  }

  return BookData.getBookById(bookId);
}

/**
 * renderBook
 * ----------
 * Updates the DOM with the book details.
 *
 * @param {object} book - The book object to render
 */
function renderBook(book) {
  if (!book) return;

  document.querySelector('.info .title').textContent = book.title;
  document.querySelector('.author').textContent =
    `Author: ${book.author} | Release year: ${book.year}`;

  document.querySelector('.summery').textContent = book.summary;
  document.querySelector('.price').textContent = book.price;

  const coverImg = document.querySelector('.cover');
  coverImg.src = book.cover;
  coverImg.alt = `Cover of ${book.title}`;

  const readLink = document.querySelector('.state-read');
  readLink.href = book.pdfUrl;
}

/**
 * renderNotFound
 * --------------
 * Displays a fallback message if the book does not exist.
 */
function renderNotFound() {
  document.querySelector('.book-card').innerHTML =
    '<p>Book not found.</p>';
}

document.addEventListener('DOMContentLoaded', () => {
  const book = loadBook();

  if (!book) {
    renderNotFound();
    return;
  }

  renderBook(book);
  handlePurchaseUI(book);

});

function hasPurchasedBook(bookId) {
  const purchases =
    JSON.parse(localStorage.getItem('bookclub_purchases')) || [];
  return purchases.includes(bookId);
}

function handlePurchaseUI(book) {
  const isLoggedIn =
    sessionStorage.getItem('bookclub_isAuthed') === 'true';

  const buyBtn = document.querySelector('.state-buy');
  const readLink = document.querySelector('.state-read');
  if (!isLoggedIn) return;

  const purchased = hasPurchasedBook(book.id);

  if (purchased) {
    readLink.classList.remove('hidden');
  } else {

    buyBtn.classList.remove('hidden');

    buyBtn.addEventListener('click', () => {
      const purchases =
        JSON.parse(localStorage.getItem('bookclub_purchases')) || [];

      purchases.push(book.id);
      localStorage.setItem(
        'bookclub_purchases',
        JSON.stringify(purchases)
      );


      buyBtn.classList.add('hidden');
      readLink.classList.remove('hidden');
    });
  }
}
