import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_create(self) :
        node = HTMLNode(tag='p', value='Hello, World!', children=None, props={'class': 'text'})
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'Hello, World!')
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {'class': 'text'})
        
        node = HTMLNode(tag='a', value=None, children=[HTMLNode(tag='span', value='Click here')], props={'href': 'https://example.com'})
        self.assertEqual(node.tag, 'a')
        self.assertIsNone(node.value)
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, 'span')
        self.assertEqual(node.props, {'href': 'https://example.com'})
        
    def test_to_html_without_tag(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError,node.to_html)    
    
    def test_props_to_html(self):
        node = HTMLNode(tag='div')
        self.assertEqual(node.props_to_html(), '')
        
        node = HTMLNode(tag='img', value=None, children=None, props={'src': 'image.png', 'alt': 'An image'})
        self.assertEqual(node.props_to_html(), ' src="image.png" alt="An image"')
        
        node = HTMLNode(tag='input', value=None, children=None, props={'type': 'text', 'placeholder': 'Enter text'})
        self.assertEqual(node.props_to_html(), ' type="text" placeholder="Enter text"')
    
    def test_repr(self):
        node = HTMLNode(tag='div', value='Content', children=None, props={'class': 'container'})
        self.assertEqual(repr(node), 'HTMLNode(tag=div, value=Content, children=None, props= class="container")')
        
        node = HTMLNode(tag='span', value=None, children=[HTMLNode(tag='strong', value='Bold Text')], props={'style': 'color: red;'})
        self.assertEqual(repr(node), 'HTMLNode(tag=span, value=None, children=[HTMLNode(tag=strong, value=Bold Text, children=None, props=)], props= style="color: red;")')
    
if __name__ == "__main__":
    unittest.main()