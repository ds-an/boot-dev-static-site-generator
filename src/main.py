from site_generation import copy_source_to_dest_dir, generate_page

def main():
    copy_source_to_dest_dir("static", "public")
    generate_page("content/index.md", "template.html", "public")
    
main()
