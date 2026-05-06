const fs = require('fs');


const path = 'web_app/lesson.html';
const content = fs.readFileSync(path, 'utf8');

// The corrupted block starts at `if (window.parent.connectionType === 'BLE') {`
// And ends at `try {\n                await writeToHub('\\x03\\x03');`
const startMarker = `            if (window.parent.connectionType === 'BLE') {`;
const endMarker = `            try {
                await writeToHub('\\x03\\x03');`;

const startIndex = content.indexOf(startMarker);
const endIndex = content.indexOf(endMarker);

if (startIndex === -1 || endIndex === -1) {
    console.error("Markers not found");
    process.exit(1);
}

const cleanBLELogic = `            if (window.parent.connectionType === 'BLE') {
                // ===============================================
                // BLE Î¨¥ÏÑ† ?§ÏãúÍ∞?Î∏îÎ°ù ?îÏßÑ (Î≤ÑÏ∏Ñ??Î®∏Ïã†)
                // LWP3 Í≥µÏãù ?ÑÎ°ú?†ÏΩú???¥Ïö©??Î∞îÏù¥?àÎ¶¨ Î™®ÌÑ∞ ?®ÌÇ∑ ?ÑÏÜ°
                // ===============================================
                // ?îÏßÑ ?§Ìñâ ?ùÎ≥Ñ??(Ï§ëÎ≥µ ?§Ìñâ Î∞©Ï? Î∞??àÏ†Ñ Î£®ÌîÑ Ï∑®ÏÜå??
                window.bleEngineRunCounter = (window.bleEngineRunCounter || 0) + 1;
                const currentRunId = window.bleEngineRunCounter;

                console.log(\`?? [BLE_ENGINE] Starting \${validStacks.length} concurrent block stacks (RunID: \${currentRunId})\`);

                let maxGlobalDelay = 0;
                let anySequenceFound = false;

                validStacks.forEach((stack) => {
                    const stackBlocks = Array.from(stack.querySelectorAll('.workspace-item'));
                    if (stackBlocks.length === 0) return;
                    
                    anySequenceFound = true;
                    // Ï≤?Î∏îÎ°ù???¥Î≤§??Î∏îÎ°ù?∏Ï?(StartÍ∞Ä ?ÑÎãåÏßÄ) ?ïÏù∏
                    const firstAction = stackBlocks[0].getAttribute('data-action');
                    const isEventLoop = firstAction !== 'start';

                    let currentBleDelay = 0;
                    let bleGlobalMotorSpeed = 40;
                    const bleQueue = [];

                    stackBlocks.forEach((block) => {
                        const action = block.getAttribute('data-action');
                        blockCount++; // ?¨Í∏∞???ÑÏ†Å?¥ÎèÑ ?àÏ†Ñ

                        let paramVal = 1;
                        let timeVal = 1;
                        let paramEl = null;

                        if (action === 'motor_cw' || action === 'motor_ccw') {
                            const timeEl = block.querySelector('.block-param');
                            if (timeEl) {
                                if (timeEl.hasAttribute('data-val')) timeVal = parseFloat(timeEl.getAttribute('data-val'));
                                else {
                                    const textVal = timeEl.innerText.trim();
                                    if (!isNaN(textVal) && textVal !== "") timeVal = parseFloat(textVal);
                                }
                            }
                        } else {
                            paramEl = block.querySelector('.block-param:not(.param-time)');
                            if (paramEl) {
                                if (paramEl.hasAttribute('data-val')) paramVal = parseFloat(paramEl.getAttribute('data-val'));
                                else {
                                    const textVal = paramEl.innerText.trim();
                                    if (!isNaN(textVal) && textVal !== "") paramVal = parseFloat(textVal);
                                }
                            }

                            const timeEl = block.querySelector('.param-time');
                            if (timeEl) {
                                if (timeEl.hasAttribute('data-val')) timeVal = parseFloat(timeEl.getAttribute('data-val'));
                                else {
                                    const textVal = timeEl.innerText.trim();
                                    if (!isNaN(textVal) && textVal !== "") timeVal = parseFloat(textVal);
                                }
                            }
                        }

                        if (paramVal === -1) paramVal = Math.floor(Math.random() * 3) + 1;
                        if (timeVal === -1) timeVal = Math.floor(Math.random() * 3) + 1;

                        switch (action) {
                            case 'motor_speed_set':
                                bleGlobalMotorSpeed = paramVal === -1 ? 40 : paramVal;
                                break;
                            case 'motor_cw':
                                bleQueue.push({ action: 'motor', speed: bleGlobalMotorSpeed, delay: currentBleDelay });
                                currentBleDelay += (timeVal * 1000);
                                bleQueue.push({ action: 'motor', speed: 0, delay: currentBleDelay });
                                currentBleDelay += 300;
                                break;
                            case 'motor_ccw':
                                bleQueue.push({ action: 'motor', speed: -bleGlobalMotorSpeed, delay: currentBleDelay });
                                currentBleDelay += (timeVal * 1000);
                                bleQueue.push({ action: 'motor', speed: 0, delay: currentBleDelay });
                                currentBleDelay += 300;
                                break;
                            case 'motor_stop':
                                bleQueue.push({ action: 'motor', speed: 0, delay: currentBleDelay });
                                currentBleDelay += 300;
                                break;
                            case 'sound_note':
                            case 'sound_animal':
                            case 'sound_play':
                                currentBleDelay += 5000;
                                break;
                            case 'event_color_sensor':
                                bleQueue.push({ action: 'wait_color', targetColor: paramVal, delay: currentBleDelay });
                                break;
                            case 'flow_wait':
                                currentBleDelay += (paramVal * 1000);
                                break;
                            case 'control_repeat':
                            case 'control_forever':
                                break;
                            case 'matrix_image':
                            case 'matrix_pixel':
                                let freshMatEl = block.querySelector('.param-unified') || block.querySelector('.block-param:not(.param-time)');
                                let matrixArrBLE = freshMatEl ? (freshMatEl.getAttribute('data-matrix') || JSON.stringify([0, 6, 0, 0, 0, 0, 6, 0, 6])) : JSON.stringify([0, 6, 0, 0, 0, 0, 6, 0, 6]);
                                let mBleTime = freshMatEl ? (parseFloat(freshMatEl.getAttribute('data-val')) || 2) : 2;

                                bleQueue.push({ action: 'matrix', colors: JSON.parse(matrixArrBLE), delay: currentBleDelay });
                                currentBleDelay += (mBleTime * 1000);
                                bleQueue.push({ action: 'matrix_clear', delay: currentBleDelay });
                                break;
                            case 'matrix_clear':
                                bleQueue.push({ action: 'matrix_clear', delay: currentBleDelay });
                                break;
                        }
                    });

                    if (currentBleDelay > maxGlobalDelay) {
                        maxGlobalDelay = currentBleDelay;
                    }

                    const executeBleQueue = async () => {
                        let lastExecutionTime = 0;
                        for (const cmd of bleQueue) {
                            if (window.bleEngineRunCounter !== currentRunId) return; // ?¥Ï†Ñ ?§Ìñâ Î£®ÌîÑ Ï∑®ÏÜå
                            try {
                                const waitTime = cmd.delay - lastExecutionTime;
                                
                                if (waitTime > 0 && cmd.action !== 'wait_color') {
                                    console.log(\`?±Ô∏è [BLE_ENGINE] Executing cmd: \${cmd.action} (waitTime: \${waitTime}ms)\`);
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
                                    console.log(\`?±Ô∏è [BLE_ENGINE] Waiting for Color Sensor to detect color ID: \${cmd.targetColor}\`);
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
                                        if (!matched) await new Promise(r => setTimeout(r, 100)); // ?¥ÎßÅ Ï£ºÍ∏∞ 100ms
                                    }
                                    if (!matched) return; // ?∏Î? Ï∑®ÏÜå
                                    console.log(\`??[BLE_ENGINE] Target Color \${cmd.targetColor} Detected! Continuing sequence...\`);
                                    
                                    // ?Ä?ÑÎùº???ôÍ∏∞??- ?¥Î≤§??Ï°∞Í±¥ ÎßåÏ°± ?ÑÎ????úÎ†à?¥Í? ?ÅÏö©?òÍ≤å ??
                                    lastExecutionTime = cmd.delay; 
                                }
                            } catch (e) {
                                console.error("??[BLE_ENGINE] Command Error:", e);
                            }
                        }
                    };

                    if (isEventLoop) {
                        (async () => {
                            // ?¥Î≤§???∏Îì§?? ??Î≤?Î¨¥Ï°∞Í±??êÎ? Ï∞®Î?Î°??§Ìñâ?òÍ≥†, ?ùÎÇú ???§Ïãú Í∞êÏãú??
                            while (window.bleEngineRunCounter === currentRunId) {
                                await executeBleQueue();
                                await new Promise(r => setTimeout(r, 500)); // Ï§ëÎ≥µ ??£º Î∞©Ï? Ïø®Îã§??
                            }
                        })();
                    } else {
                        executeBleQueue();
                    }
                });

                // Í≤åÏûÑ Î≥¥ÏÉÅ Î°úÏßÅ?Ä Î∏îÎ°ù ?§Ìñâ ?ÑÎ°ú ?†Ï?
                setTimeout(() => {
                    if (blockCount > 1 && anySequenceFound && window.bleEngineRunCounter === currentRunId) {
                        triggerSuccessConfetti();
                        try { window.parent.sendWebSocketAction({ action: "CAT_FEED_REWARD" }); } catch (e) { }
                    }
                }, maxGlobalDelay + 1000);

                return;
            }

`;

const newContent = content.substring(0, startIndex) + cleanBLELogic + content.substring(endIndex);
fs.writeFileSync(path, newContent, 'utf8');

try {
    const checkScript = newContent.match(/<script>([\s\S]*?)<\/script>/i)[1];
    acorn.parse(checkScript, { ecmaVersion: 2020 });
    console.log("Syntax is fully clean! Fix applied successfully.");
} catch (e) {
    console.error("Still error:", e);
}
