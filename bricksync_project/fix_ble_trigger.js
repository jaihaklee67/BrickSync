const fs = require('fs');

let html = fs.readFileSync('web_app/lesson.html', 'utf8');

// 1. Remove cache clearing
const badCacheLine = "                                    window.parent.sensorData = {};";
html = html.replace(badCacheLine, "                                    // 캐시 초기화 제거 (현재 상태 즉시 반영 위함)");

// 2. Add edge trigger (wait for clear) logic
const oldLoop = `                        // 백그라운드 무한 루프 런처
                        const backgroundLoop = async () => {
                            while (window.bleEngineRunCounter === currentRunId) {
                                if (!isExecuting) {
                                    isExecuting = true;
                                    await runBlocksSeq(rootBlocks).catch(() => { });
                                    // 한 바퀴 시퀀스 다 돈 다음엔 모터/조명이 끝났을 때 다시 센싱 모드로 복귀
                                    isExecuting = false;
                                }
                                await new Promise(r => setTimeout(r, 100));
                            }
                        };`;

const newLoop = `                        // 백그라운드 무한 루프 런처
                        const backgroundLoop = async () => {
                            while (window.bleEngineRunCounter === currentRunId) {
                                if (!isExecuting) {
                                    isExecuting = true;
                                    await runBlocksSeq(rootBlocks).catch(() => { });
                                    
                                    // 무한 반복 방지를 위한 엣지 트리거 (블럭 치울 때까지 대기)
                                    let targetCol = 9; // 기본 빨간색
                                    const pEl = rootBlocks[0].querySelector('.block-param:not(.param-time)');
                                    if(pEl) {
                                        let val = parseFloat(pEl.getAttribute('data-val') || pEl.innerText.trim());
                                        if(!isNaN(val)) targetCol = val;
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
                                        else await new Promise(r => setTimeout(r, 50));
                                    }

                                    // 한 바퀴 시퀀스 다 돈 다음엔 모터/조명이 끝났을 때 다시 센싱 모드로 복귀
                                    isExecuting = false;
                                }
                                await new Promise(r => setTimeout(r, 50));
                            }
                        };`;

if (html.indexOf(oldLoop) > -1) {
    html = html.replace(oldLoop, newLoop);
    fs.writeFileSync('web_app/lesson.html', html, 'utf8');
    console.log("SUCCESS");
} else {
    console.log("FAILED to find loop string");
}
