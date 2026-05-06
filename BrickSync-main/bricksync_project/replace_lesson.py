import re

with open('web_app/lesson.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = "                let currentBleDelay = 0;"
end_marker = "                }, currentBleDelay + 500);"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Not found")
    exit(1)

content_to_replace = text[start_idx:end_idx + len(end_marker)]

match = re.search(r"blocks\.forEach\(\(block\) => \{(.*?)\}\);\s+// 블록 전체 실행", content_to_replace, re.DOTALL)
if not match:
    print("Inner body not found")
    exit(1)

inner_body = match.group(1)

new_logic = """                // 엔진 실행 식별자 (중복 실행 방지 및 예전 루프 취소용)
                window.bleEngineRunCounter = (window.bleEngineRunCounter || 0) + 1;
                const currentRunId = window.bleEngineRunCounter;

                console.log(`🚀 [BLE_ENGINE] Starting ${validStacks.length} concurrent block stacks (RunID: ${currentRunId})`);

                let maxGlobalDelay = 0;
                let anySequenceFound = false;

                validStacks.forEach((stack) => {
                    const stackBlocks = Array.from(stack.querySelectorAll('.workspace-item'));
                    if (stackBlocks.length === 0) return;
                    
                    anySequenceFound = true;
                    const firstAction = stackBlocks[0].getAttribute('data-action');
                    const isEventLoop = firstAction.startsWith('event_');

                    let currentBleDelay = 0;
                    let bleGlobalMotorSpeed = 40;
                    const bleQueue = [];

                    stackBlocks.forEach((block) => {""" + inner_body + """});

                    if (currentBleDelay > maxGlobalDelay) {
                        maxGlobalDelay = currentBleDelay;
                    }

                    const executeBleQueue = async () => {
                        let lastExecutionTime = 0;
                        for (const cmd of bleQueue) {
                            if (window.bleEngineRunCounter !== currentRunId) return; // 이전 실행 취소됨
                            try {
                                // 누적 딜레이(cmd.delay)와 이전 실행 시간(lastExecutionTime)의 차이만큼만 대기
                                const waitTime = cmd.delay - lastExecutionTime;
                                
                                if (waitTime > 0 && cmd.action !== 'wait_color') {
                                    console.log(`⏱️ [BLE_ENGINE] Executing cmd: ${cmd.action} (waitTime: ${waitTime}ms)`);
                                    await new Promise(r => setTimeout(r, waitTime));
                                    lastExecutionTime = cmd.delay;
                                } else if (cmd.action !== 'wait_color') {
                                    console.log(`⏱️ [BLE_ENGINE] Executing cmd: ${cmd.action} (waitTime: 0ms)`);
                                }

                                if (cmd.action === 'motor') {
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev === 64 || dev === 61 || dev === 62 || dev === 63 || dev === 57 || dev === 59) continue;

                                        let speedInt = Math.round(cmd.speed);
                                        let speedHex = speedInt < 0 ? (256 + speedInt) : speedInt;
                                        await window.parent.writeToHub(new Uint8Array([7, 0, 0x81, p, 0x10, 0x01, speedHex]));
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                } else if (cmd.action === 'matrix') {
                                    let encodedColors = cmd.colors.map(c => c > 0 ? c + 160 : 0);
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev !== undefined && dev !== 64) continue;

                                        let payload = [16, 0, 0x81, p, 0x10, 0x51, 0x02, ...encodedColors];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 30));
                                    }
                                } else if (cmd.action === 'matrix_clear') {
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev !== undefined && dev !== 64) continue;

                                        let payload = [16, 0, 0x81, p, 0x10, 0x51, 0x02, 0, 0, 0, 0, 0, 0, 0, 0, 0];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                    await window.parent.writeToHub(new Uint8Array([8, 0, 0x81, 50, 0x10, 0x51, 0x00, 0]));
                                } else if (cmd.action === 'wait_color') {
                                    console.log(`⏱️ [BLE_ENGINE] Waiting for Color Sensor to detect color ID: ${cmd.targetColor}`);
                                    let matched = false;
                                    while (!matched && window.bleEngineRunCounter === currentRunId) {
                                        if (window.parent.sensorData) {
                                            for (let p = 0; p < 6; p++) {
                                                if (window.parent.hubDevices && window.parent.hubDevices[p] === 61) {
                                                    if (window.parent.sensorData[p] === cmd.targetColor) {
                                                        matched = true;
                                                        break;
                                                    }
                                                }
                                            }
                                        }
                                        if (!matched) await new Promise(r => setTimeout(r, 100)); // 폴링 주기 100ms
                                    }
                                    if (!matched) return; // 외부 취소
                                    console.log(`✅ [BLE_ENGINE] Target Color ${cmd.targetColor} Detected! Continuing sequence...`);
                                    
                                    // 주의! 대기했던 시간은 동기화되어야 하므로, 이 이벤트를 지나치면 지체되었던 시간을 리셋해야 함.
                                    // 큐에서 정의된 다음 애니메이션 시간차가 유지되도록 lastExecutionTime을 현재 cmd.delay로 땡겨옴.
                                    lastExecutionTime = cmd.delay; 
                                }
                            } catch (e) {
                                console.error("❌ [BLE_ENGINE] Command Error:", e);
                            }
                        }
                    };

                    if (isEventLoop) {
                        (async () => {
                            // 이벤트 루프: 조건이 만족되어 전체 큐가 실행된 후 계속해서 이벤트를 감시
                            while (window.bleEngineRunCounter === currentRunId) {
                                await executeBleQueue();
                                await new Promise(r => setTimeout(r, 500)); // 무한 폭주 방지 쿨다운
                            }
                        })();
                    } else {
                        executeBleQueue();
                    }
                });

                // 게임 시작시 폭죽 쏘기 등 블록 카운트 로직
                setTimeout(() => {
                    if (blockCount > 1 && anySequenceFound && window.bleEngineRunCounter === currentRunId) {
                        triggerSuccessConfetti();
                        try { window.parent.sendWebSocketAction({ action: "CAT_FEED_REWARD" }); console.log("포트나이트 연동 신호(CAT_FEED_REWARD) 전송 완료 [BLE]"); } catch (e) { }
                    }
                }, maxGlobalDelay + 1000);"""

text = text[:start_idx] + new_logic + text[end_idx + len(end_marker):]

with open('web_app/lesson.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("PYTHON REPLACE SUCCESS!")
