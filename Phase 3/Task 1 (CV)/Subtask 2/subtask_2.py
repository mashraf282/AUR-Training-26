import numpy as np
import cv2

def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened() is False:
        print("Error opening video stream or file")
        return None
    return cap


def detect_shapes(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    sat = hsv[:, :, 1]

    blur = cv2.medianBlur(sat, 5)

    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)

    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 200:
            continue


        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        vertices = len(approx)

        x, y, w, h = cv2.boundingRect(contour)
        box_area = w * h
        extent = float(area) / box_area if box_area > 0 else 0

        circularity = (4 * np.pi * area) / (peri ** 2)

        if circularity >= 0.82 or extent < 0.83:
            shape = "Circle"
        elif extent >= 0.85 and vertices == 4:
            shape = "Square"
        else:
            shape = "Square" if extent >= 0.85 else "Circle"

        m = cv2.moments(contour)
        if m["m00"] == 0:
            continue

        cx = int(m["m10"] / m["m00"])
        cy = int(m["m01"] / m["m00"])

        if not detect_color(frame, shape, cx, cy):
            continue

        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        cv2.putText(frame, shape, (cx - 30, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

def detect_color(frame, shape, cx, cy):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h, s, v = hsv[cy, cx]

    if s < 100 or v < 100:
        return False

    is_red = (0 <= h <= 5) or (170 <= h <= 180)

    is_blue = (100 <= h <= 140)

    if is_red and shape == "Circle":
        return True
    elif is_blue and shape == "Square":
        return True
    return False

def main():
    video_path = 'thrown_shapes_noisy_30s.mp4'
    cap = read_video(video_path)

    if cap is None:
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result = detect_shapes(frame)

        cv2.imshow('Frame', result)

        if cv2.waitKey(30) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__  == "__main__":
    main()