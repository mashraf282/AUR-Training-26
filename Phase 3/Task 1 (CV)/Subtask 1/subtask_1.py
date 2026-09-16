import cv2
import matplotlib.pyplot as plt

img = cv2.imread('noise_img.png')
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

avg_blur = cv2.blur(grey, (7, 7))
median_blur = cv2.medianBlur(grey, 5)
gaussian_blur = cv2.GaussianBlur(grey, (7, 7), 0)

otsu, _ = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


# gaussian best outcome (could be something else but that's what i got)
avg = cv2.Canny(avg_blur, otsu * 0.5, otsu * 0.6)
median = cv2.Canny(median_blur, otsu * 0.8, otsu * 1.5)
gaussian = cv2.Canny(gaussian_blur, otsu * 0.65, otsu * 1)

fig, ax = plt.subplots(2, 2, figsize=(10, 10))
ax[0, 0].imshow(grey, cmap='gray')
ax[0, 0].set_title('Original Image')
ax[0, 1].imshow(avg, cmap='gray')
ax[0, 1].set_title('Average Blur')
ax[1, 0].imshow(median, cmap='gray')
ax[1, 0].set_title('Median Blur')
ax[1, 1].imshow(gaussian, cmap='gray')
ax[1, 1].set_title('Gaussian Blur')

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()