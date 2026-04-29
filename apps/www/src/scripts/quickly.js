import { generate } from "random-words";

const STORAGE_KEY = "quickly-theme";
const SUGGESTIONS = [
  "quickly search engine",
  "quickly find files",
  "quick sort algorithm",
  "quickly meaning",
  "quicken loans",
  "quick recipes",
  "quickly synonym",
  "quick maths",
  "quickly adverb",
  "quick draw",
];
const CHIPS = ["Trending", "News", "Sports", "Finance", "Technology", "Science"];
const API_URL = window.QUICKLY_API_URL || "http://localhost:5000";

function applyTheme(theme) {
  document.documentElement.classList.toggle("dark", theme === "dark");
  localStorage.setItem(STORAGE_KEY, theme);
  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.setAttribute("aria-label", `Switch to ${theme === "light" ? "dark" : "light"} theme`);
  });
}

function initTheme() {
  const saved = localStorage.getItem(STORAGE_KEY);
  const preferred = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  applyTheme(saved || preferred);
  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      applyTheme(document.documentElement.classList.contains("dark") ? "light" : "dark");
    });
  });
}

function targetFor(query, page = 1) {
  const params = new URLSearchParams({ q: query.trim() });
  if (page > 1) params.set("page", page);
  return `/search?${params.toString()}`;
}

function randomWord() {
  const word = generate();
  if (typeof word === "string" && word.trim()) return word.trim();
  return CHIPS[Math.floor(Math.random() * CHIPS.length)];
}

function renderSuggestions(input, list, onSubmit) {
  const value = input.value.toLowerCase();
  const matches =
    value.length > 1 ? SUGGESTIONS.filter((item) => item.startsWith(value)).slice(0, 6) : [];
  list.innerHTML = "";
  list.classList.toggle("hidden", matches.length === 0 || document.activeElement !== input);
  input
    .closest("[data-search-shell]")
    ?.classList.toggle("is-open", matches.length > 0 && document.activeElement === input);

  matches.forEach((suggestion) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className =
      "flex w-full items-center gap-3 px-5 py-2.5 text-left text-sm text-[#4a4540] transition-colors duration-100 hover:bg-[var(--accent-soft)] dark:text-[#b8b0a5]";
    item.innerHTML = `<svg width="14" height="14" viewBox="0 0 20 20" fill="none" class="shrink-0 opacity-35"><circle cx="8.5" cy="8.5" r="5.5" stroke="currentColor" stroke-width="1.8"></circle><path d="M13 13L17 17" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"></path></svg><span><strong class="font-medium text-[#141210] dark:text-[#f0ede8]">${suggestion.slice(0, input.value.length)}</strong>${suggestion.slice(input.value.length)}</span>`;
    item.addEventListener("mousedown", (event) => {
      event.preventDefault();
      input.value = suggestion;
      onSubmit(suggestion);
    });
    list.append(item);
  });
}

function initSearchBars() {
  document.querySelectorAll("[data-search-form]").forEach((form) => {
    const input = form.querySelector("[data-search-input]");
    const list = form.querySelector("[data-suggestions]");
    const clear = form.querySelector("[data-clear-search]");
    if (!input || !list) return;

    const onSubmit = (query) => {
      if (query.trim()) window.location.href = targetFor(query);
    };

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      onSubmit(input.value);
    });
    input.addEventListener("input", () => {
      clear?.classList.toggle("hidden", !input.value);
      renderSuggestions(input, list, onSubmit);
    });
    input.addEventListener("focus", () => renderSuggestions(input, list, onSubmit));
    input.addEventListener("blur", () =>
      setTimeout(() => renderSuggestions(input, list, onSubmit), 150),
    );
    clear?.addEventListener("click", () => {
      input.value = "";
      clear.classList.add("hidden");
      renderSuggestions(input, list, onSubmit);
      input.focus();
    });
  });

  document.querySelectorAll("[data-random-search]").forEach((button) => {
    button.addEventListener("click", () => {
      window.location.href = targetFor(randomWord());
    });
  });
}

function cap(value) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function escapeHtml(value) {
  const element = document.createElement("div");
  element.textContent = value || "";
  return element.innerHTML;
}

function displayUrl(value) {
  try {
    const url = new URL(value);
    return `${url.hostname}${url.pathname === "/" ? "" : url.pathname}`;
  } catch {
    return value || "";
  }
}

function resultDomain(value) {
  try {
    return new URL(value).hostname;
  } catch {
    return (value || "").split("/")[0];
  }
}

async function fetchResults(query, page) {
  const url = new URL("/search", API_URL);
  url.searchParams.set("q", query);
  url.searchParams.set("page", page);
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Search failed with ${response.status}`);
  }
  return response.json();
}

function normalizeSearchPayload(payload) {
  if (Array.isArray(payload)) {
    return {
      results: payload,
      meta: {
        search_speed_ms: 0,
        total_results: payload.length,
      },
      pagination: {
        page: 1,
        page_size: payload.length || 10,
        total_pages: payload.length ? 1 : 0,
        has_next: false,
        has_previous: false,
      },
    };
  }

  return {
    results: payload.results || [],
    meta: payload.meta || {},
    pagination: payload.pagination || {},
  };
}

function renderResultList(root, results) {
  const list = root.querySelector("[data-results-list]");
  if (!results.length) {
    list.innerHTML =
      '<div class="rounded-xl border-[1.5px] border-black/[0.09] bg-white/70 p-5 font-dm text-[13.5px] text-[#4a4540] backdrop-blur-sm dark:border-white/[0.08] dark:bg-[#1e1c18]/70 dark:text-[#b8b0a5]">No results found.</div>';
    return;
  }

  list.innerHTML = results
    .map((item, index) => {
      const url = item.url || "";
      const dom = resultDomain(url);
      const featured = index === 0;
      const title = escapeHtml(item.title || url || "Untitled result");
      const snippet = escapeHtml(item.description || "");
      const href = escapeHtml(url);
      return `<article class="group animate-result-slide r${index} transition-all duration-150 ${featured ? "mb-1 rounded-xl border-[1.5px] border-black/[0.09] bg-white/70 p-5 shadow-sm backdrop-blur-sm hover:border-[var(--accent)] hover:bg-[var(--accent-soft)] dark:border-white/[0.08] dark:bg-[#1e1c18]/70" : "border-b border-black/[0.07] py-3.5 dark:border-white/[0.06]"}">
      <a href="${href}" class="block" target="_blank" rel="noreferrer">
        <div class="mb-1.5 flex flex-wrap items-center gap-2">
          <img src="https://www.google.com/s2/favicons?domain=${escapeHtml(dom)}&sz=32" width="15" height="15" class="shrink-0 rounded-[3px]" alt="">
          <span class="max-w-[320px] truncate text-[13px] font-light text-[#8a837a] dark:text-[#6e6760]">${escapeHtml(displayUrl(url))}</span>
          ${featured ? `<span class="shrink-0 rounded-full bg-[var(--accent-soft)] px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-[var(--accent)]">Top pick</span>` : ""}
        </div>
        <h3 class="mb-1.5 font-dm text-[17px] font-medium leading-snug text-[oklch(0.48_0.18_245)] transition-colors duration-150 group-hover:text-[var(--accent)] group-hover:underline group-hover:underline-offset-2 dark:text-[oklch(0.70_0.16_245)]">${title}</h3>
        <p class="max-w-[680px] text-[13.5px] font-light leading-relaxed text-[#4a4540] dark:text-[#b8b0a5]">${snippet}</p>
      </a>
    </article>`;
    })
    .join("");
}

function renderPagination(root, query, pagination) {
  const paginationRoot = root.querySelector("[data-pagination]");
  if (!paginationRoot) return;

  const current = pagination.page || 1;
  const total = pagination.total_pages || 0;
  if (total <= 1) {
    paginationRoot.innerHTML = "";
    return;
  }

  const start = Math.max(1, current - 3);
  const end = Math.min(total, start + 6);
  const pageItems = [];

  if (pagination.has_previous) {
    pageItems.push(
      `<a href="${targetFor(query, current - 1)}" class="rounded-lg border-[1.5px] border-black/[0.09] px-4 py-2 font-dm text-[13px] text-[#4a4540] transition-colors duration-150 hover:border-black/20 dark:border-white/[0.08] dark:text-[#b8b0a5] dark:hover:border-white/20">Prev</a>`,
    );
  } else {
    pageItems.push(
      '<span class="rounded-lg border-[1.5px] border-black/[0.09] px-4 py-2 font-dm text-[13px] text-[#4a4540] opacity-35 dark:border-white/[0.08] dark:text-[#b8b0a5]">Prev</span>',
    );
  }

  for (let page = start; page <= end; page += 1) {
    const isActive = page === current;
    pageItems.push(
      isActive
        ? `<span class="flex h-9 w-9 items-center justify-center rounded-lg border-[1.5px] border-[var(--accent)] bg-[var(--accent)] font-dm text-[13px] font-semibold text-white">${page}</span>`
        : `<a href="${targetFor(query, page)}" class="flex h-9 w-9 items-center justify-center rounded-lg border-[1.5px] border-black/[0.09] font-dm text-[13px] text-[#4a4540] transition-all duration-150 hover:border-black/20 dark:border-white/[0.08] dark:text-[#b8b0a5] dark:hover:border-white/20">${page}</a>`,
    );
  }

  if (pagination.has_next) {
    pageItems.push(
      `<a href="${targetFor(query, current + 1)}" class="rounded-lg border-[1.5px] border-black/[0.09] px-4 py-2 font-dm text-[13px] text-[#4a4540] transition-colors duration-150 hover:border-black/20 dark:border-white/[0.08] dark:text-[#b8b0a5] dark:hover:border-white/20">Next</a>`,
    );
  } else {
    pageItems.push(
      '<span class="rounded-lg border-[1.5px] border-black/[0.09] px-4 py-2 font-dm text-[13px] text-[#4a4540] opacity-35 dark:border-white/[0.08] dark:text-[#b8b0a5]">Next</span>',
    );
  }

  paginationRoot.innerHTML = pageItems.join("");
}

async function initResultsPage() {
  const root = document.querySelector("[data-results-page]");
  if (!root) return;
  const params = new URLSearchParams(window.location.search);
  const query = params.get("q") || "Trending";
  const page = Math.max(Number.parseInt(params.get("page") || "1", 10) || 1, 1);

  document.title = `${query} - Quickly`;
  root.querySelector("[data-search-input]").value = query;
  if (root.hasAttribute("data-server-rendered")) return;

  root.querySelector("[data-stats]").textContent = "Searching...";
  const panelTitle = root.querySelector("[data-panel-title]");
  const panelImage = root.querySelector("[data-panel-image]");
  if (panelTitle) panelTitle.textContent = cap(query);
  if (panelImage) panelImage.innerHTML = `image placeholder<br>${query}`;
  root.querySelector("[data-speed]").textContent = "--";
  root.querySelector("[data-found]").textContent = "--";
  root.querySelector("[data-results-list]").innerHTML =
    '<div class="rounded-xl border-[1.5px] border-black/[0.09] bg-white/70 p-5 font-dm text-[13.5px] text-[#4a4540] backdrop-blur-sm dark:border-white/[0.08] dark:bg-[#1e1c18]/70 dark:text-[#b8b0a5]">Loading results...</div>';

  try {
    const payload = normalizeSearchPayload(await fetchResults(query, page));
    const results = payload.results;
    const totalResults = payload.meta.total_results ?? results.length;
    const speedMs = payload.meta.search_speed_ms ?? 0;
    const speedSeconds = (speedMs / 1000).toFixed(2);
    root.querySelector("[data-stats]").innerHTML =
      `<strong class="font-medium text-[#4a4540] dark:text-[#b8b0a5]">${totalResults.toLocaleString()}</strong> results <span class="mx-1.5 opacity-40">.</span> page ${payload.pagination.page || page} of ${payload.pagination.total_pages || 1} <span class="mx-1.5 opacity-40">.</span> ${speedSeconds}s`;
    root.querySelector("[data-speed]").textContent = `${speedSeconds}s`;
    root.querySelector("[data-found]").textContent = totalResults.toLocaleString();
    renderResultList(root, results);
    renderPagination(root, query, payload.pagination);
  } catch (error) {
    console.error(error);
    root.querySelector("[data-stats]").textContent = "Search failed.";
    root.querySelector("[data-results-list]").innerHTML =
      '<div class="rounded-xl border-[1.5px] border-red-500/30 bg-white/70 p-5 font-dm text-[13.5px] text-[#4a4540] backdrop-blur-sm dark:bg-[#1e1c18]/70 dark:text-[#b8b0a5]">Could not load results from the API.</div>';
  }

  root.querySelector("[data-related]").innerHTML = [
    `${query} explained`,
    `${query} examples`,
    `${query} tutorial`,
    `best ${query}`,
    `${query} history`,
    `how to use ${query}`,
  ]
    .map(
      (item) =>
        `<a href="${targetFor(item)}" class="rounded-full border-[1.5px] border-black/[0.09] bg-white/50 px-3.5 py-1.5 font-dm text-[13px] text-[#4a4540] transition-all duration-150 hover:border-[var(--accent)] hover:text-[var(--accent)] dark:border-white/[0.08] dark:bg-[#1e1c18]/50 dark:text-[#b8b0a5]">${item}</a>`,
    )
    .join("");

  root.querySelector("[data-ai-toggle]")?.addEventListener("click", (event) => {
    const full = root.querySelector("[data-ai-full]");
    const short = root.querySelector("[data-ai-short]");
    if (!full || !short) return;
    const open = full.classList.toggle("hidden");
    short.classList.toggle("hidden", !open);
    event.currentTarget.textContent = open ? "Show more" : "Show less";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initSearchBars();
  initResultsPage();
});
