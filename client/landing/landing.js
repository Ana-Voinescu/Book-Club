document.addEventListener('DOMContentLoaded', () => {
  const isAuthed = sessionStorage.getItem('bookclub_isAuthed') === 'true';

const guestPanel = document.querySelector('.intro');
const ctaBtn = document.querySelector('.intro .btn'); 


  if (!isAuthed) return; 


  if (guestPanel) guestPanel.classList.add('hidden');

  if (ctaBtn) {

    if (ctaBtn.tagName.toLowerCase() === 'a') {
      ctaBtn.textContent = 'Go to Library';
      ctaBtn.href = '../library/library.html';
    } else {
      ctaBtn.textContent = 'Go to Library';
      ctaBtn.addEventListener('click', () => {
        window.location.href = '../library/library.html';
      });
    }
  }
});
