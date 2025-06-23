## 🧠 jetAI.py - AI 기반 자율주행 제어 스크립트

`jetAI.py`는 **Jetson Nano**와 **JetBotMini**를 기반으로, Jetson-Inference 모델을 활용해 객체를 감지하고, 감지된 객체에 따라 주행 동작을 수행하는 Python 스크립트입니다.

---

### 📂 주요 기능

- 경로 등록: Python 패키지 및 JetBotMini 모듈 경로 수동 등록
- JetBotMini 모터 제어: `jetbotmini.Robot` 객체로 좌우 모터를 제어
- 객체 감지: 학습된 SSD-MobileNet 모델을 불러와 실시간 객체 인식
- 주행 로직: 감지된 객체에 따라 전진, 후진, 회전, 정지 제어 수행
- 종료 처리: `Ctrl + C` 입력 시 안전하게 모터 정지

---

### 🚗 객체별 동작

| 감지된 객체 | 동작     | 설명                  |
|-------------|----------|-----------------------|
| `animal`    | 후진     | 장애물 감지 시 회피     |
| `green`     | 전진     | 안전 신호 시 전진      |
| `right`     | 우회전   | 방향 지시 신호 대응    |
| `left`      | 좌회전   | 방향 지시 신호 대응    |
| `stop`,`red`| 정지     | 빨간불, 정지신호 대응 |

---

### 🛠 사용된 모델

- 모델 경로: `models/mymodel/ssd-mobilenet.onnx`
- 라벨 파일: `models/mymodel/labels.txt`
- 입력: CSI 카메라 (`csi://0`)
- 임계값: 감지 confidence threshold 0.5 이상

---

### ▶️ 실행 방법

```bash
python3 jetAI.py


```


## 📁 데이터셋 구성

AI 학습을 위한 데이터셋은 다음과 같은 구조로 구성되어 있습니다:


### 📌 각 폴더 및 파일 설명

- **Annotations/**  
  객체의 위치(bounding box) 및 클래스 정보를 담고 있는 XML 형식의 어노테이션 파일들이 저장되어 있습니다.

- **ImageSets/Main/**  
  전체 이미지들 중 학습(train), 검증(val), 테스트(test)용으로 분할된 리스트 파일이 포함되어 있습니다.

- **JPEGImages/**  
  모델 학습 및 검증에 사용되는 원본 이미지(jpg 형식)들이 포함된 디렉토리입니다.

- **labels.txt**  
  학습 대상 객체의 클래스 이름이 나열된 텍스트 파일입니다. 모델이 감지할 수 있는 객체의 목록이 정의되어 있습니다.

