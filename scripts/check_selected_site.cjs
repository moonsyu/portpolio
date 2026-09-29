// Isolated local-site regression checks. Never reads the user's browser profile.
const http = require('node:http');
const fs = require('node:fs/promises');
const path = require('node:path');
const assert = require('node:assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const output=process.env.PORTFOLIO_SITE_REVIEW || path.resolve(root,'../portpolio-work/site-review');
const mime={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.webp':'image/webp','.gif':'image/gif','.woff':'font/woff','.pdf':'application/pdf'};
const server=http.createServer(async(req,res)=>{
  try{
    const requested=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    const file=path.resolve(root,'.'+(requested==='/'?'/index.html':requested));
    if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
    const data=await fs.readFile(file);res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(data);
  }catch{res.writeHead(404);res.end();}
});
(async()=>{
  await fs.mkdir(output,{recursive:true});
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const browser=await chromium.launch({headless:true,executablePath:process.env.PORTFOLIO_TEST_BROWSER || 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const errors=[];
  const page=await browser.newPage({viewport:{width:1600,height:1000},reducedMotion:'reduce'});
  page.on('pageerror',e=>errors.push(e.message));
  page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
  try{
    await page.goto(`http://127.0.0.1:${server.address().port}`,{waitUntil:'networkidle'});
    // Keep captures still while changing sections; production smooth scrolling is unchanged.
    await page.addStyleTag({content:'html{scroll-behavior:auto!important}'});
    await page.evaluate(async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});
    assert.equal(await page.locator('.profile-heading').count(),1);
    assert.equal(await page.locator('#stm .slide-surface').count(),4);
    assert.equal(await page.locator('#credentials .award-list li').count(),6);
    assert.equal(await page.locator('#skills .skill-icons li').count(),16);
    const arch=page.locator('#stm img[src$="stm-application.svg"]');
    assert.equal(await arch.count(),1);
    const sourceChecks=await page.evaluate(()=>({
      profile:document.querySelector('.profile-heading').getBoundingClientRect().x,
      intro:document.querySelector('.intro-copy').getBoundingClientRect().x,
      timeline:getComputedStyle(document.querySelector('.timeline-item')).display,
      headingColor:getComputedStyle(document.querySelector('h1')).color,
      bodyColor:getComputedStyle(document.body).color,
      fonts:document.fonts.check('600 22px "Noto Sans KR"'),
    }));
    assert(sourceChecks.profile<sourceChecks.intro);
    assert.equal(sourceChecks.timeline,'grid');
    assert.equal(sourceChecks.headingColor,'rgb(25, 95, 206)');
    assert.equal(sourceChecks.bodyColor,'rgb(25, 72, 120)');
    assert(sourceChecks.fonts);
    const slides=page.locator('#home .slide-surface,#about .slide-surface,#skills .slide-surface,#credentials .slide-surface,#stm .slide-surface');
    assert.equal(await slides.count(),8);
    for(let i=0;i<8;i++)await slides.nth(i).screenshot({path:path.join(output,`desktop-${i+1}.png`),animations:'disabled'});
    await page.locator('#about').scrollIntoViewIfNeeded();
    await page.waitForFunction(()=>document.querySelector('nav a[href="#home"]').getAttribute('aria-current')==='location');
    await arch.scrollIntoViewIfNeeded();
    await page.locator('#stm [data-diagram]').click();
    await page.waitForFunction(()=>document.querySelector('.image-dialog').open && document.querySelector('.image-dialog img').complete);
    const view=page.locator('.dialog-viewport');
    const box=await view.boundingBox();
    const img=page.locator('.image-dialog img');
    const first=await img.getAttribute('style');
    await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.wheel(0,-160);
    await page.waitForFunction(()=>document.querySelector('.image-dialog img').style.transform.includes('scale(1.') );
    assert.notEqual(await img.getAttribute('style'),first);
    const zoomed=await img.getAttribute('style');
    await page.mouse.down();await page.mouse.move(box.x+box.width/2+85,box.y+box.height/2+30,{steps:4});await page.mouse.up();
    assert.notEqual(await img.getAttribute('style'),zoomed);
    await page.keyboard.press('0');await page.keyboard.press('Escape');
    assert.equal(await page.locator('.image-dialog').evaluate(d=>d.open),false);
    const gif=page.locator('[data-demo-toggle="stm-demo"]');
    const old=await gif.getAttribute('aria-pressed');await gif.click();assert.notEqual(await gif.getAttribute('aria-pressed'),old);await gif.click();
    for(const width of [1280,900,768,390,360]){
      await page.setViewportSize({width,height:900});
      const overflow=await page.evaluate(()=>[...document.querySelectorAll('main h1,main h2,main h3,main h4,main p,main li,main dd,.slide-surface')].filter(e=>e.getBoundingClientRect().width && (e.getBoundingClientRect().right>innerWidth+2 || e.getBoundingClientRect().left < -2)).map(e=>({tag:e.tagName,text:e.textContent.slice(0,70)})));
      assert.deepEqual(overflow,[],`Horizontal overflow at ${width}px: ${JSON.stringify(overflow)}`);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true);
      if(width===390){
        await page.locator('#home').screenshot({path:path.join(output,'mobile-intro.png'),animations:'disabled'});
        await page.locator('#credentials').screenshot({path:path.join(output,'mobile-credentials.png'),animations:'disabled'});
      }
    }
    assert.deepEqual(errors,[]);
    await fs.writeFile(path.join(output,'checks.json'),JSON.stringify({sourceChecks,widths:[1600,1280,900,768,390,360],slides:8,imageZoomPan:true,gifToggle:true,errors},null,2));
    console.log('PASS: 8 sections, selected layouts, blue text, 6 viewport widths, local fonts, original SVG, zoom/pan, GIF, anchors, no network/JS errors');
  }finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
