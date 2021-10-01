from PIL import ImageChops
import math, operator
from PIL import Image

from time import sleep




im1=Image.open('/home/pi/Desktop/images/image0.jpg')
im2=Image.open('/home/pi/Desktop/images/image1.jpg')
diff = ImageChops.difference(im1, im2)
h = diff.histogram()
sq = (value*(idx**2)for idx, value in enumerate(h))
sum_of = sum(sq)
rms= math.sqrt(sum_of/float(im1.size[0]*im1.size[1]))
print(rms)
