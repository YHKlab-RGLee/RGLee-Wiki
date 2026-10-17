"""Build the home navigation graph from MkDocs' resolved navigation and HTML."""
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlsplit


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.hrefs.extend(value for key, value in attrs if key == 'href' and value)


def build_graph(nav, site_url):
    nodes, edges, pages = [], [], {}

    def walk(items, parent=None, depth=0, branch=0):
        for position, item in enumerate(items):
            color = position if parent is None else branch
            if item.is_section:
                key = f'section:{len(nodes)}'
                node = dict(id=key, label=item.title, depth=depth, branch=color)
                index = next((child for child in item.children
                              if child.is_page and child.file.name == 'index'), None)
                if index is not None:
                    node['url'] = index.url
                nodes.append(node)
                if parent is not None:
                    edges.append(dict(source=parent, target=key, kind='tree'))
                walk(item.children, key, depth + 1, color)
            elif item.is_page and item.file.name != 'index':
                key = item.file.src_uri
                nodes.append(dict(id=key, label=item.title, depth=depth,
                                  branch=color, url=item.url))
                pages[key] = item
                if parent is not None:
                    edges.append(dict(source=parent, target=key, kind='tree'))

    walk(nav.items)
    base = (site_url or 'https://wiki.invalid/').rstrip('/') + '/'
    # Use resolved output URLs: Markdown, reference-style and HTML anchors all
    # arrive here after MkDocs' link processing. Anchors/query strings collapse.
    def canonical(url):
        parts = urlsplit(url)
        return parts.netloc, unquote(parts.path)

    urls = {canonical(urljoin(base, page.url)): key for key, page in pages.items()}
    seen = set()
    for source, page in pages.items():
        parser = Links()
        parser.feed(page.content or '')
        for href in parser.hrefs:
            target = urls.get(canonical(urljoin(urljoin(base, page.url), href)))
            if target and source != target and (source, target) not in seen:
                seen.add((source, target))
                edges.append(dict(source=source, target=target, kind='link'))
    return dict(nodes=nodes, edges=edges)


def on_env(env, *, config, files, **kwargs):
    # on_env runs after every page has been rendered, including on serve rebuilds.
    home = next((file.page for file in files if file.src_uri == 'index.md'), None)
    if home:
        config.extra['document_graph'] = build_graph(home.navigation, config.site_url)
    return env


def on_nav(nav, *, config, files, **kwargs):
    # Navigation is build-local; attach it to Home rather than retaining globals.
    for page in nav.pages:
        if page.file.src_uri == 'index.md':
            page.navigation = nav
    return nav
