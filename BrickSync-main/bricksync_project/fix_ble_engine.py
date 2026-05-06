import codecs

path = 'web_app/lesson.html'
with codecs.open(path, 'r', 'utf-8') as f:
    html = f.read()

startMarker = "            if (window.parent.connectionType === 'BLE') {"
endMarker = "            try {\n                await writeToHub('\\x03\\x03');"

s = html.find(startMarker)
e = html.find(endMarker)

if s == -1 or e == -1:
    print("Markers not found", s, e)
    exit(1)

newBLE = """            if (window.parent.connectionType === 'BLE') {
                window.bleEngineRunCounter = (window.bleEngineRunCounter || 0) + 1;
                const currentRunId = window.bleEngineRunCounter;
                console.log(`🚀 [BLE_ENGINE] Starting ${validStacks.length} concurrent block stacks (RunID: ${currentRunId})`);

                let anySequenceFound = false;

                const executeStack = async (stack) => {
                    const stackBlocks = Array.from(stack.querySelectorAll('.workspace-item'));
                    if (stackBlocks.length === 0) return;
                    anySequenceFound = true;

                    const parseBlock = (block) => {
                        const action = block.getAttribute('data-action');
                        let paramVal = 1; let timeVal = 1; let paramEl = null;

                        if (action === 'motor_cw' || action === 'motor_ccw') {
                            const timeEl = block.querySelector('.block-param');
                            if (timeEl) {
                                if (timeEl.hasAttribute('data-val')) timeVal = parseFloat(timeEl.getAttribute('data-val'));
                                else { const tv = timeEl.innerText.trim(); if (!isNaN(tv) && tv !== "") timeVal = parseFloat(tv); }
                            }
                        } else {
                            paramEl = block.querySelector(':scope > .block-param:not(.param-time)') || block.querySelector('.block-param:not(.param-time)');
                            if (paramEl) {
                                if (paramEl.hasAttribute('data-val')) paramVal = parseFloat(paramEl.getAttribute('data-val'));
                                else { const tv = paramEl.innerText.trim(); if (!isNaN(tv) && tv !== "") paramVal = parseFloat(tv); }
                            }
                            const timeEl = block.querySelector(':scope > .param-time') || block.querySelector('.param-time');
                            if (timeEl) {
                                if (timeEl.hasAttribute('data-val')) timeVal = parseFloat(timeEl.getAttribute('data-val'));
                                else { const tv = timeEl.innerText.trim(); if (!isNaN(tv) && tv !== "") timeVal = parseFloat(tv); }
                            }
                        }
                        if (paramVal === -1) paramVal = Math.floor(Math.random() * 3) + 1;
                        if (timeVal === -1) timeVal = Math.floor(Math.random() * 3) + 1;
                        return { action, paramVal, timeVal, paramEl, block };
                    };

                    let bleGlobalMotorSpeed = 40;

                    const runBlocksSeq = async (blocksArray) => {
                        for (const block of blocksArray) {
                            if (window.bleEngineRunCounter !== currentRunId) return;
                            const parsed = parseBlock(block);
                            blockCount++;

                            switch (parsed.action) {
                                case 'motor_speed_set':
                                    bleGlobalMotorSpeed = parsed.paramVal;
                                    break;
                                case 'motor_cw':
                                case 'motor_ccw':
                                    let speed = bleGlobalMotorSpeed;
                                    if (parsed.action === 'motor_ccw') speed = -speed;
                                    let deg = Math.floor(parsed.timeVal * 360);
                                    let d1 = deg & 0xFF; let d2 = (deg >> 8) & 0xFF; let d3 = (deg >> 16) & 0xFF; let d4 = (deg >> 24) & 0xFF;
                                    let speedHex = speed < 0 ? (256 + speed) : speed;
                                    for (let p=0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev === 64 || dev === 61 || dev === 62 || dev === 63 || dev === 57 || dev === 59) continue;
                                        let payload = [14, 0x00, 0x81, p, 0x11, 0x0B, d1, d2, d3, d4, speedHex, 100, 127, 3];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                    let estTimeMs = (deg / Math.max(10, Math.abs(speed))) * 100; 
                                    if (estTimeMs < 100) estTimeMs = 100;
                                    await new Promise(r => setTimeout(r, estTimeMs + 200)); 
                                    break;
                                case 'motor_stop':
                                    for (let p=0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev === 64 || dev === 61 || dev === 62 || dev === 63 || dev === 57 || dev === 59) continue;
                                        await window.parent.writeToHub(new Uint8Array([7, 0, 0x81, p, 0x10, 0x01, 0])); // power 0
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                    break;
                                case 'sound_play':
                                    await new Promise(r => setTimeout(r, 4000));
                                    break;
                                case 'event_color_sensor':
                                    console.log(`⏱️ [BLE] Waiting for color: ${parsed.paramVal}.. clearing old state first.`);
                                    
                                    // 중요: 이전 측정값이 남아있어 바로 통과하는 버그 패치! (기다릴 때만 센서를 확인)
                                    // 센서 데이터 갱신을 위해 최소한의 폴링 대기시간을 준 후 값을 검증합니다.
                                    window.parent.sensorData = {}; // 기존 센서 측정치 캐시 무효화 강제

                                    let matched = false;
                                    while (!matched && window.bleEngineRunCounter === currentRunId) {
                                        if (window.parent.sensorData) {
                                            for (let p = 0; p < 6; p++) {
                                                if (window.parent.sensorData[p] === parsed.paramVal) {
                                                    matched = true; 
                                                    break;
                                                }
                                            }
                                        }
                                        await new Promise(r => setTimeout(r, 100)); // 실시간 계속 폴링
                                    }
                                    if(!matched) return;
                                    console.log(`✅ [BLE] Color ${parsed.paramVal} detected! Proceeding to next block.`);
                                    // 모터 등 다음 블럭으로 넘어가기 위해 약간 딜레이 확보 (블루투스 부하 줄임)
                                    await new Promise(r => setTimeout(r, 200));
                                    break;
                                case 'flow_wait':
                                    await new Promise(r => setTimeout(r, parsed.paramVal * 1000));
                                    break;
                                case 'matrix_pixel':
                                    let matEl = parsed.block.querySelector('.param-unified') || parsed.block.querySelector('.block-param:not(.param-time)');
                                    let matrixArrBLE = matEl ? (matEl.getAttribute('data-matrix') || JSON.stringify([0,6,0,0,0,0,6,0,6])) : JSON.stringify([0,6,0,0,0,0,6,0,6]);
                                    let mBleTime = matEl ? (parseFloat(matEl.getAttribute('data-val')) || 2) : 2;
                                    let mArr = JSON.parse(matrixArrBLE);
                                    let encodedColors = mArr.map(c => c > 0 ? c + 160 : 0);
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev !== undefined && dev !== 64) continue;
                                        let payload = [16, 0, 0x81, p, 0x10, 0x51, 0x02, ...encodedColors];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 30));
                                    }
                                    await new Promise(r => setTimeout(r, mBleTime * 1000));
                                    
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev !== undefined && dev !== 64) continue;
                                        let payload = [16, 0, 0x81, p, 0x10, 0x51, 0x02, 0,0,0,0, 0,0,0,0, 0];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                    await window.parent.writeToHub(new Uint8Array([8, 0, 0x81, 50, 0x10, 0x51, 0x00, 0]));
                                    break;
                                case 'matrix_clear':
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev !== undefined && dev !== 64) continue;
                                        let payload = [16, 0, 0x81, p, 0x10, 0x51, 0x02, 0,0,0,0, 0,0,0,0, 0];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                    await window.parent.writeToHub(new Uint8Array([8, 0, 0x81, 50, 0x10, 0x51, 0x00, 0]));
                                    break;
                                case 'control_repeat':
                                case 'control_forever':
                                    let iters = parsed.action === 'control_forever' ? Infinity : parsed.paramVal;
                                    const innerStack = parsed.block.querySelector(':scope > .loop-inner-stack');
                                    let children = [];
                                    if (innerStack) children = Array.from(innerStack.children).filter(b => b.classList.contains('workspace-item') && !b.classList.contains('placeholder'));
                                    
                                    for (let i = 0; i < iters; i++) {
                                        if (window.bleEngineRunCounter !== currentRunId) break;
                                        await runBlocksSeq(children);
                                    }
                                    break;
                            }
                        }
                    };
                    
                    let rootBlocks = Array.from(stack.children).filter(b => b.classList.contains('workspace-item') && !b.classList.contains('placeholder'));
                    
                    const firstAction = rootBlocks[0] ? rootBlocks[0].getAttribute('data-action') : '';
                    if (firstAction && firstAction.startsWith('event_')) {
                        // Event loop continuously monitors the stack (무한 루프로 이벤트 감시)
                        while (window.bleEngineRunCounter === currentRunId) {
                            await runBlocksSeq(rootBlocks);
                            await new Promise(r => setTimeout(r, 200)); 
                        }
                    } else {
                        // 순차적 1회 실행
                        await runBlocksSeq(rootBlocks);
                    }
                };

                Promise.all(validStacks.map(stack => executeStack(stack))).then(() => {
                    if (window.bleEngineRunCounter === currentRunId && anySequenceFound && blockCount > 1) {
                        triggerSuccessConfetti();
                        try { window.parent.sendWebSocketAction({ action: "CAT_FEED_REWARD" }); console.log("포트나이트 연동 신호(CAT_FEED_REWARD) 전송 완료 [BLE]"); } catch (e) { }
                    }
                });
                
                return;
            }
"""

html = html[:s] + newBLE + html[e:]
with codecs.open(path, 'w', 'utf-8') as f:
    f.write(html)
print("SUCCESS Python patch for BLE Engine")
