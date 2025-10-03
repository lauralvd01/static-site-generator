import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_create(self) :
        node = LeafNode(tag="p", value="This is a paragraph of text.")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph of text.")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        
        node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me!")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"href": "https://www.google.com"})
        
        node = LeafNode(tag=None, value="Hello, World!")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Hello, World!")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_leaf_to_html(self) :
        node = LeafNode(tag="p", value="This is a paragraph of text.")
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')
        
        node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
        node = LeafNode(tag=None, value="Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")
        
    def test_leaf_to_html_without_value(self):
        node = LeafNode(None,None)
        self.assertRaises(ValueError,node.to_html)
        
if __name__ == "__main__":
    unittest.main()