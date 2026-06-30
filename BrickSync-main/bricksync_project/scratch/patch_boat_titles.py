import sys

# 1. Patch settings.js
settings_path = r"C:\Users\PC\Documents\GitHub\BrickSync\BrickSync-main\bricksync_project\web_app\settings.js"
with open(settings_path, 'r', encoding='utf-8') as f:
    settings_content = f.read()

target_s1 = 'lesson_1: "1. 요리조리 기울여서 탐험보트를 출발시켜요",'
replacement_s1 = 'lesson_1: "1. 탐험보트를 출발시켜요",'
target_s2 = 'lesson_1: "1. Tilt left and right to launch the exploration boat",'
replacement_s2 = 'lesson_1: "1. Launch the exploration boat",'

if target_s1 in settings_content:
    settings_content = settings_content.replace(target_s1, replacement_s1)
    print("settings.js ko title patched.")
if target_s2 in settings_content:
    settings_content = settings_content.replace(target_s2, replacement_s2)
    print("settings.js en title patched.")

with open(settings_path, 'w', encoding='utf-8') as f:
    f.write(settings_content)


# 2. Patch lesson.html
lesson_path = r"C:\Users\PC\Documents\GitHub\BrickSync\BrickSync-main\bricksync_project\web_app\lesson.html"
with open(lesson_path, 'r', encoding='utf-8') as f:
    lesson_content = f.read()

# Update themeDescriptions
target_l1 = "'1': '레고 허브의 조명을 켜고 다채로운 색상을 조립해 보며 기초 동작을 익혀봅시다.',"
replacement_l1 = "'1': '5초 대기 후 앞으로 3번 이동하고, 좌회전 1번 후 뒤로 2번 이동해 보트를 출발시켜 봅시다.',"

target_l2 = "'1': 'Learn basic Lego Hub light and color matrix control operations.',"
replacement_l2 = "'1': 'Wait 5 seconds, move forward 3 times, turn left 1 time, and move backward 2 times to launch the boat.',"

# Update projectNames
target_l3 = "'1': '학습 1: 요리조리 기울여서 탐험보트를 출발시켜요',"
replacement_l3 = "'1': '학습 1: 탐험보트를 출발시켜요',"

# Update mData title
target_l4 = "title: '첫 번째 연동', desc: '5초 대기 후 앞으로 3번 이동하고, 좌회전 1번 후 뒤로 2번 이동하세요.',"
replacement_l4 = "title: '탐험보트를 출발시켜요', desc: '5초 대기 후 앞으로 3번 이동하고, 좌회전 1번 후 뒤로 2번 이동하세요.',"

# Update missionData title
target_l5 = "badge: 'STAGE 1', title: '첫 번째 연동', desc: '5초 대기 후 앞으로 3번 이동하고, 좌회전 1번 후 뒤로 2번 이동하세요.',"
replacement_l5 = "badge: 'STAGE 1', title: '탐험보트를 출발시켜요', desc: '5초 대기 후 앞으로 3번 이동하고, 좌회전 1번 후 뒤로 2번 이동하세요.',"

if target_l1 in lesson_content:
    lesson_content = lesson_content.replace(target_l1, replacement_l1)
    print("lesson.html themeDescriptions ko patched.")
if target_l2 in lesson_content:
    lesson_content = lesson_content.replace(target_l2, replacement_l2)
    print("lesson.html themeDescriptions en patched.")
if target_l3 in lesson_content:
    lesson_content = lesson_content.replace(target_l3, replacement_l3)
    print("lesson.html projectNames patched.")
if target_l4 in lesson_content:
    lesson_content = lesson_content.replace(target_l4, replacement_l4)
    print("lesson.html mData title patched.")
if target_l5 in lesson_content:
    lesson_content = lesson_content.replace(target_l5, replacement_l5)
    print("lesson.html missionData title patched.")

with open(lesson_path, 'w', encoding='utf-8') as f:
    f.write(lesson_content)


# 3. Patch mission.html
mission_path = r"C:\Users\PC\Documents\GitHub\BrickSync\BrickSync-main\bricksync_project\web_app\mission.html"
with open(mission_path, 'r', encoding='utf-8') as f:
    mission_content = f.read()

target_m1 = """                '1': {
                    title: '학습 1: 요리조리 기울여서 탐험보트를 출발시켜요',
                    badge: 'STAGE 1',
                    desc: '가장 기본적인 블록들을 조립하여 현실 세계의 레고 허브 조명을 켜봅시다.',
                    goals: ['블루투스로 혹은 USB로 스파이크 허브 연결하기', '조명 블록을 사용하여 원하는 모양 그리기', '포트나이트 게임에 신호 보내기']
                },"""

replacement_m1 = """                '1': {
                    title: '학습 1: 탐험보트를 출발시켜요',
                    badge: 'STAGE 1',
                    desc: '5초 대기 후 앞으로 3번 이동하고, 좌회전 1번 후 뒤로 2번 이동해 보트를 출발시킵니다.',
                    goals: ['블루투스 혹은 USB로 스파이크 허브 연결하기', '대기 블록과 이동 블록 연결하기', '포트나이트 게임에 신호 보내기']
                },"""

target_m2 = """                '1': {
                    title: 'Lesson 1: Tilt left and right to launch the exploration boat',
                    badge: 'STAGE 1',
                    desc: 'Assemble the most basic blocks to light up the real-world LEGO Hub.',
                    goals: ['Connect Spike Hub via Bluetooth or USB', 'Draw desired shapes using light blocks', 'Send signals to Fortnite game']
                },"""

replacement_m2 = """                '1': {
                    title: 'Lesson 1: Launch the exploration boat',
                    badge: 'STAGE 1',
                    desc: 'Wait 5 seconds, move forward 3 times, turn left 1 time, and move backward 2 times to launch the boat.',
                    goals: ['Connect Spike Hub via Bluetooth or USB', 'Connect wait and movement blocks', 'Send signals to Fortnite game']
                },"""

if target_m1 in mission_content:
    mission_content = mission_content.replace(target_m1, replacement_m1)
    print("mission.html ko briefing patched.")
else:
    print("mission.html ko briefing target not found!")

if target_m2 in mission_content:
    mission_content = mission_content.replace(target_m2, replacement_m2)
    print("mission.html en briefing patched.")
else:
    print("mission.html en briefing target not found!")

with open(mission_path, 'w', encoding='utf-8') as f:
    f.write(mission_content)

print("All patches completed.")
