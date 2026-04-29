type Theme = "light" | "dark";

const STORAGE_KEY = "quickly-theme";

function applyTheme(theme: Theme) {
  document.documentElement.classList.toggle("dark", theme === "dark");
  document.documentElement.style.colorScheme = theme;
  localStorage.setItem(STORAGE_KEY, theme);
  document.querySelectorAll<HTMLButtonElement>("[data-theme-toggle]").forEach((button) => {
    button.setAttribute("aria-label", `Switch to ${theme === "light" ? "dark" : "light"} theme`);
  });
}

function initTheme() {
  const saved = localStorage.getItem(STORAGE_KEY);
  const preferred: Theme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  applyTheme(saved === "dark" || saved === "light" ? saved : preferred);
  document.querySelectorAll<HTMLButtonElement>("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      applyTheme(document.documentElement.classList.contains("dark") ? "light" : "dark");
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
});
