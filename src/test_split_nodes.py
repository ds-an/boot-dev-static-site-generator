import unittest

from textnode import TextNode, TextType

from node_operations import split_nodes_delimiter


class TestSplitNodes(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is a node with **bold text**.", TextType.PLAIN)
        result = [
            TextNode("This is a node with ", TextType.PLAIN),
            TextNode("bold text", TextType.BOLD),
            TextNode(".", TextType.PLAIN)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), result)
    def test_italic(self):
        node = TextNode("This is a node with no end dot and _italic text_", TextType.PLAIN)
        result = [
            TextNode("This is a node with no end dot and ", TextType.PLAIN),
            TextNode("italic text", TextType.ITALIC),
        ]
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), result)
    def test_code(self):
        node = TextNode("This is a node with _code text_ and a few words after.", TextType.PLAIN)
        result = [
            TextNode("This is a node with ", TextType.PLAIN),
            TextNode("code text", TextType.CODE),
            TextNode(" and a few words after.", TextType.PLAIN),
        ]
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.CODE), result)
