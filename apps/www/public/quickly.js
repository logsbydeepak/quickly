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

function applyTheme(theme) {
  document.documentElement.classList.toggle("dark", theme === "dark");
  localStorage.setItem(STORAGE_KEY, theme);
  document.querySelectorAll("[data-theme-label]").forEach((label) => {
    label.textContent = theme === "light" ? "Dark" : "Light";
  });
  document
    .querySelectorAll("[data-theme-moon]")
    .forEach((icon) => icon.classList.toggle("hidden", theme !== "light"));
  document
    .querySelectorAll("[data-theme-sun]")
    .forEach((icon) => icon.classList.toggle("hidden", theme === "light"));
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

function targetFor(query) {
  return `/results?q=${encodeURIComponent(query.trim())}`;
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
      window.location.href = targetFor(CHIPS[Math.floor(Math.random() * CHIPS.length)]);
    });
  });
}

function cap(value) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function makeResults(query) {
  const first = query.split(" ")[0];
  return [
    {
      id: 1,
      url: "en.wikipedia.org",
      displayUrl: `en.wikipedia.org > wiki > ${first}`,
      title: `${cap(query)} - Wikipedia`,
      snippet: `${cap(query)} refers to a concept widely studied across many disciplines. First documented in the early 20th century, it has evolved considerably and now encompasses multiple fields of study including science, technology, and culture.`,
    },
    {
      id: 2,
      url: "www.quickly.com",
      displayUrl: "quickly.com > results",
      title: `Quickly finds: ${query} - Top results`,
      snippet: `Our fastest search results for "${query}". Quickly indexes the web in real-time so you always get the most up-to-date information. Try our new AI-powered summary feature.`,
      featured: true,
    },
    {
      id: 3,
      url: "www.britannica.com",
      displayUrl: "britannica.com > topic",
      title: `${cap(query)}: Definition, History & Facts | Britannica`,
      snippet: `Comprehensive encyclopedia entry covering the history, definition, and key facts about ${query}. Britannica has been the world's most trusted source of knowledge since 1768.`,
    },
    {
      id: 4,
      url: "www.reddit.com",
      displayUrl: "reddit.com > r > all > search",
      title: `Reddit - Community discussions about ${query}`,
      snippet: `Thousands of community discussions about "${query}" across Reddit. See what real people think, share experiences, and get answers from those who know.`,
    },
    {
      id: 5,
      url: "medium.com",
      displayUrl: `medium.com > tagged > ${query.replace(/ /g, "-")}`,
      title: `The Complete Guide to ${cap(query)} (2026)`,
      snippet: `Everything you need to know about ${query} in 2026. Covers fundamentals, advanced techniques, and practical applications that experts actually use day-to-day.`,
    },
    {
      id: 6,
      url: "stackoverflow.com",
      displayUrl: "stackoverflow.com > questions",
      title: `Questions tagged [${first}] - Stack Overflow`,
      snippet: `Browse questions tagged with ${first} on Stack Overflow. Ask questions, get answers, and collaborate with developers worldwide.`,
    },
    {
      id: 7,
      url: "www.youtube.com",
      displayUrl: "youtube.com > results",
      title: `${cap(query)} - YouTube`,
      snippet: `Watch videos about ${query} on YouTube. From tutorials to deep-dive documentaries, millions of creators have covered this topic for audiences everywhere.`,
    },
    {
      id: 8,
      url: "news.ycombinator.com",
      displayUrl: "news.ycombinator.com > item",
      title: `Ask HN: Best resource for learning about ${query}?`,
      snippet: `Hacker News thread where community members share their top resources, books, courses, and tools for going deep on ${query}.`,
    },
  ];
}

function initResultsPage() {
  const root = document.querySelector("[data-results-page]");
  if (!root) return;
  const params = new URLSearchParams(window.location.search);
  const query = params.get("q") || "Trending";
  const time = (Math.random() * 0.4 + 0.08).toFixed(2);
  const resultCount = (Math.random() * 900 + 100).toFixed(0);
  const results = makeResults(query);

  document.title = `${query} - Quickly`;
  root.querySelector("[data-search-input]").value = query;
  root.querySelector("[data-stats]").innerHTML =
    `About <strong class="font-medium text-[#4a4540] dark:text-[#b8b0a5]">${resultCount} million</strong> results <span class="mx-1.5 opacity-40">.</span>(${time}s)`;
  root.querySelector("[data-ai-query]").textContent = cap(query);
  root.querySelector("[data-ai-full]").textContent =
    `${cap(query)} is a multifaceted topic with roots in numerous academic and practical disciplines. It encompasses a broad range of concepts including theoretical frameworks, real-world applications, and ongoing research. Key aspects include its historical development, current state of understanding, and future directions. Researchers and practitioners continue to explore its implications across various fields, yielding new insights regularly.`;
  root.querySelector("[data-panel-title]").textContent = cap(query);
  root.querySelector("[data-panel-image]").innerHTML = `image placeholder<br>${query}`;
  root.querySelector("[data-speed]").textContent = `${time}s`;
  root.querySelector("[data-found]").textContent = `${Math.floor(Math.random() * 900) + 100}M`;

  const list = root.querySelector("[data-results-list]");
  list.innerHTML = results
    .map((item, index) => {
      const dom = item.url.split("/")[0];
      const featured = item.featured;
      return `<article class="group animate-result-slide r${index} cursor-pointer transition-all duration-150 ${featured ? "mb-1 rounded-xl border-[1.5px] border-black/[0.09] bg-white/70 p-5 shadow-sm backdrop-blur-sm hover:border-[var(--accent)] hover:bg-[var(--accent-soft)] dark:border-white/[0.08] dark:bg-[#1e1c18]/70" : "border-b border-black/[0.07] py-3.5 dark:border-white/[0.06]"}">
      <div class="mb-1.5 flex flex-wrap items-center gap-2">
        <img src="https://www.google.com/s2/favicons?domain=${dom}&sz=32" width="15" height="15" class="shrink-0 rounded-[3px]" alt="">
        <span class="max-w-[320px] truncate text-[13px] font-light text-[#8a837a] dark:text-[#6e6760]">${item.displayUrl}</span>
        ${featured ? `<span class="shrink-0 rounded-full bg-[var(--accent-soft)] px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-[var(--accent)]">Top pick</span>` : ""}
      </div>
      <h3 class="mb-1.5 font-dm text-[17px] font-medium leading-snug text-[oklch(0.48_0.18_245)] transition-colors duration-150 group-hover:text-[var(--accent)] group-hover:underline group-hover:underline-offset-2 dark:text-[oklch(0.70_0.16_245)]">${item.title}</h3>
      <p class="max-w-[680px] text-[13.5px] font-light leading-relaxed text-[#4a4540] dark:text-[#b8b0a5]">${item.snippet}</p>
    </article>`;
    })
    .join("");

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

  root.querySelector("[data-ai-toggle]").addEventListener("click", (event) => {
    const full = root.querySelector("[data-ai-full]");
    const short = root.querySelector("[data-ai-short]");
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
