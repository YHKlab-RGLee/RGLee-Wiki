import unittest
from types import SimpleNamespace as Obj
from hooks.document_graph import build_graph


def page(path, content='', url=None):
    return Obj(is_section=False, is_page=True, title=path,
               file=Obj(name=path.rsplit('/', 1)[-1].split('.')[0], src_uri=path),
               url=url or path[:-3] + '/', content=content)


def section(title, children):
    return Obj(is_section=True, is_page=False, title=title, children=children)


class GraphTests(unittest.TestCase):
    def test_hierarchy_links_and_exclusions(self):
        a = page('topic/a.md', '<a href="../b/#one">B</a><a href="../b/?q=2">B</a>'
                 '<a href="../">index</a><a href="#self">self</a>'
                 '<a href="https://other.test/topic/b/">external</a>'
                 '<code>&lt;a href="../c/"&gt;</code>')
        b = page('topic/b.md', '<a href="/wiki/topic/a/">A</a>')
        nav = Obj(items=[page('index.md'), section('Domain', [page('domain/index.md'),
                  section('Topic', [page('topic/index.md'), a, b])])])
        graph = build_graph(nav, 'https://example.test/wiki/')
        self.assertEqual([n['label'] for n in graph['nodes']], ['Domain', 'Topic', 'topic/a.md', 'topic/b.md'])
        self.assertEqual(graph['nodes'][0]['url'], 'domain/index/')
        self.assertEqual(graph['nodes'][1]['url'], 'topic/index/')
        self.assertEqual([n['depth'] for n in graph['nodes']], [0, 1, 2, 2])
        self.assertEqual(len([e for e in graph['edges'] if e['kind'] == 'tree']), 3)
        self.assertEqual([(e['source'], e['target']) for e in graph['edges'] if e['kind'] == 'link'],
                         [('topic/a.md', 'topic/b.md'), ('topic/b.md', 'topic/a.md')])
        b.content = ''
        self.assertEqual(len([e for e in build_graph(nav, 'https://example.test/wiki/')['edges'] if e['kind'] == 'link']), 1)

    def test_sections_only_use_their_own_index(self):
        nav = Obj(items=[section('Domain', [section('Topic', [
            page('topic/index.md', url='topic/'), page('topic/a.md')])])])
        nodes = build_graph(nav, '')['nodes']
        self.assertNotIn('url', nodes[0])
        self.assertEqual(nodes[1]['url'], 'topic/')

    def test_file_urls_and_encoded_paths(self):
        a = page('a.md', '<a href="b%20name.html#section">B</a>', 'a.html')
        b = page('b name.md', url='b%20name.html')
        graph = build_graph(Obj(items=[a, b]), '')
        self.assertEqual(graph['edges'], [dict(source='a.md', target='b name.md', kind='link')])


if __name__ == '__main__':
    unittest.main()
