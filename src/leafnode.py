from htmlnode import HTMLNode

"""
A LeafNode is a type of HTMLNode that represents a single HTML tag with no children. 
For example, a simple <p> tag with some text inside of it.
In this next example, <p> is not a leaf node, but <b> is :
<p>
  This is a paragraph. It can have a lot of text inside tbh.
  <b>This is bold text.</b>
  This is the last sentence.
</p>
"""
class LeafNode(HTMLNode):
    
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    """
    Returns a string that represents the HTML tag string of the node.
    """
    def to_html(self):
        if self.value is None :
            raise ValueError("LeafNode must have a value")
        if self.tag is None :
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    