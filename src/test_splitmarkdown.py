import unittest

from textnode import TextNode, TextType

from splitmarkdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestSplitMarkdown(unittest.TestCase):
    def test_split_raw_text(self):
        node = TextNode("This is raw text",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(new_nodes,[node])
        new_nodes = split_nodes_delimiter([node],'_',TextType.ITALIC)
        self.assertEqual(new_nodes,[node])
        new_nodes = split_nodes_delimiter([node],'`',TextType.CODE)
        self.assertEqual(new_nodes,[node])
        
        nodes = [node, TextNode("This is a second raw text",TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes,'**',TextType.BOLD)
        self.assertEqual(new_nodes,nodes)
        new_nodes = split_nodes_delimiter(nodes,'_',TextType.ITALIC)
        self.assertEqual(new_nodes,nodes)
        new_nodes = split_nodes_delimiter(nodes,'`',TextType.CODE)
        self.assertEqual(new_nodes,nodes)
    
    def test_split_bold_within_raw_text(self):
        node = TextNode("This is a text with a **bold word** in the middle.",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("bold word",TextType.BOLD),TextNode(" in the middle.",TextType.TEXT)])
        
        node = TextNode("This is a text with a **bold word** in the middle, and a **second bold part.**",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("bold word",TextType.BOLD),TextNode(" in the middle, and a ",TextType.TEXT),TextNode("second bold part.",TextType.BOLD)])
        
        node = TextNode("This is a text with a **first bold part ****and a second bold part** that follow.",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("first bold part ",TextType.BOLD),TextNode("and a second bold part",TextType.BOLD),TextNode(" that follow.",TextType.TEXT)])
        
    def test_split_italic_within_raw_text(self):
        node = TextNode("This is a text with an **italic word** in the middle.",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],'**',TextType.ITALIC)
        self.assertEqual(new_nodes,[TextNode("This is a text with an ",TextType.TEXT),TextNode("italic word",TextType.ITALIC),TextNode(" in the middle.",TextType.TEXT)])
        
        node = TextNode("This is a text with an **italic word** in the middle, and a **second italic part.**",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],'**',TextType.ITALIC)
        self.assertEqual(new_nodes,[TextNode("This is a text with an ",TextType.TEXT),TextNode("italic word",TextType.ITALIC),TextNode(" in the middle, and a ",TextType.TEXT),TextNode("second italic part.",TextType.ITALIC)])
        
        node = TextNode("This is a text with a **first italic part ****and a second italic part** that follow.",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],'**',TextType.ITALIC)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("first italic part ",TextType.ITALIC),TextNode("and a second italic part",TextType.ITALIC),TextNode(" that follow.",TextType.TEXT)])
    
    def test_split_code_within_raw_text(self):
        node = TextNode("This is a text with a **code word** in the middle.",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],'**',TextType.CODE)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("code word",TextType.CODE),TextNode(" in the middle.",TextType.TEXT)])
        
        node = TextNode("This is a text with a **code word** in the middle, and a **second code part.**",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],'**',TextType.CODE)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("code word",TextType.CODE),TextNode(" in the middle, and a ",TextType.TEXT),TextNode("second code part.",TextType.CODE)])
        
        node = TextNode("This is a text with a **first code part ****and a second code part** that follow.",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],'**',TextType.CODE)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("first code part ",TextType.CODE),TextNode("and a second code part",TextType.CODE),TextNode(" that follow.",TextType.TEXT)])
        
    def test_split_texts_with_several_text_types(self):
        node_with_bold_italic_code = TextNode("This is a text with **bold**, _italic_ and `code` words.",TextType.TEXT)
        node_with_italic_bold_code = TextNode("This is a text with _italic_, **bold** and `code` words.",TextType.TEXT)
        node_with_code_bold_italic = TextNode("This is a text with `code`, **bold** and _italic_ words.",TextType.TEXT)
        node_with_italic_code_bold = TextNode("This is a text with _italic_, `code` and **bold** words.",TextType.TEXT)
        
        first_result = [TextNode("This is a text with ",TextType.TEXT),TextNode("bold",TextType.BOLD),TextNode(', ',TextType.TEXT),TextNode("italic",TextType.ITALIC),TextNode(' and ',TextType.TEXT),TextNode("code",TextType.CODE),TextNode(' words.',TextType.TEXT)]
        result1 = split_nodes_delimiter([node_with_bold_italic_code],'**',TextType.BOLD)
        result2 = split_nodes_delimiter(result1,'_',TextType.ITALIC)
        result3 = split_nodes_delimiter(result2,'`',TextType.CODE)
        self.assertEqual(result3,first_result)
        
        second_result = [TextNode("This is a text with ",TextType.TEXT),TextNode("italic",TextType.ITALIC),TextNode(', ',TextType.TEXT),TextNode("bold",TextType.BOLD),TextNode(' and ',TextType.TEXT),TextNode("code",TextType.CODE),TextNode(' words.',TextType.TEXT)]
        result1 = split_nodes_delimiter([node_with_italic_bold_code],'**',TextType.BOLD)
        result2 = split_nodes_delimiter(result1,'_',TextType.ITALIC)
        result3 = split_nodes_delimiter(result2,'`',TextType.CODE)
        self.assertEqual(result3,second_result)
        
        third_result = [TextNode("This is a text with ",TextType.TEXT),TextNode("code",TextType.CODE),TextNode(', ',TextType.TEXT),TextNode("bold",TextType.BOLD),TextNode(' and ',TextType.TEXT),TextNode("italic",TextType.ITALIC),TextNode(' words.',TextType.TEXT)]
        result1 = split_nodes_delimiter([node_with_code_bold_italic],'**',TextType.BOLD)
        result2 = split_nodes_delimiter(result1,'_',TextType.ITALIC)
        result3 = split_nodes_delimiter(result2,'`',TextType.CODE)
        self.assertEqual(result3,third_result)
        
        fourth_result = [TextNode("This is a text with ",TextType.TEXT),TextNode("italic",TextType.ITALIC),TextNode(', ',TextType.TEXT),TextNode("code",TextType.CODE),TextNode(' and ',TextType.TEXT),TextNode("bold",TextType.BOLD),TextNode(' words.',TextType.TEXT)]
        result1 = split_nodes_delimiter([node_with_italic_code_bold],'**',TextType.BOLD)
        result2 = split_nodes_delimiter(result1,'_',TextType.ITALIC)
        result3 = split_nodes_delimiter(result2,'`',TextType.CODE)
        self.assertEqual(result3,fourth_result)
        
        with_code = split_nodes_delimiter([node_with_bold_italic_code, node_with_italic_bold_code, node_with_code_bold_italic, node_with_italic_code_bold], '`', TextType.CODE)
        with_italic = split_nodes_delimiter(with_code, '_', TextType.ITALIC)
        final = split_nodes_delimiter(with_italic, '**', TextType.BOLD)
        self.assertEqual(final, first_result + second_result + third_result + fourth_result)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), ![another one](https://url.com) and one [link](dumblink.com).")
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png"),("another one","https://url.com")])
        
        matches = extract_markdown_images("This is raw text with a **bold** word")
        self.assertEqual(matches,[])
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), ![another one](https://url.com) and one [link](dumblink.com).")
        self.assertListEqual(matches, [("link","dumblink.com")])