/* Run after ./build.sh build, with Playwright available to Node:
 * NODE_PATH=experiment/graph-browser/node_modules \
 * PLAYWRIGHT_BROWSERS_PATH=experiment/graph-browser/browsers \
 * experiment/graph-browser/node_modules/node/bin/node tests/document-graph.browser.cjs
 * Optional GRAPH_SCREENSHOTS=experiment/graph-browser saves preview images.
 */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
(async () => {
  const site = path.resolve('site');
  const server = http.createServer(async (req, res) => {
    try {
      const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
      const file = path.resolve(site, '.' + pathname + (pathname.endsWith('/') ? 'index.html' : ''));
      if (!file.startsWith(site + path.sep)) throw new Error('Invalid path');
      const types = {'.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json'};
      res.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
      res.end(await fs.readFile(file));
    } catch { res.writeHead(404).end(); }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  try {
    browser = await chromium.launch({headless: true});
    const origin = `http://127.0.0.1:${server.address().port}`;
    const page = await browser.newPage({viewport: {width: 1440, height: 1100}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.route('**/*', route => route.request().url().startsWith(origin) ? route.continue() : route.abort());
    await page.goto(origin);
    const graph = page.locator('.document-graph');
    await graph.scrollIntoViewIfNeeded();
    await page.waitForTimeout(400);
    assert.equal(await graph.locator('input, button, p').count(), 0);
    const count = await graph.locator('.node').count();
    assert(count > 60);
    async function screenshot(name) {
      if (process.env.GRAPH_SCREENSHOTS) await graph.screenshot({path: `${process.env.GRAPH_SCREENSHOTS}/${name}.png`});
    }
    await screenshot('overview');
    const id = await graph.locator('.node[data-depth="0"]').first().getAttribute('data-id');
    const target = graph.locator(`[data-id="${id}"]`);
    const oldRadius = await target.locator('.main-circle').getAttribute('r');
    const oldTransform = await graph.locator('svg > g').getAttribute('transform');
    await target.locator('text').click();
    await page.waitForTimeout(160);
    const midTransform = await graph.locator('svg > g').getAttribute('transform');
    assert.notEqual(midTransform, oldTransform, 'camera moves during animation');
    await page.waitForTimeout(800);
    const endTransform = await graph.locator('svg > g').getAttribute('transform');
    assert.notEqual(midTransform, endTransform, 'camera does not jump immediately');
    assert.equal(await graph.getAttribute('data-center'), id);
    assert.equal(Number(await target.locator('.main-circle').getAttribute('r')), Number(oldRadius) * 1.5);
    assert.equal(await graph.locator('.node').count(), count, 'focus preserves the surrounding graph');
    const isCentered = () => target.evaluate(el => {
      const node = el.querySelector('.main-circle').getBoundingClientRect();
      const svg = el.closest('svg').getBoundingClientRect();
      return Math.hypot(node.x + node.width / 2 - svg.x - svg.width / 2, node.y + node.height / 2 - svg.y - svg.height / 2) < 2;
    });
    assert(await isCentered());
    await screenshot('focused');
    const box = await graph.boundingBox();
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await page.mouse.wheel(0, -350);
    await page.waitForTimeout(400);
    const screenFont = await target.locator('text').evaluate(el => parseFloat(getComputedStyle(el).fontSize) * el.getScreenCTM().a);
    assert(Math.abs(screenFont - 14) < .1, 'zoom preserves readable label size');
    const beforePan = await graph.locator('svg > g').getAttribute('transform');
    await page.mouse.move(box.x + 10, box.y + 10);
    await page.mouse.down(); await page.mouse.move(box.x + 70, box.y + 50, {steps: 10}); await page.mouse.up();
    assert.notEqual(await graph.locator('svg > g').getAttribute('transform'), beforePan);
    await target.focus(); await page.keyboard.press('Space'); await page.waitForTimeout(850);
    assert(await isCentered());
    const beforeDrag = await target.getAttribute('transform');
    const circle = await target.locator('.main-circle').boundingBox();
    await page.mouse.move(circle.x + circle.width / 2, circle.y + circle.height / 2);
    await page.mouse.down(); await page.mouse.move(circle.x + 90, circle.y + 70, {steps: 12}); await page.mouse.up();
    assert.notEqual(await target.getAttribute('transform'), beforeDrag);
    assert.equal(await graph.getAttribute('data-center'), id, 'drag does not trigger another selection');
    // Keyboard can reach any document even if outside the current viewport.
    const articleId = await graph.locator('.node[data-depth="2"]').first().getAttribute('data-id');
    const article = graph.locator(`[data-id="${articleId}"]`);
    await article.focus(); await page.keyboard.press('Space'); await page.waitForTimeout(850);
    assert.equal(await graph.getAttribute('data-center'), await article.getAttribute('data-id'));
    await article.locator('.main-circle').dblclick();
    await page.waitForURL(url => url.pathname !== '/');
    await page.goBack(); await page.waitForTimeout(500);
    assert.equal(await page.locator('.document-graph .node').count(), count);
    assert.deepEqual(errors, []);
    const mobile = await browser.newPage({viewport: {width: 390, height: 844}, isMobile: true, hasTouch: true, reducedMotion: 'reduce'});
    await mobile.route('**/*', route => route.request().url().startsWith(origin) ? route.continue() : route.abort());
    mobile.on('pageerror', error => errors.push(error.message));
    await mobile.goto(origin);
    await mobile.locator('.document-graph').scrollIntoViewIfNeeded();
    const mobileId = await mobile.locator('.document-graph .node[data-depth="0"]').first().getAttribute('data-id');
    const mobileTarget = mobile.locator(`.document-graph [data-id="${mobileId}"]`);
    await mobileTarget.locator('.main-circle').tap();
    await mobile.waitForTimeout(100);
    assert.equal(await mobile.locator('.document-graph').getAttribute('data-center'), await mobileTarget.getAttribute('data-id'));
    await mobile.setViewportSize({width: 430, height: 900});
    await mobile.waitForTimeout(200);
    assert(await mobileTarget.evaluate(el => {
      const circle = el.querySelector('.main-circle').getBoundingClientRect();
      const svg = el.closest('svg').getBoundingClientRect();
      return Math.abs(circle.x + circle.width / 2 - svg.x - svg.width / 2) < 2;
    }));
    await mobile.evaluate(() => document.body.setAttribute('data-md-color-scheme', 'slate'));
    if (process.env.GRAPH_SCREENSHOTS) await mobile.locator('.document-graph').screenshot({path: `${process.env.GRAPH_SCREENSHOTS}/mobile-dark.png`});
    assert.deepEqual(errors, []);
    console.log('PASS: animated focus, labels, node sizing, zoom, pan, drag, keyboard, navigation, mobile tap/resize, reduced motion; no browser errors.');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
