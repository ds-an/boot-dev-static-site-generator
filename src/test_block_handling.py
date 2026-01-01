import unittest

from block_handling import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_2(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )
    def test_block_to_block_type_heading(self):
        md = """
# This is a heading
"""
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )
    def test_block_to_block_type_code(self):
        md = "```This is a code block```"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )
    def test_block_to_block_type_quote(self):
        md = ">This is a quote block\n>That continues here\n>And ends here"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )
    def test_block_to_block_type_quote_2(self):
        md = ">This is an invalid quote block\nThat continues here\n>And ends here"
        block_type = block_to_block_type(md)
        self.assertNotEqual(
            block_type,
            BlockType.QUOTE
        )
    def test_block_to_block_type_unordered_list(self):
        md = "- This is an unordered list\n- That continues here\n- And ends here"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )
    def test_block_to_block_type_ordered_list(self):
        md = "1. This is an ordered list\n2. That continues here\n3. And ends here"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )
    def test_block_to_block_type_ordered_list_2(self):
        md = "1. This is an invalid ordered list\n10. That continues here\n3. And ends here"
        block_type = block_to_block_type(md)
        self.assertNotEqual(
            block_type,
            BlockType.ORDERED_LIST
        )
    def test_block_to_block_type_paragraph(self):
        md = "This is a paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )
    def test_markdown_to_html_node(self):
        md = "1. This is an ordered list\n2. That continues here\n3. And ends here\n\n- This is an unordered list\n- That continues here\n- And ends here"
        block_type = markdown_to_html_node(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )
    def test_markdown_to_html_node_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    # def test_markdown_to_html_node_codeblock(self):
    #     md = """
    # ```
    # This is text that _should_ remain
    # the **same** even with inline stuff
    # ```
    # """
    #
    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    #     )
