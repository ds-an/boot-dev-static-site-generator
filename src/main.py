from site_generation import copy_source_to_dest_dir, generate_page, generate_pages_recursive
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_source_to_dest_dir("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
main()
