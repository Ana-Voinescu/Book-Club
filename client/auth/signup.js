// Step 1: catch form submit so the page doesn't reload
const form = document.querySelector('.signup-form');

const USERS_KEY = 'bookclub_users';

function loadUsers() {
  try { return JSON.parse(localStorage.getItem(USERS_KEY) || '[]'); }
  catch { return []; }
}
function saveUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
}


// Shows a single form-level error message (and makes it visible)
function showError(message) {
  const el = document.querySelector('.form-error');
  el.textContent = message;
  el.classList.remove('hidden');
}

// Hides the error area when the form is valid (or before re-validating)
function clearError() {
  const el = document.querySelector('.form-error');
  el.textContent = '';
  el.classList.add('hidden');
}



form.addEventListener('submit', (e) => {
  e.preventDefault(); // stop the browser from reloading the page

  // Read current values (we'll validate them in the next step)
  const fullName = document.querySelector('#fullname').value.trim();
  const email = document.querySelector('#email').value.trim();
  const password = document.querySelector('#password').value;
  const confirmPassword = document.querySelector('#confirm-password').value;


  clearError();
  // Basic password rules (Step 2): minimum length + match confirm
  if (password.length < 8) {
    showError('Password must be at least 8 characters long.');
    return;
    }if (password !== confirmPassword) {
    showError('Passwords do not match.');
    return;
    }

    const users = loadUsers();

    const normalizedEmail = email.trim().toLowerCase();
    const alreadyExists = users.some(u => (u.email || '').toLowerCase() === normalizedEmail);
    if (alreadyExists) {
      showError('An account with this email already exists.');
      return;
    }

    users.push({
      fullName,
      email: normalizedEmail,
      password
    });

    saveUsers(users);


    // Demo: save "logged in" state locally
    sessionStorage.setItem('bookclub_isAuthed', 'true');
    sessionStorage.setItem('bookclub_userName', fullName);


    form.reset();

    window.location.href = '../landing/index.html';



  console.log({ fullName, email, password, confirmPassword });
});
const welcomeEl = document.querySelector('.welcome-message');

if (isLoggedIn && welcomeEl) {
  const name = localStorage.getItem('bookclub_userName');
  if (name) {
    welcomeEl.textContent = `Welcome, ${name}!`;
    welcomeEl.classList.remove('hidden');
  }
}

