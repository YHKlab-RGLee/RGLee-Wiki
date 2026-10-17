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
    assert.equal(await graph.locator('button').count(), 1);
    const colors = await graph.locator('.node').evaluateAll(nodes => {
      const branches = new Map();
      for (const node of nodes) {
        const branch = node.dataset.branch;
        const color = getComputedStyle(node.querySelector('.main-circle')).fill;
        if (branches.has(branch) && branches.get(branch) !== color) throw new Error('Inconsistent branch color');
        branches.set(branch, color);
      }
      return [...branches.values()];
    });
    assert.equal(new Set(colors).size, colors.length, 'top-level branches have distinct colors');
    const hierarchy = await graph.locator('.node').evaluateAll(nodes => [0, 1, 2].map(depth => {
      const node = nodes.find(n => Number(n.dataset.depth) === depth);
      return {radius: Number(node.querySelector('.main-circle').getAttribute('r')),
        font: parseFloat(getComputedStyle(node.querySelector('text')).fontSize)};
    }));
    assert(hierarchy[0].radius > hierarchy[1].radius && hierarchy[1].radius > hierarchy[2].radius);
    assert(hierarchy[0].font > hierarchy[1].font && hierarchy[1].font > hierarchy[2].font);
    async function assertTopicLabels(root) {
      const result = await root.locator('.node[data-depth="1"] text').evaluateAll(labels => {
        const boxes = labels.map(el => el.getBoundingClientRect());
        return {
          visible: labels.every(el => getComputedStyle(el).visibility === 'visible'),
          overlap: boxes.some((a, i) => boxes.slice(i + 1).some(b =>
            a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top))
        };
      });
      assert(result.visible, 'overview shows every topic label');
      assert(!result.overlap, 'topic labels do not overlap each other');
    }
    await assertTopicLabels(graph);
    const count = await graph.locator('.node').count();
    assert(count > 60);
    const layoutState = () => graph.evaluate(root => ({
      camera: root.querySelector('svg > g').getAttribute('transform'),
      nodes: [...root.querySelectorAll('.node')].map(el => ({
        id: el.dataset.id, position: el.getAttribute('transform'),
        label: el.querySelector('text').style.visibility === 'visible'
          ? el.querySelector('text').getAttribute('transform') : null,
        visibility: el.querySelector('text').style.visibility
      })).sort((a, b) => a.id.localeCompare(b.id))
    }));
    const initialLayout = await layoutState();
    const clusters = await graph.locator('.node').evaluateAll(elements => {
      const nodes = elements.map(el => el.__data__);
      return [...new Set(nodes.map(n => n.branch))].map(branch => {
        const members = nodes.filter(n => n.branch === branch);
        const outside = nodes.filter(n => n.branch !== branch);
        const averageDistance = pairs => pairs.reduce((sum, [a, b]) =>
          sum + Math.hypot(a.x - b.x, a.y - b.y), 0) / pairs.length;
        return {
          within: averageDistance(members.flatMap((a, i) => members.slice(i + 1).map(b => [a, b]))),
          between: averageDistance(members.flatMap(a => outside.map(b => [a, b])))
        };
      });
    });
    for (const cluster of clusters) {
      assert(cluster.within < cluster.between * .65, 'each category forms a recognizable initial cluster');
    }
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
    async function checkNeighborhood(center) {
      const state = await graph.evaluate((root, center) => {
        const data = JSON.parse(root.querySelector('.document-graph__data').textContent);
        const neighbors = new Set([center]);
        for (const edge of data.edges) {
          if (edge.source === center) neighbors.add(edge.target);
          if (edge.target === center) neighbors.add(edge.source);
        }
        const parents = new Map(data.edges.filter(e => e.kind === 'tree').map(e => [e.target, e.source]));
        const ancestorChildren = new Set();
        let child = center;
        while (parents.has(child)) {
          ancestorChildren.add(child);
          child = parents.get(child);
          neighbors.add(child);
        }
        return [...root.querySelectorAll('.node')].every(node =>
          node.classList.contains('muted') === !neighbors.has(node.dataset.id)) &&
          [...root.querySelectorAll('.link')].every(line => {
            const edge = line.__data__;
            const active = edge.source.id === center || edge.target.id === center ||
              (edge.kind === 'tree' && ancestorChildren.has(edge.target.id));
            return line.classList.contains('connected') === active && line.classList.contains('muted') === !active;
          });
      }, center);
      assert(state, 'the center, direct neighbors, ancestors and the path to the root stay active');
      assert(await graph.locator('.node.muted').count() > 0);
      assert(await graph.locator('.link.muted').count() > 0);
    }
    await checkNeighborhood(id);
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
    assert(Math.abs(screenFont - 20) < .1, 'zoom preserves readable label size');
    const beforePan = await graph.locator('svg > g').getAttribute('transform');
    await page.mouse.move(box.x + 10, box.y + 80);
    await page.mouse.down(); await page.mouse.move(box.x + 70, box.y + 120, {steps: 10}); await page.mouse.up();
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
    await checkNeighborhood(articleId);
    await graph.locator('.document-graph__reset').click();
    assert.equal(await graph.getAttribute('data-center'), null);
    assert.equal(await graph.locator('.muted, .current, .connected').count(), 0);
    assert.equal(await graph.locator('[aria-pressed="true"]').count(), 0);
    assert.deepEqual(await layoutState(), initialLayout,
      'reset restores initial node positions, camera and labels after dragging and zooming');
    await graph.locator('.document-graph__reset').click();
    await page.waitForTimeout(150);
    assert.deepEqual(await layoutState(), initialLayout, 'repeated reset stays at the initial layout');
    await article.focus(); await page.keyboard.press('Space'); await page.waitForTimeout(850);
    const articleBox = await article.locator('.main-circle').boundingBox();
    const startX = articleBox.x + articleBox.width / 2, startY = articleBox.y + articleBox.height / 2;
    const beforeHold = await graph.locator('.node').evaluateAll(nodes => nodes.map(n => n.getAttribute('transform')));
    await page.mouse.move(startX, startY);
    await page.mouse.down();
    await page.waitForTimeout(450);
    await page.mouse.move(startX + 3, startY + 2);
    await page.waitForTimeout(100);
    assert.deepEqual(await graph.locator('.node').evaluateAll(nodes => nodes.map(n => n.getAttribute('transform'))),
      beforeHold, 'holding and slight jitter do not restart the layout');
    await page.mouse.up();
    await page.waitForTimeout(850);
    assert.equal(new URL(page.url()).pathname, '/', 'single click on the selected article does not navigate');
    await article.locator('.main-circle').dblclick();
    await page.waitForURL(url => url.pathname !== '/');
    await page.goBack(); await page.waitForTimeout(500);
    assert.equal(await page.locator('.document-graph .node').count(), count);
    for (const title of ['Computational science', 'Model reduction']) {
      const section = graph.locator('.node').filter({has: page.locator('title', {hasText: title + ' —'})});
      const url = await section.evaluate(el => el.__data__.url);
      assert(url, 'section has its index URL');
      await section.focus(); await page.keyboard.press('Space'); await page.waitForTimeout(850);
      await section.locator('.main-circle').dblclick();
      await page.waitForURL(new URL(url, origin).href);
      await page.goBack(); await page.waitForTimeout(500);
    }
    assert.deepEqual(errors, []);
    const mobile = await browser.newPage({viewport: {width: 390, height: 844}, isMobile: true, hasTouch: true, reducedMotion: 'reduce'});
    await mobile.route('**/*', route => route.request().url().startsWith(origin) ? route.continue() : route.abort());
    mobile.on('pageerror', error => errors.push(error.message));
    await mobile.goto(origin);
    await mobile.locator('.document-graph').scrollIntoViewIfNeeded();
    await assertTopicLabels(mobile.locator('.document-graph'));
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
    await mobile.locator('.document-graph__reset').tap();
    assert.equal(await mobile.locator('.document-graph').getAttribute('data-center'), null);
    assert.equal(await mobile.locator('.document-graph .muted').count(), 0);
    const mobileArticle = mobile.locator(`.document-graph [data-id="${articleId}"]`);
    await mobileArticle.focus(); await mobile.keyboard.press('Space'); await mobile.waitForTimeout(100);
    const touch = await mobile.context().newCDPSession(mobile);
    const mb = await mobileArticle.locator('.main-circle').boundingBox();
    const mx = mb.x + mb.width / 2, my = mb.y + mb.height / 2;
    const beforeTouch = await mobileArticle.getAttribute('transform');
    await touch.send('Input.dispatchTouchEvent', {type: 'touchStart', touchPoints: [{x: mx, y: my}]});
    await mobile.waitForTimeout(400);
    await touch.send('Input.dispatchTouchEvent', {type: 'touchMove', touchPoints: [{x: mx + 3, y: my + 2}]});
    assert.equal(await mobileArticle.getAttribute('transform'), beforeTouch, 'touch jitter does not drag the node');
    await touch.send('Input.dispatchTouchEvent', {type: 'touchEnd', touchPoints: []});
    await mobile.waitForTimeout(450);
    assert.equal(new URL(mobile.url()).pathname, '/', 'single tap on the selected article does not navigate');
    await touch.send('Input.dispatchTouchEvent', {type: 'touchStart', touchPoints: [{x: mx, y: my}]});
    await touch.send('Input.dispatchTouchEvent', {type: 'touchMove', touchPoints: [{x: mx + 65, y: my + 35}]});
    await mobile.waitForTimeout(100);
    assert.notEqual(await mobileArticle.getAttribute('transform'), beforeTouch, 'touch dragging still moves nodes');
    await touch.send('Input.dispatchTouchEvent', {type: 'touchEnd', touchPoints: []});
    assert.equal(new URL(mobile.url()).pathname, '/', 'touch drag does not open a document');
    await mobileArticle.focus(); await mobile.keyboard.press('Space'); await mobile.waitForTimeout(100);
    await mobileArticle.locator('.main-circle').tap();
    await mobileArticle.locator('.main-circle').tap();
    await mobile.waitForURL(url => url.pathname !== '/');
    assert.deepEqual(errors, []);
    console.log('PASS: clusters, ancestors, animated focus, zoom/pan, mouse/touch drag, hold/jitter, double-click/double-tap navigation, keyboard, mobile resize; no browser errors.');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
