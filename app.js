const dialog = document.querySelector('.image-dialog');
const dialogImage = dialog.querySelector('img');
const dialogCaption = dialog.querySelector('#image-caption');
document.querySelectorAll('[data-enlarge]').forEach(button => {
  button.addEventListener('click', () => {
    const image = button.querySelector('img');
    dialogImage.src = image.src;
    dialogImage.alt = image.alt;
    dialogCaption.textContent = image.alt;
    dialog.showModal();
  });
});
dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  const box = dialog.getBoundingClientRect();
  if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
});
const sections = document.querySelectorAll('main > section[id], footer[id]');
const navigation = document.querySelectorAll('nav a[href^="#"]');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navigation.forEach(link => {
        if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
  });
}, { rootMargin: '-10% 0px -65% 0px', threshold: 0 });
sections.forEach(section => observer.observe(section));
