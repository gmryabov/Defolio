const THEME_KEY = 'preferred-theme';

function applyTheme(theme) {
document.documentElement.setAttribute('data-bs-theme', theme);
}

function toggleTheme() {
const currentTheme = document.documentElement.getAttribute('data-bs-theme');
const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
const toggleButton = document.getElementById('theme-toggler');
applyTheme(newTheme);
localStorage.setItem(THEME_KEY, newTheme);
if (newTheme === 'dark') {
  toggleButton.innerHTML = '<i class="bi bi-moon-stars"></i> Переключить тему';
} else {
  toggleButton.innerHTML = '<i class="bi bi-brightness-low"></i> Переключить тему';
}
}

function detectSystemTheme() {
return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
  ? 'dark'
  : 'light';
}

function initTheme() {
const savedTheme = localStorage.getItem(THEME_KEY);
const themeToApply = savedTheme || detectSystemTheme() || 'light';
const toggleButton = document.getElementById('theme-toggler');
applyTheme(themeToApply);
if (themeToApply === 'dark') {
  toggleButton.innerHTML = '<i class="bi bi-moon-stars"></i> Переключить тему';
} else {
  toggleButton.innerHTML = '<i class="bi bi-brightness-low"></i> Переключить тему';
}
}

document.addEventListener('DOMContentLoaded', () => {
initTheme();

const toggleButton = document.getElementById('theme-toggler');
if (toggleButton) {
  toggleButton.addEventListener('click', toggleTheme);
}
});