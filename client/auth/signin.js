// 1) Grab the correct form (your HTML uses "signip-form")
const form = document.querySelector('.signip-form');

const USERS_KEY = 'bookclub_users';

function showError(message) {
  const el = document.querySelector('.form-error');
  el.textContent = message;
  el.classList.remove('hidden');
}

function clearError() {
  const el = document.querySelector('.form-error');
  el.textContent = '';
  el.classList.add('hidden');
}


// Helper: load users created in Sign Up (example key; use YOUR real key from signup.js)
function loadUsers() {
  try { return JSON.parse(localStorage.getItem(USERS_KEY) || '[]'); }
  catch { return []; }
}


form.addEventListener('submit', (e) => {
  e.preventDefault();

  const email = document.querySelector('#email').value.trim().toLowerCase();
  const password = document.querySelector('#password').value;

  clearError();

  if (!email || !password) {
    showError('Please enter email and password.');
    return;
  }

  const users = loadUsers();
  const user = users.find(u => (u.email || '').toLowerCase() === email);

  if (!user) {
    showError('No account found with this email.');
    return;
  }

  if (user.password !== password) {
    showError('Incorrect password.');
    return;
  }

  sessionStorage.setItem('bookclub_isAuthed', 'true');
  sessionStorage.setItem('bookclub_userName', user.fullName);

  form.reset();
  window.location.href = '../landing/index.html';
});
