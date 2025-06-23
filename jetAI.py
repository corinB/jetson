import sys, time

# ──────────────────── 경로 등록 ────────────────────
sys.path.extend([
    '/usr/local/lib/python3.6/dist-packages',
    '/usr/lib/python3/dist-packages',
    '/usr/lib/python3.6/dist-packages',
    '/usr/local/lib/python3.6/dist-packages/jetbotmini-0.4.0-py3.6.egg'
])

# ──────────────────── JetBotMini 모터 제어 ────────────────────
from jetbotmini import Robot
robot = Robot()

# ──────────────────── Jetson-Inference 객체 감지 ──────────────
import jetson.inference, jetson.utils

net = jetson.inference.detectNet(
    argv=[
        "--model=models/mymodel/ssd-mobilenet.onnx",
        "--labels=models/mymodel/labels.txt",
        "--input-blob=input_0",
        "--output-cvg=scores",
        "--output-bbox=boxes",
        "--threshold=0.5"
    ]
)
camera = jetson.utils.videoSource("csi://0")

print("▶ 감지·주행 루프 시작 (Ctrl-C 로 종료)")

FORWARD  =  0.5   # 전진 속도
BACKWARD = -0.5   # 후진 속도
MIDEWARD = 0.3

try:
    while True:
        img = camera.Capture()
        if img is None:
            continue

        detections = net.Detect(img)
        classes = {net.GetClassDesc(d.ClassID) for d in detections}

        # 감지된 객체 출력
        print("감지:", ", ".join(classes) if classes else "없음")

        if 'animal' in classes:           # animal → 후진
            robot.left_motor.value  = BACKWARD
            robot.right_motor.value = BACKWARD
            print("ANIMAL 감지 → 후진")
        elif 'green' in classes:          # green  → 전진
            robot.left_motor.value  = FORWARD
            robot.right_motor.value = FORWARD
            print("GREEN 감지 → 전진")
        elif 'right' in classes:        # right  → 우회전
            robot.left_motor.value  = FORWARD
            robot.right_motor.value = MIDEWARD
            print("right 감지 → 우회전")    
        elif 'left' in classes:  # left  → 좌회전
            robot.left_motor.value  = MIDEWARD
            robot.right_motor.value = FORWARD
            print("left 감지 → 좌회전")
        else:                             # 그 외 → 정지
            robot.left_motor.value  = 0.0
            robot.right_motor.value = 0.0
            print("조건 없음 → 정지")

        time.sleep(0.1)  # 100 ms 간격

except KeyboardInterrupt:
    pass
finally:
    robot.left_motor.value = 0.0
    robot.right_motor.value = 0.0
    print("\n▶ 종료, 모터 정지 완료")

