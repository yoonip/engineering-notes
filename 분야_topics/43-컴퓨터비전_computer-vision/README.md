# 컴퓨터 비전과 영상 처리 | Computer Vision & Image Processing

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

컴퓨터 비전은 영상에서 물체·공간·움직임 등의 정보를 추정하는 분야다. 영상은 카메라의 광학계·센서·노출·좌표계·색 표현을 거쳐 만들어지므로 입력 형식 자체가 모델의 동작에 영향을 준다.

## 영상 처리와 기하

필터는 잡음 제거·경계 강조·주파수 선택 등에 쓰인다. Camera calibration은 영상 좌표와 공간의 투영 관계를 추정하고 왜곡을 다룬다. 특징점과 대응점은 영상 간 정합과 3차원 복원의 단서다. OpenCV·Kornia는 영상 처리와 기하 연산을 지원한다.

## 인식 과제와 구조

Classification은 영상의 범주, detection은 물체 위치와 범주, segmentation은 pixel 단위 구분, tracking은 시간에 따른 동일 객체의 연결을 다룬다. Pose·depth estimation은 자세와 거리를 추정한다. ResNet·EfficientNet·ViT는 표현 학습 구조, YOLO·DETR은 검출, SAM 계열은 분할, DINO 계열은 자기지도 표현 학습 등에 쓰인다.

torchvision·timm·Detectron2·MMDetection은 모델과 학습·평가 구성을 제공한다. 정확도 외에 해상도·latency·메모리·작은 객체 성능이 응용에서 중요하다. 같은 연속 영상의 인접 frame이 학습·시험 데이터에 나뉘어 들어가면 성능이 실제보다 높게 나올 수 있다.

## 관련 기술

OpenCV, torchvision, timm, ResNet, ViT, YOLO, SAM, DINO, Detectron2, MMDetection, Kornia

## 참고 자료

- [OpenCV tutorials](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html)

## 기초 해설

- [카메라 모델, 영상 필터, CV 검증](해설_notes/카메라모델영상필터CV검증_camera-filtering-and-validation.md)

## English

### Computer vision

Computer vision estimates information about objects, space, and motion from images. An image reflects the camera's optics, sensor, exposure, coordinate system, and color representation, so the input format itself affects model behavior.

### Image processing and geometry

Filters remove noise, emphasize edges, or select frequency components. Camera calibration estimates the projection between image coordinates and space and accounts for distortion. Features and correspondences support image registration and 3D reconstruction. OpenCV and Kornia provide tools for image processing and geometric operations.

### Recognition tasks and architectures

Classification assigns an image category. Detection locates and classifies objects, segmentation labels pixels, and tracking associates the same object across time. Pose and depth estimation recover configuration and distance. ResNet, EfficientNet, and ViT are representation-learning architectures. YOLO and DETR support detection, SAM models support segmentation, and DINO models include self-supervised representation learning.

torchvision, timm, Detectron2, and MMDetection provide models and training or evaluation components. Resolution, latency, memory, and small-object performance matter alongside accuracy. Mixing adjacent frames of the same sequence into training and test sets can produce overly optimistic evaluation results.

### Foundation article

- [카메라 모델, 영상 필터, CV 검증](해설_notes/카메라모델영상필터CV검증_camera-filtering-and-validation.md#english)
