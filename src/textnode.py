from enum import Enum

from leafnode import LeafNode

class TextType(Enum):
    TEXT = 'normal_text'
    BOLD = 'bold_text'
    ITALIC = 'italic_text'
    CODE = 'code_text'
    LINK = 'link'
    IMAGE = 'image'
    
class TextNode:
    def __init__(self, text, type, url = None):
        self.text = text
        self.text_type = type
        self.url = url
    
    def __eq__(self, value):
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_html_node(self):
        if self.text_type == TextType.TEXT :
            return LeafNode(tag=None,value=self.text)
        elif self.text_type == TextType.BOLD :
            return LeafNode(tag="b",value=self.text)
        elif self.text_type == TextType.ITALIC :
            return LeafNode(tag="i",value=self.text)
        elif self.text_type == TextType.CODE :
            return LeafNode(tag="code",value=self.text)
        elif self.text_type == TextType.LINK :
            return LeafNode(tag="a",value=self.text,props={"href":self.url})
        elif self.text_type == TextType.IMAGE :
            return LeafNode(tag="img",value="",props={"src":self.url, "alt":self.text})
        else :
            raise Exception