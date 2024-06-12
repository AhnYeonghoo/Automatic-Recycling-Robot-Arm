import torch
import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators import gzip
from django.http import HttpResponse

# YOLO 모델 로드
model_path = r'C:\Users\leesa\OneDrive\바탕 화면\samplemodel.pt'
model = torch.hub.load('WongKinYiu/yolov7', 'custom', model_path)

# 객체 감지 함수
def detect_objects(frame):
    results = model(frame)
    return results

# 웹캠 스트리밍 제네레이터
def gen(camera):
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        results = detect_objects(frame)
        # 결과 프레임에 감지된 객체를 그리기
        for (xmin, ymin, xmax, ymax, label, confidence) in results.xyxy[0]:
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax, int(ymax))), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {confidence:.2f}', (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# 웹캠 스트리밍 뷰
@gzip.gzip_page
def webcam_view(request):
    try:
        return StreamingHttpResponse(gen(cv2.VideoCapture(0)), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        return HttpResponse(f"<h1>{str(e)}</h1>")

# 핸드폰 스트리밍 뷰
@gzip.gzip_page
def phone_view(request):
    try:
        # 비디오 캡처 장치 번호를 핸드폰 화면 스트리밍 소스로 변경
        return StreamingHttpResponse(gen(cv2.VideoCapture(1)), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        return HttpResponse(f"<h1>{str(e)}</h1>")

# 선택 페이지 뷰
def index(request):
    return render(request, 'camera/index.html')
