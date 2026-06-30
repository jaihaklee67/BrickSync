import sys

path = r"C:\Users\PC\Documents\GitHub\BrickSync\BrickSync-main\bricksync_project\web_app\lesson.html"

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update briefing mData for Stage 1
target_1 = "'1': { badge: 'STAGE 1', title: '첫 번째 연동', desc: '조명 블록을 꺼내어 조립해서 허브에 불을 켜보세요!', tasks: [{text: '재생(시작) 블록 연결하기'}, {text: '조명 블록(3x3) 연결하기'}] },"
replacement_1 = "'1': { badge: 'STAGE 1', title: '첫 번째 연동', desc: '5초 대기 후 앞으로 3번 이동하고, 좌회전 1번 후 뒤로 2번 이동하세요.', tasks: [{text: '재생(시작) 블록 연결하기'}, {text: '5초 대기하기'}, {text: '앞으로 3번 이동하기'}, {text: '좌회전 1번 작동하기'}, {text: '뒤로 2번 이동하기'}] },"

if target_1 in content:
    content = content.replace(target_1, replacement_1)
    print("1. mData stage 1 briefing patched.")
else:
    print("1. mData stage 1 briefing target not found!")

# 2. Update missionData stage 1
target_2 = """            '1': {
                badge: 'STAGE 1', title: '첫 번째 연동', desc: '5초 대기 후 앞으로 3초 이동하고, 좌회전 1초 후 뒤로 2초 이동하세요.',
                pinCode: '7241',
                tasks: [
                    { id: 'start', text: '재생(시작) 블록 연결하기' },
                    { id: 'flow_wait_5', text: '5초 대기하기' },
                    { id: 'car_forward_3', text: '앞으로 3초 이동하기' },
                    { id: 'car_left_1', text: '좌회전 1초 작동하기' },
                    { id: 'car_backward_2', text: '뒤로 2초 이동하기' }
                ]
            },"""

replacement_2 = """            '1': {
                badge: 'STAGE 1', title: '첫 번째 연동', desc: '5초 대기 후 앞으로 3번 이동하고, 좌회전 1번 후 뒤로 2번 이동하세요.',
                pinCode: '7241',
                tasks: [
                    { id: 'start', text: '재생(시작) 블록 연결하기' },
                    { id: 'flow_wait_5', text: '5초 대기하기' },
                    { id: 'car_forward_3', text: '앞으로 3번 이동하기' },
                    { id: 'car_left_1', text: '좌회전 1번 작동하기' },
                    { id: 'car_backward_2', text: '뒤로 2번 이동하기' }
                ]
            },"""

if target_2 in content:
    content = content.replace(target_2, replacement_2)
    print("2. missionData stage 1 patched.")
else:
    print("2. missionData stage 1 target not found!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch complete.")
