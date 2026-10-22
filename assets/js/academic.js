(() => {
  'use strict';
  const root = document.documentElement;
  const languageButton = document.getElementById('language-toggle');
  const menuButton = document.getElementById('menu-toggle');
  const navigation = document.getElementById('main-nav');
  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const papers = [...document.querySelectorAll('.paper')];
  const search = document.getElementById('paper-search');
  const count = document.getElementById('publication-count');
  const reset = document.getElementById('reset-filter');
  const empty = document.getElementById('empty-state');
  let currentFilter = 'selected';
  let currentField = null;

  const english = () => root.lang === 'en';
  const label = (zh, en) => english() ? en : zh;

  function updatePapers() {
    const query = search.value.trim().toLowerCase();
    root.dataset.publicationView = currentFilter === 'selected' && !currentField && !query ? 'selected' : currentFilter;
    let visible = 0;
    for (const paper of papers) {
      const matchesFilter = currentFilter === 'all' ||
        (currentFilter === 'selected' && paper.dataset.selected === 'true') ||
        (currentFilter === 'first' && paper.dataset.first === 'true') ||
        (currentFilter === 'quantum' && paper.dataset.field === 'quantum');
      const matchesField = !currentField || paper.dataset.field === currentField;
      const matchesQuery = !query || paper.dataset.search.includes(query);
      const show = matchesFilter && matchesField && matchesQuery;
      paper.hidden = !show;
      if (show) visible++;
    }
    filterButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === currentFilter)));
    const fieldNames = {nuclear: label('核结构', 'nuclear structure'), atomic: label('原子物理', 'atomic physics'), quantum: label('量子信息', 'quantum information')};
    const suffix = currentField ? ` · ${fieldNames[currentField]}` : '';
    count.textContent = label(`显示 ${visible} / ${papers.length} 篇已发表论文`, `Showing ${visible} of ${papers.length} published papers`) + suffix;
    reset.hidden = currentFilter === 'selected' && !currentField && !query;
    empty.hidden = visible !== 0;
  }

  function revealWorkTarget(id, {focus = false, behavior = 'instant'} = {}) {
    const target = document.getElementById(id);
    if (!target || !target.matches('.paper, .manuscript, #scattering-method')) return;
    if (target.classList.contains('paper') && target.hidden) {
      currentFilter = 'all';
      currentField = null;
      search.value = '';
      updatePapers();
    }
    requestAnimationFrame(() => {
      target.scrollIntoView({block: 'start', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : behavior});
      if (focus) target.focus({preventScroll: true});
    });
  }

  function revealWorkFromHash() {
    try { revealWorkTarget(decodeURIComponent(location.hash.slice(1))); } catch (_) {}
  }

  function setLanguage(language) {
    root.lang = language;
    document.title = label('谢辉辉 Hui Hui Xie · 核结构与精密原子物理', 'Hui Hui Xie · Nuclear Structure & Precision Atomic Physics');
    languageButton.setAttribute('aria-label', english() ? '切换为中文' : 'Switch to English');
    const menuIsOpen = navigation.classList.contains('is-open');
    menuButton.setAttribute('aria-label', menuIsOpen ? label('关闭导航菜单', 'Close menu') : label('打开导航菜单', 'Open menu'));
    search.placeholder = label('搜索标题、作者、期刊或年份', 'Search title, author, journal, year');
    search.setAttribute('aria-label', label('搜索论文', 'Search publications'));
    document.querySelectorAll('.research-link').forEach(button => button.setAttribute('aria-label', label('查看相关论文', 'View related papers')));
    document.querySelectorAll('.copy-feedback').forEach(status => { status.textContent = ''; });
    try { localStorage.setItem('hhx-language', language); } catch (_) {}
    updatePapers();
  }

  languageButton.addEventListener('click', () => {
    const headerBottom = document.querySelector('.site-header').getBoundingClientRect().bottom;
    const anchor = [...document.querySelectorAll('main section[id]')].find(section => section.getBoundingClientRect().bottom > headerBottom + 12);
    const beforeTop = anchor ? anchor.getBoundingClientRect().top : 0;
    setLanguage(english() ? 'zh-CN' : 'en');
    // Preserve the reading position when translated paragraphs change the layout.
    if (anchor) requestAnimationFrame(() => requestAnimationFrame(() => {
      const shift = anchor.getBoundingClientRect().top - beforeTop;
      if (Math.abs(shift) > 1) window.scrollBy({top: shift, behavior: 'instant'});
    }));
  });
  document.querySelectorAll('[data-copy-bib]').forEach(button => button.addEventListener('click', async () => {
    const text = document.getElementById(button.dataset.copyBib).textContent;
    const status = button.parentElement.querySelector('.copy-feedback');
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const field = document.createElement('textarea');
        field.value = text;
        field.setAttribute('readonly', '');
        field.style.position = 'fixed';
        field.style.opacity = '0';
        document.body.append(field);
        field.select();
        const copied = document.execCommand('copy');
        field.remove();
        if (!copied) throw new Error('Clipboard unavailable');
      }
      status.textContent = label('已复制', 'Copied');
    } catch (_) {
      status.textContent = label('复制失败，请选择下方文本或下载 .bib', 'Select the text below or download the .bib file');
    }
  }));
  document.querySelectorAll('.diagram-work-link').forEach(link => link.addEventListener('click', event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const id = decodeURIComponent(link.hash.slice(1));
    if (!document.getElementById(id)) return;
    event.preventDefault();
    try {
      if (location.hash !== link.hash) history.pushState(null, '', link.hash);
    } catch (_) {
      location.hash = link.hash;
      return;
    }
    revealWorkTarget(id, {focus: true, behavior: 'smooth'});
  }));
  window.addEventListener('hashchange', revealWorkFromHash);
  filterButtons.forEach(button => button.addEventListener('click', () => {
    currentFilter = button.dataset.filter;
    currentField = null;
    updatePapers();
  }));
  search.addEventListener('input', () => {
    // Searching examines the full catalogue; a representative-paper filter must not hide a match.
    if (search.value.trim()) { currentFilter = 'all'; currentField = null; }
    updatePapers();
  });
  reset.addEventListener('click', () => {
    currentFilter = 'selected'; currentField = null; search.value = ''; updatePapers();
  });
  document.querySelectorAll('.research-link').forEach(button => button.addEventListener('click', () => {
    currentField = button.dataset.field;
    currentFilter = currentField === 'quantum' ? 'quantum' : 'all';
    search.value = '';
    updatePapers();
    document.getElementById('publications').scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
  }));

  function closeMenu() { navigation.classList.remove('is-open'); menuButton.setAttribute('aria-expanded', 'false'); menuButton.setAttribute('aria-label', label('打开导航菜单', 'Open menu')); }
  menuButton.addEventListener('click', () => {
    const open = !navigation.classList.contains('is-open');
    navigation.classList.toggle('is-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? label('关闭导航菜单', 'Close menu') : label('打开导航菜单', 'Open menu'));
  });
  navigation.querySelectorAll('a').forEach(anchor => anchor.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
  if ('IntersectionObserver' in window) {
    const links = [...navigation.querySelectorAll('a')];
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) if (entry.isIntersecting) {
        links.forEach(link => link.classList.toggle('is-current', link.getAttribute('href') === `#${entry.target.id}`));
      }
    }, {rootMargin: '-15% 0px -65% 0px', threshold: 0});
    document.querySelectorAll('main section[id]').forEach(section => observer.observe(section));
  }
  setLanguage(english() ? 'en' : 'zh-CN');
  revealWorkFromHash();
})();
