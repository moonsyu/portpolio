/** Render the current local HTML into one section per 16:9 PDF page.
 * Uses an isolated headless document renderer; never attaches to a user browser.
 */
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {spawnSync} = require('node:child_process');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');

const root = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
function option(name, fallback) {
  const i = args.indexOf(name);
  return i < 0 ? fallback : args[i + 1];
}
const source = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const sourceVariant = source.includes('name="portfolio-variant" content="web-app"') ? 'web-app' : 'full';
const requestedVariant = option('--variant', 'auto');
const variant = requestedVariant === 'auto' ? sourceVariant : requestedVariant;
if (!['all', 'full', 'web-app'].includes(variant)) throw Error('Unknown PDF variant');
if (sourceVariant === 'web-app' && variant !== 'web-app') throw Error('Build the full PDF from the embedded branch');
const out = path.resolve(option('--output-dir', path.join(root, 'output/pdf')));
const keepWork = option('--work-dir', null);
const work = keepWork ? path.resolve(keepWork) : fs.mkdtempSync(path.join(os.tmpdir(), 'portfolio-pdf-'));
fs.mkdirSync(out, {recursive: true});
fs.mkdirSync(work, {recursive: true});
const css = fs.readFileSync(path.join(root, 'styles.css'), 'utf8');
const exportCss = fs.readFileSync(path.join(__dirname, 'pdf.css'), 'utf8');
const base = pathToFileURL(root + path.sep).href;

async function render(browser, edition) {
  const page = await browser.newPage({viewport: {width: 1440, height: 810}, deviceScaleFactor: 1});
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  // Build only from checked-in content. No app scripts, APIs or external resources.
  await page.route('**/*', route => {
    const url = route.request().url();
    return /^(file:|data:|about:)/.test(url) ? route.continue() : route.abort();
  });
  await page.setContent('<!doctype html><html lang="ko"><head></head><body></body></html>');
  const result = await page.evaluate(({source, sourceVariant, edition, base, css, exportCss}) => {
    const doc = new DOMParser().parseFromString(source, 'text/html');
    const site = doc.querySelector('link[rel="canonical"]').href;
    // Download controls belong to the website, not the exported document.
    doc.querySelectorAll('.hero-actions .button-pdf').forEach(button => button.remove());
    if (edition === 'web-app' && sourceVariant !== 'web-app') {
      doc.querySelector('#stm').remove();
      doc.querySelector('.project-index a[href="#stm"]').remove();
      doc.querySelectorAll('.timeline-item').forEach(row => {
        if (row.textContent.includes('SSAFY')) row.remove();
      });
      doc.querySelectorAll('.skill-group').forEach(group => {
        if (group.querySelector('h3').textContent.includes('임베디드')) group.remove();
      });
      doc.querySelector('#hero-title').innerHTML = 'Java 백엔드 개발<span>모바일 연동 · 클라우드 배포</span>';
      doc.querySelector('.hero-description').innerHTML = 'Java 백엔드 개발과 Android·서버 연동 경험을 바탕으로<br>서비스의 데이터·인증·배포 흐름을 연결하는 개발자, 장문수';
      doc.querySelector('.hero-bottom span').textContent = 'Java Backend · Mobile Integration · Cloud Deployment';
      doc.querySelector('.about-points').innerHTML = '<li>Java 기반 백엔드 서버 개발</li><li>Android·서버 데이터 연동</li><li>데이터베이스 이전·클라우드 배포</li>';
      doc.querySelectorAll('.project-index .index-number').forEach((el, i) => el.textContent = String(i + 1).padStart(2, '0'));
      doc.querySelectorAll('.project-number').forEach((el, i) => el.textContent = String(i + 1).padStart(2, '0'));
    }
    const slides = [];
    const clone = selector => doc.querySelector(selector).cloneNode(true);
    function add(anchor, title, kind, nodes, project = '') {
      const slide = document.createElement('section');
      slide.className = `pdf-slide ${kind}`;
      slide.id = `page-${anchor}`;
      const content = document.createElement('div');
      content.className = 'slide-content';
      nodes.forEach(node => content.append(node));
      slide.append(content);
      document.body.append(slide);
      slides.push({anchor, title, kind, project});
    }
    add('home', '표지', 'cover', [clone('.site-header'), clone('.hero')]);
    add('about', '소개', 'profile white', [clone('#about .section-intro'), clone('.about-grid')]);
    add('skills', '보유 기술 스택', 'skills white', [clone('.skills-section')]);
    add('credentials', '수상 · 자격 · 어학', 'credentials white', [clone('.credentials-layout')]);
    add('projects', '프로젝트', 'project-list', [clone('#projects .section-intro'), clone('.project-index')]);
    doc.querySelectorAll('article.project').forEach(project => {
      const id = project.id;
      const name = project.querySelector('.project-heading h3').textContent;
      add(id, `${name} · 개요`, 'overview', [project.querySelector('.project-heading').cloneNode(true), project.querySelector('.project-overview').cloneNode(true)], name);
      project.querySelectorAll('.detail-section').forEach(section => {
        const anchor = section.getAttribute('aria-labelledby');
        let kind = 'detail-page white';
        if (section.querySelector('.application-architecture')) kind += ' architecture-page';
        if (section.querySelector('.evidence-stack')) kind += ' evidence-stack-page';
        if (section.querySelector('.reflection-status')) kind += ' reflection-page';
        if (section.querySelector('.implementation-list')) kind += ' implementation-page';
        add(anchor, `${name} · ${section.querySelector('h4').textContent}`, kind, [section.cloneNode(true)], name);
      });
    });
    add('contact', '연락처', 'contact-page white', [clone('.contact')]);
    const anchors = new Set(slides.map(slide => slide.anchor));
    document.querySelectorAll('.pdf-slide').forEach((slide, i) => {
      const item = slides[i];
      slide.dataset.anchor = item.anchor;
      slide.dataset.title = item.title;
      slide.querySelectorAll('script').forEach(el => el.remove());
      slide.querySelectorAll('img').forEach(img => {
        img.loading = 'eager';
        const source = img.dataset.poster || img.getAttribute('src');
        img.src = new URL(source, base).href;
      });
      slide.querySelectorAll('button').forEach(button => {
        const link = document.createElement('a');
        link.className = button.className;
        link.href = site + '#' + item.anchor;
        link.innerHTML = button.innerHTML;
        link.setAttribute('aria-label', button.getAttribute('aria-label') || '웹에서 보기');
        button.replaceWith(link);
      });
      // Static GIF frames retain a real link to the interactive original.
      slide.querySelectorAll('img[data-gif]').forEach(img => {
        const label = document.createElement('a');
        label.className = 'pdf-demo-link';
        label.href = site + '#' + item.anchor;
        label.textContent = '실행 GIF 보기 ↗';
        img.closest('figure').append(label);
      });
      slide.querySelectorAll('a').forEach(a => {
        const href = a.getAttribute('href') || '';
        if (href.startsWith('#')) {
          a.href = anchors.has(href.slice(1)) ? `#page-${href.slice(1)}` : site + href;
        } else if (href.startsWith('./')) a.href = new URL(href, site).href;
        a.removeAttribute('download');
      });
      const footer = document.createElement('div');
      footer.className = 'slide-footer';
      const siteAnchor = ['skills', 'credentials'].includes(item.anchor) ? 'about' : item.anchor;
      footer.innerHTML = `<a href="${site}#${siteAnchor}">Jang MoonSu${item.project ? ' · ' + item.project : ' · PORTFOLIO'}</a><span>${String(i + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}</span>`;
      slide.append(footer);
    });
    document.head.innerHTML = '<meta charset="utf-8"><title>장문수 | ' + (edition === 'web-app' ? 'Web & App Portfolio' : 'Developer Portfolio') + '</title>';
    const style = document.createElement('style');
    style.textContent = css + '\n' + exportCss;
    document.head.append(style);
    return {slides, html: '<!doctype html>\n' + document.documentElement.outerHTML};
  }, {source, sourceVariant, edition, base, css, exportCss});
  const htmlPath = path.join(work, `${edition}.html`);
  fs.writeFileSync(htmlPath, result.html);
  await page.goto(pathToFileURL(htmlPath).href);
  await page.emulateMedia({media: 'screen', reducedMotion: 'reduce'});
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(img => img.decode()));
  });
  const layout = await page.evaluate(() => [...document.querySelectorAll('.pdf-slide')].map(slide => {
    const content = slide.querySelector('.slide-content');
    const style = getComputedStyle(content);
    const available = 810 - parseFloat(style.top) - 48;
    const height = content.scrollHeight;
    const scale = Math.min(1, available / height);
    // CSS zoom changes pagination geometry too; transform alone can silently
    // move the last list item onto a clipped fragment during PDF printing.
    const left = parseFloat(style.left);
    const top = parseFloat(style.top);
    const width = parseFloat(style.width);
    content.style.zoom = String(scale);
    content.style.left = `${(left + width * (1 - scale) / 2) / scale}px`;
    content.style.top = `${top / scale}px`;
    const bounds = slide.getBoundingClientRect();
    const broken = [...slide.querySelectorAll('img')].filter(i => !i.complete || !i.naturalWidth).map(i => i.src);
    const outside = [...content.querySelectorAll('img,h1,h2,h3,h4,h5,p,li,dt,dd')].filter(el => {
      const r = el.getBoundingClientRect();
      return r.width && (r.left < bounds.left - 1 || r.right > bounds.right + 1 || r.bottom > bounds.top + 763);
    }).map(el => el.tagName + ':' + el.textContent.trim().slice(0, 80));
    const text = [];
    const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const value = walker.currentNode.textContent.trim();
      if (value) text.push(value);
    }
    return {anchor: slide.dataset.anchor, title: slide.dataset.title, scale, sourceHeight: height, broken, outside, text};
  }));
  const issues = layout.filter(item => item.scale < 0.78 || item.broken.length || item.outside.length);
  fs.writeFileSync(path.join(work, `${edition}-layout.json`), JSON.stringify({slides: result.slides, layout, errors}, null, 2));
  if (issues.length || errors.length) throw Error(JSON.stringify({issues, errors}, null, 2));
  // Save the fitted source as a reproducible preview, without app runtime scripts.
  fs.writeFileSync(htmlPath, '<!doctype html>\n' + await page.content());
  const filename = edition === 'full' ? 'Jang-MoonSu-Portfolio.pdf' : 'Jang-MoonSu-Web-App-Portfolio.pdf';
  const target = path.join(out, filename);
  await page.pdf({path: target, width: '1440px', height: '810px', printBackground: true, preferCSSPageSize: true, tagged: true});
  const check = spawnSync(process.env.PDF_PYTHON || 'python', [path.join(__dirname, 'verify_pdf.py'), target, path.join(work, `${edition}-layout.json`)], {stdio: 'inherit'});
  if (check.error) throw check.error;
  if (check.status !== 0) throw Error(`PDF content verification failed: ${edition}`);
  console.log(JSON.stringify({file: target, pages: result.slides.length, minScale: Math.min(...layout.map(item => item.scale))}));
  await page.close();
}

(async () => {
  const executable = option('--browser-executable', process.env.PDF_BROWSER_EXECUTABLE);
  const launch = {headless: true};
  if (executable) launch.executablePath = executable;
  else if (process.platform === 'win32') launch.channel = 'msedge';
  const browser = await chromium.launch(launch);
  try {
    for (const edition of variant === 'all' ? ['full', 'web-app'] : [variant]) await render(browser, edition);
  } finally {
    await browser.close();
    if (!keepWork) {
      const temporaryRoot = path.resolve(os.tmpdir()) + path.sep;
      if (!path.resolve(work).startsWith(temporaryRoot) || !path.basename(work).startsWith('portfolio-pdf-')) throw Error('Unexpected temporary path');
      fs.rmSync(work, {recursive: true, force: true});
    }
  }
})().catch(error => {console.error(error); process.exitCode = 1;});
