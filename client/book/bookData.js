/**
 * books
 * -----
 * An array of book objects.
 * Each object represents ONE book in the system.
 *
 * In the future:
 * - This data will come from the backend (DB)
 * - This array will be replaced by a fetch() call
 */
const books = [
  {
    id: 'romeo-juliet', // unique identifier (used in URL: ?id=romeo-juliet)
    title: 'Romeo and Juliet',
    author: 'William Shakespeare',
    year: 1998,
    summary:
      'Shakespeare’s timeless tragedy of two young lovers from feuding families.Their passionate romance ends in heartbreak, symbolizing love’s power and peril.',
    price: 10,
    cover: '../images/books/Romeo&Juliet.jpg',
    pdfUrl:
      'https://www.gutenberg.org/cache/epub/1513/pg1513-images.html'
  },

  {
    id: 'moby-dick',
    title: 'Moby Dick',
    author: 'Herman Melville',
    year: 2001,
    summary:
      'A thrilling tale of Captain Ahab’s obsessive quest to hunt the great white whale.It explores themes of fate, obsession, and the struggle between man and nature.',
    price: 0,
    cover: '../images/books/mobyDick.jpg',
    pdfUrl:
      'https://www.gutenberg.org/cache/epub/2701/pg2701-images.html'
  },

  {
    id: 'shakespeare',
    title: 'The Complete Works of William Shakespeare',
    author: 'William Shakespeare',
    year: 1994,
    summary:
      'The Complete Works of William Shakespeare brings together all of Shakespeare’s plays, sonnets, and poems in one volume.It offers the timeless masterpieces of the Bard, from tragedies and comedies to histories, showcasing the richness of English literature.',
    price: 0,
    cover: '../images/books/WilliamShakespeare.jpg',
    pdfUrl:
      'https://www.gutenberg.org/cache/epub/100/pg100-images.html'
  }
];

/**
 * getBookById
 * -------------
 * Returns a single book object that matches the given id.
 *
 * @param {string} bookId - The id taken from the URL (?id=...)
 * @returns {object | undefined}
 *
 * Why this function exists:
 * - Keeps lookup logic in one place
 * - Makes it easy to replace with backend later
 */
function getBookById(bookId) {
  return books.find(book => book.id === bookId);
}

// Expose data/functions to the global scope
window.BookData = {
  getBookById
};
