from PIL import Image
import cPickle
import numpy as np
import matplotlib.pyplot as plt

with open('./data/pictures.pickle','rb') as file:
    list = cPickle.load(file)

a = list[0]

print a.shape
# plt.subplot(121)

# plt.imshow(a, cmap = 'gray')

im = Image.fromarray(np.float32(a))
b = np.array(im.resize((50,50)))
print b

print b.shape

# plt.subplot(122)
plt.imshow(b, cmap = 'gray')

plt.show()