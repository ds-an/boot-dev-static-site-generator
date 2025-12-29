import unittest

from textnode import TextNode, TextType

from node_operations import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


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
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_link_at_the_start(self):
        node = TextNode(
            "[This link](https://i.imgur.com/zjjcJKZ.png) is at the start of the string.",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is at the start of the string.", TextType.PLAIN),
            ],
            new_nodes,
        )
    def test_split_image_at_the_end(self):
        node = TextNode(
            "At the end of this string is an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("At the end of this string is an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    def test_split_text(self):
        text_for_nodes = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text_for_nodes)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )   
