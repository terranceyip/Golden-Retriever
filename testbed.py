import os

image = open("item.png",'rb')
newImage = open ("oldItem.png", 'wb')
newImage.write(image.read())
newImage.close()
image.close()
os.remove("item.png")