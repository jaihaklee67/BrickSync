import os, glob

folder = "C:/Users/PC/Documents/GitHub/BrickSync/bricksync_project/web_app/"
html_files = glob.glob(folder + "*.html")

for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the target elements and replace naive links
    # For A tags:
    content = content.replace('href="index.html"', 'href="#" onclick="location.href=\'index.html?v=\'+new Date().getTime(); return false;"')
    content = content.replace('href="workspace.html"', 'href="#" onclick="location.href=\'workspace.html?v=\'+new Date().getTime(); return false;"')
    content = content.replace('href="ai_lab.html"', 'href="#" onclick="location.href=\'ai_lab.html?v=\'+new Date().getTime(); return false;"')

    # For onclick events:
    # Need to be extremely careful. If it already has '?v=', we skip it.
    if "?v=" not in content:
        content = content.replace("location.href='index.html'", "location.href='index.html?v='+new Date().getTime()")
        content = content.replace("location.href='ai_lab.html'", "location.href='ai_lab.html?v='+new Date().getTime()")
        content = content.replace("location.href='workspace.html'", "location.href='workspace.html?v='+new Date().getTime()")
        content = content.replace('window.location.href = "index.html"', 'window.location.href = "index.html?v=" + new Date().getTime()')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Busted caching across {len(html_files)} files!")
