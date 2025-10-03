import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_create(self):
        node = ParentNode("a",[LeafNode("span","Click me!",{"class":"button"})])
        self.assertEqual(node.tag,"a")
        self.assertIsNone(node.value)
        self.assertIsNone(node.props)
        self.assertEqual(len(node.children),1)
    
    def test_to_html(self):
        node = ParentNode("p", children=
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_without_tag(self):
        node = ParentNode(None,[])
        self.assertRaises(ValueError,node.to_html)
           
    def test_to_html_without_children(self):
        node = ParentNode("div",None)
        node = ParentNode(None,[])
        self.assertRaises(ValueError,node.to_html)