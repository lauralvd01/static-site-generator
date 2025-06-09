from textnode import TextNode
from textnode import TextType

def main():
    print(TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev'))
    print(TextNode('This is some normal text', TextType.NORMAL))
    

main()