import unittest
from site_generation import copy_source_to_dest_dir, extract_title

class TestSiteGeneration(unittest.TestCase):
    def test_extract_title(self):
        title = ""
        with open("content/index.md", "r") as reader:
            md = reader.read()
            title = extract_title(md)
        self.assertEqual(title, "Tolkien Fan Club")
