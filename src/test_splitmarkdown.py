import unittest

from textnode import TextNode, TextType

import splitmarkdown as sp

class TestSplitMarkdown(unittest.TestCase):
    def test_split_raw_text(self):
        node = TextNode("This is raw text",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(new_nodes,[node])
        new_nodes = sp.split_nodes_delimiter([node],'_',TextType.ITALIC)
        self.assertEqual(new_nodes,[node])
        new_nodes = sp.split_nodes_delimiter([node],'`',TextType.CODE)
        self.assertEqual(new_nodes,[node])
        
        nodes = [node, TextNode("This is a second raw text",TextType.TEXT)]
        new_nodes = sp.split_nodes_delimiter(nodes,'**',TextType.BOLD)
        self.assertEqual(new_nodes,nodes)
        new_nodes = sp.split_nodes_delimiter(nodes,'_',TextType.ITALIC)
        self.assertEqual(new_nodes,nodes)
        new_nodes = sp.split_nodes_delimiter(nodes,'`',TextType.CODE)
        self.assertEqual(new_nodes,nodes)
    
    def test_split_bold_within_raw_text(self):
        node = TextNode("This is a text with a **bold word** in the middle.",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("bold word",TextType.BOLD),TextNode(" in the middle.",TextType.TEXT)])
        
        node = TextNode("This is a text with a **bold word** in the middle, and a **second bold part.**",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("bold word",TextType.BOLD),TextNode(" in the middle, and a ",TextType.TEXT),TextNode("second bold part.",TextType.BOLD)])
        
        node = TextNode("This is a text with a **first bold part ****and a second bold part** that follow.",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("first bold part ",TextType.BOLD),TextNode("and a second bold part",TextType.BOLD),TextNode(" that follow.",TextType.TEXT)])
        
        node = TextNode("**Beginning with a bold text** then normal text.",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(new_nodes,[TextNode("Beginning with a bold text",TextType.BOLD),TextNode(" then normal text.",TextType.TEXT)])
        
        node = TextNode("**Entire bold text**",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'**',TextType.BOLD)
        self.assertEqual(new_nodes,[TextNode("Entire bold text",TextType.BOLD)])
        
    def test_split_italic_within_raw_text(self):
        node = TextNode("This is a text with an _italic word_ in the middle.",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'_',TextType.ITALIC)
        self.assertEqual(new_nodes,[TextNode("This is a text with an ",TextType.TEXT),TextNode("italic word",TextType.ITALIC),TextNode(" in the middle.",TextType.TEXT)])
        
        node = TextNode("This is a text with an _italic word_ in the middle, and a _second italic part._",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'_',TextType.ITALIC)
        self.assertEqual(new_nodes,[TextNode("This is a text with an ",TextType.TEXT),TextNode("italic word",TextType.ITALIC),TextNode(" in the middle, and a ",TextType.TEXT),TextNode("second italic part.",TextType.ITALIC)])
        
        node = TextNode("This is a text with a _first italic part __and a second italic part_ that follow.",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'_',TextType.ITALIC)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("first italic part ",TextType.ITALIC),TextNode("and a second italic part",TextType.ITALIC),TextNode(" that follow.",TextType.TEXT)])
        
        node = TextNode("_Beginning with an italic text_ then normal text.",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'_',TextType.ITALIC)
        self.assertEqual(new_nodes,[TextNode("Beginning with an italic text",TextType.ITALIC),TextNode(" then normal text.",TextType.TEXT)])
        
        node = TextNode("_Entire italic text_",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'_',TextType.ITALIC)
        self.assertEqual(new_nodes,[TextNode("Entire italic text",TextType.ITALIC)])
    
    def test_split_code_within_raw_text(self):
        node = TextNode("This is a text with a `code word` in the middle.",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'`',TextType.CODE)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("code word",TextType.CODE),TextNode(" in the middle.",TextType.TEXT)])
        
        node = TextNode("This is a text with a `code word` in the middle, and a `second code part.`",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'`',TextType.CODE)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("code word",TextType.CODE),TextNode(" in the middle, and a ",TextType.TEXT),TextNode("second code part.",TextType.CODE)])
        
        node = TextNode("This is a text with a `first code part ``and a second code part` that follow.",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'`',TextType.CODE)
        self.assertEqual(new_nodes,[TextNode("This is a text with a ",TextType.TEXT),TextNode("first code part ",TextType.CODE),TextNode("and a second code part",TextType.CODE),TextNode(" that follow.",TextType.TEXT)])
        
        node = TextNode("`Beginning with code` then normal text.",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'`',TextType.CODE)
        self.assertEqual(new_nodes,[TextNode("Beginning with code",TextType.CODE),TextNode(" then normal text.",TextType.TEXT)])
        
        node = TextNode("`Entire code`",TextType.TEXT)
        new_nodes = sp.split_nodes_delimiter([node],'`',TextType.CODE)
        self.assertEqual(new_nodes,[TextNode("Entire code",TextType.CODE)])
        
    def test_split_texts_with_several_text_types(self):
        node_with_bold_italic_code = TextNode("This is a text with **bold**, _italic_ and `code` words.",TextType.TEXT)
        node_with_italic_bold_code = TextNode("This is a text with _italic_, **bold** and `code` words.",TextType.TEXT)
        node_with_code_bold_italic = TextNode("This is a text with `code`, **bold** and _italic_ words.",TextType.TEXT)
        node_with_italic_code_bold = TextNode("This is a text with _italic_, `code` and **bold** words.",TextType.TEXT)
        
        first_result = [TextNode("This is a text with ",TextType.TEXT),TextNode("bold",TextType.BOLD),TextNode(', ',TextType.TEXT),TextNode("italic",TextType.ITALIC),TextNode(' and ',TextType.TEXT),TextNode("code",TextType.CODE),TextNode(' words.',TextType.TEXT)]
        result1 = sp.split_nodes_delimiter([node_with_bold_italic_code],'**',TextType.BOLD)
        result2 = sp.split_nodes_delimiter(result1,'_',TextType.ITALIC)
        result3 = sp.split_nodes_delimiter(result2,'`',TextType.CODE)
        self.assertEqual(result3,first_result)
        
        second_result = [TextNode("This is a text with ",TextType.TEXT),TextNode("italic",TextType.ITALIC),TextNode(', ',TextType.TEXT),TextNode("bold",TextType.BOLD),TextNode(' and ',TextType.TEXT),TextNode("code",TextType.CODE),TextNode(' words.',TextType.TEXT)]
        result1 = sp.split_nodes_delimiter([node_with_italic_bold_code],'**',TextType.BOLD)
        result2 = sp.split_nodes_delimiter(result1,'_',TextType.ITALIC)
        result3 = sp.split_nodes_delimiter(result2,'`',TextType.CODE)
        self.assertEqual(result3,second_result)
        
        third_result = [TextNode("This is a text with ",TextType.TEXT),TextNode("code",TextType.CODE),TextNode(', ',TextType.TEXT),TextNode("bold",TextType.BOLD),TextNode(' and ',TextType.TEXT),TextNode("italic",TextType.ITALIC),TextNode(' words.',TextType.TEXT)]
        result1 = sp.split_nodes_delimiter([node_with_code_bold_italic],'**',TextType.BOLD)
        result2 = sp.split_nodes_delimiter(result1,'_',TextType.ITALIC)
        result3 = sp.split_nodes_delimiter(result2,'`',TextType.CODE)
        self.assertEqual(result3,third_result)
        
        fourth_result = [TextNode("This is a text with ",TextType.TEXT),TextNode("italic",TextType.ITALIC),TextNode(', ',TextType.TEXT),TextNode("code",TextType.CODE),TextNode(' and ',TextType.TEXT),TextNode("bold",TextType.BOLD),TextNode(' words.',TextType.TEXT)]
        result1 = sp.split_nodes_delimiter([node_with_italic_code_bold],'**',TextType.BOLD)
        result2 = sp.split_nodes_delimiter(result1,'_',TextType.ITALIC)
        result3 = sp.split_nodes_delimiter(result2,'`',TextType.CODE)
        self.assertEqual(result3,fourth_result)
        
        with_code = sp.split_nodes_delimiter([node_with_bold_italic_code, node_with_italic_bold_code, node_with_code_bold_italic, node_with_italic_code_bold], '`', TextType.CODE)
        with_italic = sp.split_nodes_delimiter(with_code, '_', TextType.ITALIC)
        final = sp.split_nodes_delimiter(with_italic, '**', TextType.BOLD)
        self.assertEqual(final, first_result + second_result + third_result + fourth_result)
    
    def test_extract_markdown_images(self):
        matches = sp.extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), ![another one](https://url.com) and one [link](dumblink.com).")
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png"),("another one","https://url.com")])
        
        matches = sp.extract_markdown_images("![Begin with an image](url), then raw text and a last ![image](url2)")
        self.assertEqual(matches,[("Begin with an image","url"),("image","url2")])
        
        matches = sp.extract_markdown_images("This is raw text with a **bold** word")
        self.assertEqual(matches,[])
        
    def test_extract_markdown_links(self):
        matches = sp.extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), ![another one](https://url.com) and one [link](dumblink.com).")
        self.assertListEqual(matches, [("link","dumblink.com")])
        
        matches = sp.extract_markdown_links("[Begin with a link](url), then raw text and a last [link](url2)")
        self.assertEqual(matches,[("Begin with a link","url"),("link","url2")])
    
    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev), a [link](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://www.youtube.com/@bootdotdev).",
            TextType.TEXT,
        )
        new_nodes = sp.split_nodes_image([node])
        self.assertEqual(new_nodes,[
            TextNode("This is text with an image ",TextType.TEXT),
            TextNode("to boot dev",TextType.IMAGE,"https://www.boot.dev"),
            TextNode(", a [link](https://i.imgur.com/zjjcJKZ.png) and ",TextType.TEXT),
            TextNode("another image",TextType.IMAGE,"https://www.youtube.com/@bootdotdev"),
            TextNode(".",TextType.TEXT),
            ])
        
        node = TextNode(
            "![Begin with an image](url), then raw text and a last ![image](url2)",
            TextType.TEXT,
        )
        new_nodes = sp.split_nodes_image([node])
        self.assertEqual(new_nodes,[
            TextNode("Begin with an image",TextType.IMAGE,"url"),
            TextNode(", then raw text and a last ",TextType.TEXT),
            TextNode("image",TextType.IMAGE,"url2"),
            ])
        
    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a [link to boot dev](https://www.boot.dev), an ![image](https://i.imgur.com/zjjcJKZ.png) and [another link](https://www.youtube.com/@bootdotdev).",
            TextType.TEXT,
        )
        new_nodes = sp.split_nodes_link([node])
        self.assertEqual(new_nodes,[
            TextNode("This is text with a ",TextType.TEXT),
            TextNode("link to boot dev",TextType.LINK,"https://www.boot.dev"),
            TextNode(", an ![image](https://i.imgur.com/zjjcJKZ.png) and ",TextType.TEXT),
            TextNode("another link",TextType.LINK,"https://www.youtube.com/@bootdotdev"),
            TextNode(".",TextType.TEXT),
            ])
        
        node = TextNode(
            "[Begin with a link](url), then raw text and a last [link](url2)",
            TextType.TEXT,
        )
        new_nodes = sp.split_nodes_link([node])
        self.assertEqual(new_nodes,[
            TextNode("Begin with a link",TextType.LINK,"url"),
            TextNode(", then raw text and a last ",TextType.TEXT),
            TextNode("link",TextType.LINK,"url2"),
            ])
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = sp.text_to_textnodes(text)
        self.assertEqual(result, textnodes)
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = sp.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
        md = """

This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
This is a wrong block
"""
        blocks = sp.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items\nThis is a wrong block",
            ],
        )