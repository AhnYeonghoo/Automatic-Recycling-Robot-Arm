import cv2

def start_stream(camera_source=0):
    cap = cv2.VideoCapture(camera_source)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Camera Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Camera Stream')
    parser.add_argument('--source', type=int, default=0, help='Camera source: 0 for built-in, 1 for USB')
    args = parser.parse_args()

    start_stream(args.source)
