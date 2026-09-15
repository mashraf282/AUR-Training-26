from PIL import Image

image = Image.open("img.png")
bw_image = image.convert("L")
bw_image.show()
