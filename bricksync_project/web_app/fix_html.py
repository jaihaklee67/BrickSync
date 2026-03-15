import os, glob

# Since we want to rename index.html -> workspace.html
# and menu.html -> index.html
# We must first read the files before renaming. Wait, reading them all and substituting string contents is fine regardless of how they are named, if we do it carefully.
# Actually, the easiest way: replace inside files FIRST, then rename files.

html_files = glob.glob('*.html')
for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Replace index.html with workspace.html
    new_content = content.replace('"index.html"', '"workspace.html"').replace("'index.html'", "'workspace.html'")
    # 2. Replace menu.html with index.html
    new_content = new_content.replace('"menu.html"', '"index.html"').replace("'menu.html'", "'index.html'")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)

# Now rename the files
os.rename('index.html', 'workspace.html')
os.rename('menu.html', 'index.html')

print("All files updated and renamed successfully.")
