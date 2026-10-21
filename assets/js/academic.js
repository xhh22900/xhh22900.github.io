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

  function setLanguage(language) {
    root.lang = language;
    languageButton.setAttribute('aria-label', english() ? '切换为中文' : 'Switch to English');
    const menuIsOpen = navigation.classList.contains('is-open');
    menuButton.setAttribute('aria-label', menuIsOpen ? label('关闭导航菜单', 'Close menu') : label('打开导航菜单', 'Open menu'));
    search.placeholder = label('搜索标题、作者、期刊或年份', 'Search title, author, journal, year');
    search.setAttribute('aria-label', label('搜索论文', 'Search publications'));
    document.querySelectorAll('.research-link').forEach(button => button.setAttribute('aria-label', label('查看相关论文', 'View related papers')));
    try { localStorage.setItem('hhx-language', language); } catch (_) {}
    updatePapers();
  }

  languageButton.addEventListener('click', () => setLanguage(english() ? 'zh-CN' : 'en'));
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
})();
