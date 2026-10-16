/*
MIT License

Copyright (c) 2025 develmusa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
/* Adapted from develmusa/mkdocs-network-graph-plugin, static/graph.js
 * commit 79bcdf5db686086e316ffab77c73030f75565426, Copyright (c) 2025 develmusa.
 * MIT license: vendor/mkdocs-network-graph-plugin.LICENSE (also embedded below).
 * Retains the D3 force/link/node/tick/drag renderer; replaces modal/sidebar UI
 * with an inline graph and animated focus. See README.md for modifications.
 */
(() => {
  const root = document.currentScript.previousElementSibling.previousElementSibling.previousElementSibling;
  if (!root || root.dataset.ready) return;
  root.dataset.ready = 'true';
  const graph = JSON.parse(root.querySelector('.document-graph__data').textContent);
  const d3 = window.d3;
  const svg = d3.select(root.querySelector('svg'));
  const g = svg.append('g');
  const width = () => root.clientWidth;
  const height = () => svg.node().clientHeight;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const nodesData = graph.nodes.map(n => ({...n}));
  const branchColor = d3.scaleOrdinal()
    .domain([...new Set(nodesData.map(n => n.branch))])
    .range(['#478dcc', '#d28b36', '#9b7ad4', '#42a58f', '#cb7394']);
  const processedLinksMap = new Map();
  for (const link of graph.edges) {
    const key = JSON.stringify([link.source, link.target].sort());
    if (!processedLinksMap.has(key)) processedLinksMap.set(key, {...link});
  }
  const processedLinks = Array.from(processedLinksMap.values());
  let currentNode = null;
  let hoveredNode = null;
  let scale = 1;
  const radius = d => (d.depth === 0 ? 8 : d.depth === 1 ? 6 : 5) * (d === currentNode ? 1.5 : 1);
  const zoom = d3.zoom().scaleExtent([.35, 4]).clickDistance(5)
    .on('start', event => { if (event.sourceEvent) svg.interrupt(); })
    .on('zoom', event => {
      scale = event.transform.k;
      g.attr('transform', event.transform);
      // Labels and hit targets retain their screen size even when zoomed out.
      node.select('.glyph').attr('transform', `scale(${1 / scale})`);
      placeLabels();
    });
  svg.call(zoom).on('dblclick.zoom', null);
  const link = g.append('g').attr('class', 'links').selectAll('line')
    .data(processedLinks).enter().append('line').attr('class', 'link');
  const node = g.append('g').attr('class', 'nodes').selectAll('g')
    .data(nodesData).enter().append('g')
    .attr('class', 'node').attr('data-id', d => d.id).attr('data-depth', d => d.depth)
    .attr('data-branch', d => d.branch)
    .style('--graph-branch-color', d => branchColor(d.branch))
    .attr('tabindex', 0).attr('role', 'button').attr('aria-label', d => d.label)
    .attr('aria-pressed', 'false')
    .on('mouseenter', function(event, d) { hoveredNode = d; d3.select(this).raise(); placeLabels(); })
    .on('mouseleave', () => { hoveredNode = null; placeLabels(); })
    .on('focus', function(event, d) { hoveredNode = d; d3.select(this).raise(); placeLabels(); })
    .on('blur', () => { hoveredNode = null; placeLabels(); })
    .on('click', (event, d) => {
      if (event.defaultPrevented) return;
      if ((event.ctrlKey || event.metaKey) && d.url) window.open(d.url, '_blank', 'noopener');
      else if (currentNode === d && d.url) window.location.assign(d.url);
      else focusNode(d);
    })
    .on('keydown', (event, d) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        if (event.key === 'Enter' && currentNode === d && d.url) window.location.assign(d.url);
        else focusNode(d);
      }
    })
    .call(d3.drag().clickDistance(5)
      .on('start', dragstarted).on('drag', dragged).on('end', dragended));
  const glyph = node.append('g').attr('class', 'glyph');
  glyph.append('circle').attr('class', 'hit-area').attr('r', 22);
  glyph.append('circle').attr('class', 'main-circle').attr('r', radius);
  glyph.append('title').text(d => d.url ? `${d.label} — 선택 후 다시 클릭하여 문서 열기` : d.label);
  const label = glyph.append('text').attr('x', 0);
  label.each(function(d) {
    const words = d.label.split(/\s+/);
    const lines = [''];
    for (const word of words) {
      const last = lines.length - 1;
      if (lines[last] && (lines[last] + ' ' + word).length > 23) lines.push(word);
      else lines[last] += (lines[last] ? ' ' : '') + word;
    }
    d.labelLines = lines.length;
    const text = d3.select(this);
    lines.forEach((line, i) => text.append('tspan').attr('x', 0).attr('dy', i ? '1.15em' : 0).text(line));
    d.labelBox = this.getBBox();
  });
  function placeLabels() {
    // At overview scale not every title can fit. Keep every node visible and
    // choose non-overlapping labels, revealing more as the user zooms/pans.
    // The centered node and its neighbors get first choice of label space.
    const transform = d3.zoomTransform(svg.node());
    const connected = new Set();
    if (currentNode) processedLinks.forEach(e => {
      const source = e.source.id || e.source, target = e.target.id || e.target;
      if (source === currentNode.id) connected.add(target);
      if (target === currentNode.id) connected.add(source);
    });
    const priority = d => d === currentNode ? -3 : d === hoveredNode ? -2 : connected.has(d.id) ? -1 : d.depth;
    const ordered = [...nodesData].sort((a, b) => priority(a) - priority(b));
    const occupied = nodesData.map(d => {
      const [x, y] = transform.apply([d.x, d.y]);
      return {x: x - radius(d) - 3, y: y - radius(d) - 3, w: 2 * radius(d) + 6, h: 2 * radius(d) + 6};
    });
    const intersects = (a, b) => a.x < b.x + b.w + 3 && a.x + a.w + 3 > b.x && a.y < b.y + b.h + 3 && a.y + a.h + 3 > b.y;
    const elements = new Map();
    label.each(function(d) { elements.set(d.id, this); });
    for (const d of ordered) {
      const el = elements.get(d.id), box = d.labelBox;
      const [x, y] = transform.apply([d.x, d.y]);
      const gap = radius(d) + 9;
      const candidates = [[gap, -box.height / 2], [-gap - box.width, -box.height / 2],
        [-box.width / 2, gap], [-box.width / 2, -gap - box.height]];
      let placement = null;
      for (const [dx, dy] of candidates) {
        const rect = {x: x + dx, y: y + dy, w: box.width, h: box.height};
        if (rect.x < 4 || rect.y < 4 || rect.x + rect.w > width() - 4 || rect.y + rect.h > height() - 4) continue;
        if (!occupied.some(other => intersects(rect, other))) { placement = {dx, dy, rect}; break; }
      }
      if (!placement && (d === currentNode || d === hoveredNode || d.depth === 0)) {
        placement = {dx: gap, dy: -box.height / 2, rect: {x: x + gap, y: y - box.height / 2, w: box.width, h: box.height}};
      }
      el.style.visibility = placement ? 'visible' : 'hidden';
      if (placement) {
        el.setAttribute('transform', `translate(${placement.dx - box.x},${placement.dy - box.y})`);
        occupied.push(placement.rect);
      }
    }
  }
  // Upstream's force simulation, with more space for readable labels.
  const simulation = d3.forceSimulation(nodesData)
    .force('link', d3.forceLink(processedLinks).id(d => d.id).distance(110))
    .force('charge', d3.forceManyBody().strength(-380))
    .force('center', d3.forceCenter(0, 0))
    .force('x', d3.forceX(0).strength(.035))
    .force('y', d3.forceY(0).strength(.06))
    .force('collide', d3.forceCollide(45))
    .stop();
  for (let i = 0; i < 240; i++) simulation.tick();
  function tick() {
    link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
    node.attr('transform', d => `translate(${d.x},${d.y})`);
    placeLabels();
  }
  simulation.on('tick', tick);
  tick();
  function focusNode(d) {
    currentNode = d;
    node.filter(n => n === d).raise();
    root.dataset.center = d.id;
    node.classed('current', n => n === d).attr('aria-pressed', n => String(n === d));
    node.select('.main-circle').interrupt().transition().duration(reducedMotion ? 0 : 300).attr('r', radius);
    link.classed('connected', e => e.source === d || e.target === d);
    const neighbors = new Set([d]);
    processedLinks.forEach(e => {
      if (e.source === d) neighbors.add(e.target);
      if (e.target === d) neighbors.add(e.source);
    });
    node.classed('muted', n => !neighbors.has(n));
    link.classed('muted', e => e.source !== d && e.target !== d);
    placeLabels();
    // Move the camera through the existing graph: no redraw, random layout or
    // disappearing neighbors. Interrupting a flight starts at its current frame.
    simulation.stop();
    const target = d3.zoomIdentity.translate(width() / 2, height() / 2).scale(1)
      .translate(-d.x, -d.y);
    svg.interrupt().transition().duration(reducedMotion ? 0 : 750)
      .ease(d3.easeCubicInOut).call(zoom.transform, target);
  }
  root.querySelector('.document-graph__reset').addEventListener('click', () => {
    svg.interrupt();
    simulation.stop();
    currentNode = null;
    hoveredNode = null;
    delete root.dataset.center;
    node.classed('current', false).classed('muted', false).attr('aria-pressed', 'false');
    node.select('.main-circle').interrupt().attr('r', radius);
    link.classed('connected', false).classed('muted', false);
    fit();
  });
  function dragstarted(event, d) {
    svg.interrupt();
    if (!event.active) simulation.alphaTarget(.2).restart();
    d.fx = d.x; d.fy = d.y;
  }
  function dragged(event, d) { d.fx = event.x; d.fy = event.y; }
  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null; d.fy = null;
  }
  function fit() {
    if (currentNode) {
      const t = d3.zoomTransform(svg.node());
      svg.interrupt().call(zoom.transform, d3.zoomIdentity.translate(width() / 2, height() / 2)
        .scale(t.k).translate(-currentNode.x, -currentNode.y));
      return;
    }
    const bounds = g.node().getBBox();
    const k = Math.max(.35, Math.min(1, (width() - 80) / bounds.width, (height() - 80) / bounds.height));
    svg.call(zoom.transform, d3.zoomIdentity.translate(width() / 2, height() / 2).scale(k)
      .translate(-(bounds.x + bounds.width / 2), -(bounds.y + bounds.height / 2)));
  }
  fit();
  const observer = new ResizeObserver(fit);
  observer.observe(root);
  // Home uses Material's normal navigation; disconnect if replaced dynamically.
  const removal = new MutationObserver(() => {
    if (!root.isConnected) { simulation.stop(); observer.disconnect(); removal.disconnect(); }
  });
  removal.observe(document.body, {childList: true, subtree: true});
})();
