// Titles stay visible before the observer runs, including with JavaScript disabled.
if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const titles = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('type-arrive');
        titles.unobserve(entry.target);
      }
    }
  });
  document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(title => titles.observe(title));
}
document.addEventListener('click', event => {
  for (const menu of document.querySelectorAll('.projects-menu[open]')) {
    if (!menu.contains(event.target) || event.target.closest('a')) menu.open = false;
  }
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') {
    const menu = document.querySelector('.projects-menu[open]');
    if (menu) { menu.open = false; menu.querySelector('summary').focus(); }
  }
});

// Load each short motion study only when its cover becomes visible.
const coverMotionPreference = matchMedia('(prefers-reduced-motion: reduce)');
if ('IntersectionObserver' in window) {
  const covers = document.querySelectorAll('.original-hero img[data-motion]');
  const originals = new Map(Array.from(covers, image => [image, image.getAttribute('src')]));
  const observer = new IntersectionObserver(entries => {
    for (const {target, isIntersecting} of entries) {
      if (isIntersecting && !coverMotionPreference.matches) {
        observer.unobserve(target);
        const clip = new Image();
        clip.onload = () => {
          if (coverMotionPreference.matches) return;
          target.src = clip.src;
          setTimeout(() => target.setAttribute('src', originals.get(target)), 3350);
        };
        clip.src = target.dataset.motion;
      }
    }
  }, {threshold:.25});
  function setMotion() {
    observer.disconnect();
    for (const image of covers) {
      if (coverMotionPreference.matches) image.setAttribute('src', originals.get(image));
      else observer.observe(image);
    }
  }
  setMotion();
  coverMotionPreference.addEventListener('change', setMotion);
}
