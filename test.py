from PIL import Image, ImageDraw

# define the points of the triangle
points = [(50, 0), (0, 100), (100, 100)]

# create a new image
img = Image.new('RGBA', (100, 100), color=(255, 255, 255, 0))

# create a draw object
draw = ImageDraw.Draw(img)

# draw the triangle on the image
draw.polygon(points, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))

# # show the image
# img.show()