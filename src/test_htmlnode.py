import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props={"href": "https://www.google.com",
                               "target": "_blank"})
        self.assertEqual(node.props["href"], "https://www.google.com")

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com",
                               "target": "_blank"})
        to_props_output = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), to_props_output)

    def test_props_to_html_more(self):
        node = HTMLNode(props={"href": "https://www.google.com",
                               "target": "_blank",
                               "someprop": "somevalue"})
        to_props_output = " href=\"https://www.google.com\" target=\"_blank\" someprop=\"somevalue\""
        self.assertEqual(node.props_to_html(), to_props_output)

if __name__ == "__main__":
    unittest.main()
