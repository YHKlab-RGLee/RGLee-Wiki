(() => {
  const root = document.currentScript.previousElementSibling.previousElementSibling;
  const data = JSON.parse(root.querySelector('.document-graph__data').textContent);
  const svg = root.querySelector('svg'), ns = 'http://www.w3.org/2000/svg';
  const create = (tag, attrs, parent) => {
    const el = document.createElementNS(ns, tag);
    Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value));
    parent.appendChild(el); return el;
  };
  const nodes = new Map(data.nodes.map(n => [n.id, {...n, children: []}]));
  data.edges.filter(e => e.kind === 'tree').forEach(e => nodes.get(e.source).children.push(nodes.get(e.target)));
  const children = new Set(data.edges.filter(e => e.kind === 'tree').map(e => e.target));
  const roots = [...nodes.values()].filter(n => !children.has(n.id));
  const weight = n => n.weight = n.children.length ? n.children.reduce((sum, c) => sum + weight(c), 0) : 1;
  const total = roots.reduce((sum, n) => sum + weight(n), 0);
  const place = (n, start, span) => {
    const angle = start + span / 2, radius = [110, 275, 450][Math.min(n.depth, 2)];
    n.x = Math.cos(angle) * radius; n.y = Math.sin(angle) * radius;
    let cursor = start;
    n.children.forEach(c => {const arc = span * c.weight / n.weight; place(c, cursor, arc); cursor += arc;});
  };
  let angle = -Math.PI / 2;
  roots.forEach(n => {const span = 2 * Math.PI * n.weight / total; place(n, angle + .035, span - .07); angle += span;});
  const layer = create('g', {}, svg), edgeLayer = create('g', {}, layer), nodeLayer = create('g', {}, layer);
  data.edges.forEach(e => {
    const a = nodes.get(e.source), b = nodes.get(e.target);
    e.el = create('path', {d:`M${a.x},${a.y} Q0,0 ${b.x},${b.y}`, class:`edge ${e.kind}`}, edgeLayer);
    if (e.kind === 'tree') e.el.setAttribute('d', `M${a.x},${a.y} L${b.x},${b.y}`);
  });
  const palette = ['#8971d0', '#399fbd', '#42a58b'];
  const search = root.querySelector('input[type=search]'), toggle = root.querySelector('input[type=checkbox]');
  const status = root.querySelector('.document-graph__status');
  function highlight(id = null) {
    const query = search.value.trim().toLocaleLowerCase();
    const selected = new Set([...nodes.values()].filter(n => id ? n.id === id : query && n.label.toLocaleLowerCase().includes(query)).map(n => n.id));
    const nearby = new Set(selected);
    data.edges.forEach(e => {
      const active = (e.kind === 'tree' || toggle.checked) && (selected.has(e.source) || selected.has(e.target));
      if (active) {nearby.add(e.source); nearby.add(e.target);}
      e.el.classList.toggle('active', active);
      e.el.classList.toggle('dim', Boolean(id || query) && !active);
      e.el.style.display = e.kind === 'link' && !toggle.checked ? 'none' : '';
    });
    nodes.forEach(n => {n.el.classList.toggle('dim', Boolean(id || query) && !nearby.has(n.id)); n.el.classList.toggle('active', selected.has(n.id));});
    status.textContent = id ? nodes.get(id).label : query ? `${selected.size}개 항목 일치 · 강조된 문서를 선택하세요.` : '노드에 마우스를 올리거나 키보드로 선택하면 연결을 강조합니다. 확대 후 드래그로 이동할 수 있습니다.';
  }
  nodes.forEach(n => {
    const el = create(n.url ? 'a' : 'g', {class:'node', 'data-depth':n.depth, tabindex:0, 'aria-label':n.label}, nodeLayer);
    if (n.url) el.setAttribute('href', n.url);
    n.el = el;
    create('circle', {cx:n.x, cy:n.y, r:[15, 10, 6][Math.min(n.depth, 2)], fill:palette[Math.min(n.depth, 2)]}, el);
    const title = create('title', {}, el); title.textContent = n.label;
    const text = create('text', {x:n.x + (n.x >= 0 ? 13 : -13), y:n.y + 4, 'text-anchor':n.x >= 0 ? 'start' : 'end'}, el);
    text.textContent = n.label;
    el.addEventListener('mouseenter', () => highlight(n.id));
    el.addEventListener('mouseleave', () => highlight());
    el.addEventListener('focus', () => highlight(n.id));
    el.addEventListener('blur', () => highlight());
  });
  search.addEventListener('input', () => highlight()); toggle.addEventListener('change', () => highlight());
  root.querySelector('[data-count]').textContent = `${data.nodes.filter(n => n.url).length}개 문서 · ${data.edges.filter(e => e.kind === 'link').length}개 문서 연결`;
  let scale = 1, x = 0, y = 0, drag = null;
  const transform = () => layer.setAttribute('transform', `translate(${x} ${y}) scale(${scale})`);
  root.querySelectorAll('[data-zoom]').forEach(button => button.addEventListener('click', () => {
    if (button.dataset.zoom === 'reset') {scale = 1; x = y = 0;} else scale = Math.max(.7, Math.min(5, scale * (button.dataset.zoom === 'in' ? 1.3 : 1 / 1.3)));
    transform();
  }));
  const point = event => {const p = svg.createSVGPoint(); p.x = event.clientX; p.y = event.clientY; return p.matrixTransform(svg.getScreenCTM().inverse());};
  svg.addEventListener('pointerdown', event => {if (event.target.closest('.node')) return; const p = point(event); drag = {x:p.x - x, y:p.y - y}; svg.setPointerCapture(event.pointerId);});
  svg.addEventListener('pointermove', event => {if (!drag) return; const p = point(event); x = p.x - drag.x; y = p.y - drag.y; transform();});
  ['pointerup', 'pointercancel'].forEach(type => svg.addEventListener(type, () => {drag = null;}));
})();
