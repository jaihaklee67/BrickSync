import fs from 'fs';

const path = 'web_app/lesson.html';
const content = fs.readFileSync(path, 'utf8');

const searchStart = `                let currentBleDelay = 0;
                let bleGlobalMotorSpeed = 40;
                const bleQueue = [];

                blocks.forEach((block) => {`;
const searchEnd = `                }, currentBleDelay + 500);`;

const startIndex = content.indexOf(searchStart);
const endIndex = content.indexOf(searchEnd) + searchEnd.length;

if (startIndex === -1 || endIndex < startIndex) {
    console.log("Boundary not found");
    process.exit(1);
}

// Extract the inner body of the `blocks.forEach` loop
const blocksForEachCodeMatch = content.match(/blocks\.forEach\(\(block\) => \{([\s\S]*?)\}\);/);
if (!blocksForEachCodeMatch) {
    console.log("Internal blocks.forEach body not found");
    process.exit(1);
}

// Extract the switch cases inside exactly
const originalBody = blocksForEachCodeMatch[1]; // Includes action extraction, logic, switch cases.

const newLogic = `                // 엔진 실행 식별자 (중복 실행 방지 및 예전 루프 취소용)
                window.bleEngineRunCounter = (window.bleEngineRunCounter || 0) + 1;
                const currentRunId = window.bleEngineRunCounter;

                console.log(\`🚀 [BLE_ENGINE] Starting \${validStacks.length} concurrent block stacks (RunID: \${currentRunId})\`);

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

                    stackBlocks.forEach((block) => {\${originalBody}});

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
                                console.log(\`\\u23F1\\uFE0F [BLE_ENGINE] Executing cmd: \${cmd.action} (waitTime: \${waitTime}ms)\`);

                                if (waitTime > 0 && cmd.action !== 'wait_color') {
                                    await new Promise(r => setTimeout(r, waitTime));
                                    lastExecutionTime = cmd.delay;
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
                                    console.log(\`\\u23F1\\uFE0F [BLE_ENGINE] Waiting for Color Sensor to detect color ID: \${cmd.targetColor}\`);
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
                                        if (!matched) await new Promise(r => setTimeout(r, 100));
                                    }
                                    if (!matched) return; // 루프가 외부 요인으로 중단된 경우
                                    console.log(\`\\u2705 [BLE_ENGINE] Target Color \${cmd.targetColor} Detected! Continuing sequence...\`);
                                    
                                    // 주의! 대기했던 시간은 무시하고, 이 블록부터 다시 타임라인이 계산되도록
                                    // 현재 실제 경과 시간에 맞춰야 하므로, 이 시점을 0 으로 삼아야 하지만
                                    // 큐 기반이므로, delay 누적치는 그냥 통과시키면 됩니다.
                                    lastExecutionTime = cmd.delay; 
                                }
                            } catch (e) {
                                console.error("❌ [BLE_ENGINE] Command Error:", e);
                            }
                        }
                    };

                    if (isEventLoop) {
                        (async () => {
                            // 이벤트 핸들러 역할을 위해 조건 만족 후 실행이 끝나면 다시 대기 상태로!
                            while (window.bleEngineRunCounter === currentRunId) {
                                await executeBleQueue();
                                await new Promise(r => setTimeout(r, 500)); // 중복 폭주 방지 쿨다운
                            }
                        })();
                    } else {
                        executeBleQueue();
                    }
                });

                // 게임 전송 로직
                setTimeout(() => {
                    if (blockCount > 1 && anySequenceFound && window.bleEngineRunCounter === currentRunId) {
                        triggerSuccessConfetti();
                        try { window.parent.sendWebSocketAction({ action: "CAT_FEED_REWARD" }); } catch (e) { }
                    }
                }, maxGlobalDelay + 1000);`;

const newContent = content.substring(0, startIndex) + newLogic + content.substring(endIndex);
fs.writeFileSync(path, newContent, 'utf8');
console.log("Successfully replaced!");
