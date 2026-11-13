(() => {
 const section = document.querySelector('.about-biography');
 if (!section || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
 let running = false, visible = false, timer, scrollTimer;
 const play = () => {
   if (!visible || running) return;
   running = true;
   section.classList.remove('bio-highlights-running');
   void section.offsetWidth;
   section.classList.add('bio-highlights-running');
   clearTimeout(timer);
   timer = setTimeout(() => { running = false; }, 2200);
 };
 new IntersectionObserver(entries => {
   visible = entries[0].isIntersecting;
   if (visible) play();
 }, {threshold: 0.15}).observe(section);
 addEventListener('scroll', () => {
   clearTimeout(scrollTimer);
   scrollTimer = setTimeout(play, 180);
 }, {passive:true});
})();
