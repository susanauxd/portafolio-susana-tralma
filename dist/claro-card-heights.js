(() => {
  const desktop = matchMedia('(min-width: 761px)');
  for (const row of document.querySelectorAll('.claro-row')) {
    const card = row.querySelector('.regcheq-copy');
    const content = card.querySelector('.claro-card-content');
    const media = [...row.lastElementChild.querySelectorAll('img')];
    if (row.lastElementChild.matches('video')) media.push(row.lastElementChild);
    if (!media.length) continue;

    function align() {
      if (!desktop.matches) return;
      const boxes = media.map(element => element.getBoundingClientRect());
      const top = Math.min(...boxes.map(box => box.top));
      const height = Math.max(...boxes.map(box => box.bottom)) - top;
      const style = getComputedStyle(card);
      const natural = content.offsetHeight + parseFloat(style.paddingTop) + parseFloat(style.paddingBottom);
      const tall = height >= 2 * natural;
      card.classList.toggle('tall-media', tall);
      card.style.setProperty('--paired-height', tall ? 'auto' : height + 'px');
      card.style.setProperty('--paired-top', Math.max(0, top - row.getBoundingClientRect().top) + 'px');
    }

    const observer = new ResizeObserver(align);
    [content, ...media].forEach(element => observer.observe(element));
    desktop.addEventListener('change', align);
    document.fonts.ready.then(align);
    align();
  }
})();
