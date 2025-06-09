from enum import Enum

class TextType(Enum):
    NORMAL = 'normal_text'
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