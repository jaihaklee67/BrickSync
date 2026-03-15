const fs = require('fs');

let html = fs.readFileSync('web_app/lesson.html', 'utf8');

// 1. Remove cache clearing
html = html.replace(/window\.parent\.sensorData = {};/g, "// 캐시 초기화 제거 (현재 상태 유지)\n");

const sStr = "const backgroundLoop = async () => {";
const eStr = "};";

let s = html.indexOf(sStr);
let searchEnd = html.indexOf(eStr, s);

if (s > -1) {
    let oldLoopBlock = html.substring(s, html.indexOf("// 블로킹 없이 백그라운드로 실행을 던져놓음"));

    const newTargetLoop = `const backgroundLoop = async () => {
                            let lastColorMatched = false;
                            while (window.bleEngineRunCounter === currentRunId) {
                                if (!isExecuting) {
                                    isExecuting = true;
                                    await runBlocksSeq(rootBlocks).catch(() => { });
                                    
                                    // 무한 반복 방지를 위한 엣지 트리거 (블럭 치울 때까지 대기)
                                    let targetCol = 9; // 기본 빨간색 (또는 rootBlocks[0]의 paramVal에서 추출 가능하지만 여기서는 단순화하여 9로 가정하거나 직접 파싱)
                                    if(rootBlocks[0] && rootBlocks[0].getAttribute('data-action') === 'event_color_sensor') {
                                        let matched = false;
                                        // 현재 스택의 센서 파라미터 값 추출 (어려우면 대략적인 방식으로)
                                        let pEl = rootBlocks[0].querySelector('.block-param:not(.param-time)');
                                        if (pEl) {
                                            targetCol = parseFloat(pEl.getAttribute('data-val') || pEl.innerText.trim()) || 9;
                                        }

                                        let cleared = false;
                                        while (!cleared && window.bleEngineRunCounter === currentRunId) {
                                            let stillDetecting = false;
                                            if (window.parent.sensorData) {
                                                for(let p=0; p<6; p++){
                                                    if(window.parent.sensorData[p] === targetCol) stillDetecting = true;
                                                }
                                            }
                                            if(!stillDetecting) cleared = true;
                                            else await new Promise(r => setTimeout(r, 100));
                                        }
                                    }

                                    isExecuting = false;
                                }
                                await new Promise(r => setTimeout(r, 50));
                            }
                        };
                        `;
    html = html.replace(oldLoopBlock, newTargetLoop);
    fs.writeFileSync('web_app/lesson.html', html, 'utf8');
    console.log("REPLACED LOOP SUCCESSFULLY");
} else {
    console.log("COULD NOT FIND", sStr);
}
