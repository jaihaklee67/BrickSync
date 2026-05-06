const fs = require('fs');
const html = fs.readFileSync('c:/Users/PC/Desktop/anti_2/bricksync_project/web_app/lesson.html', 'utf8');

let blockStart = html.indexOf("\`\\${indent}try:\\n\`");
let blockEnd = html.indexOf("\`\\${indent}except:\\n\\${indent}  pass\\n\`;");

if(blockStart !== -1 && blockEnd !== -1) {
    console.log("Found snippet block");
}
