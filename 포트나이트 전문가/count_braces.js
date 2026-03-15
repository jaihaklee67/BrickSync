const fs = require('fs');
const html = fs.readFileSync('c:/Users/PC/Desktop/anti_2/bricksync_project/web_app/lesson.html', 'utf8');

const regex = /<script.*?>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;

while ((match = regex.exec(html)) !== null) {
    const script = match[1];
    let open = 0, close = 0;
    
    // strip comments to avoid false positives (simple)
    const stripped = script.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*/g, '');
    
    for (let char of stripped) {
        if (char === '{') open++;
        if (char === '}') close++;
    }
    console.log(`Script ${count}: { = ${open}, } = ${close}, diff = ${open - close}`);
    count++;
}
