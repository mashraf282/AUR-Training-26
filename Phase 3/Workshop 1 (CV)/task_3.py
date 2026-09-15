import cv2

# anything not commented is the session code
# there's also a lot of yellow lines, I think pycharm is just being weird, but it doesn't affect the code

img = cv2.imread('task3.jpg')
h_img, w_img = img.shape[:2]
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# blurring for better results
blur = cv2.GaussianBlur(grey, (5, 5), 0)

# thresh otsu calculates the optimal threshold value automatically
_, thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
count = 0
for contour in contours:
    area = cv2.contourArea(contour)

    # filters out noise
    if area < 200:
        continue

    x, y, w, h = cv2.boundingRect(contour)

    # checks if the shape is too close to the image border
    margin = 10
    if x <= margin or y <= margin or (x + w) >= (w_img - margin) or (y + h) >= (h_img - margin):
        continue

    # checks actual shapes (solidity)
    # could've checked for big shapes, but that's not professional "?"
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    solidity = float(area) / hull_area if hull_area > 0 else 0

    if solidity < 0.85:
        continue

    # keeping count (which is correct)
    count += 1
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    vertices = len(approx)

    if vertices == 3:
        shape = "Triangle"
    elif vertices == 4:
        # checks for square by the aspect ratio (self-explanatory)
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        if 0.9 <= aspect_ratio <= 1.1:
            shape = "Square"
        else:
            shape = "Rectangle"
    else:
        shape = "Circle"

    m = cv2.moments(contour)
    cx = int(m["m10"] / m["m00"])
    cy = int(m["m01"] / m["m00"])

    cv2.drawContours(img, [contour], -1, (0, 255, 0), 3)
    cv2.putText(img, shape, (cx - 40, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

print(count)
cv2.imshow("Shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

