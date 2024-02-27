import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import math
import numpy as np

# Read the image in greyscale
img = cv2.imread('Leonardo-Mona-Lisa.jpg', 0)

#Iterate over each pixel and change pixel value to binary using np.binary_repr() and store it in a list.
lst = []
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
         lst.append(np.binary_repr(img[i][j] ,width=8)) # width = no. of bits

# We have a list of strings where each string represents binary pixel value. To extract bit planes we need to iterate over the strings and store the characters corresponding to bit planes into lists.
# Multiply with 2^(n-1) and reshape to reconstruct the bit image.
eight_bit_img = (np.array([int(i[0]) for i in lst],dtype = np.uint8) * 128).reshape(img.shape[0],img.shape[1])
seven_bit_img = (np.array([int(i[1]) for i in lst],dtype = np.uint8) * 64).reshape(img.shape[0],img.shape[1])
six_bit_img = (np.array([int(i[2]) for i in lst],dtype = np.uint8) * 32).reshape(img.shape[0],img.shape[1])
five_bit_img = (np.array([int(i[3]) for i in lst],dtype = np.uint8) * 16).reshape(img.shape[0],img.shape[1])
four_bit_img = (np.array([int(i[4]) for i in lst],dtype = np.uint8) * 8).reshape(img.shape[0],img.shape[1])
three_bit_img = (np.array([int(i[5]) for i in lst],dtype = np.uint8) * 4).reshape(img.shape[0],img.shape[1])
two_bit_img = (np.array([int(i[6]) for i in lst],dtype = np.uint8) * 2).reshape(img.shape[0],img.shape[1])
one_bit_img = (np.array([int(i[7]) for i in lst],dtype = np.uint8) * 1).reshape(img.shape[0],img.shape[1])


# Define your custom colormap with two colors
# custom_cmap = ListedColormap(['green', 'yellow','blue','red'])  
custom_cmap = ListedColormap({(0,1,0,0.8),(1,1,0,1),(0,0,1,0.5),(1,0,0,0.6)})
# Change 'blue' and 'red' to your desired colorslay the one-bit image with the custom colormap

# print("Max value in one-bit image:", np.max(one_bit_img))
# print("Min value in one-bit image:", np.min(one_bit_img))

plt.imshow(eight_bit_img, cmap=custom_cmap)
plt.colorbar()
plt.show()

# plt.imshow(eight_bit_img, cmap='binary')
# plt.colorbar()
# plt.show()

# plt.imshow(two_bit_img) 
# plt.show()

# plt.imshow(three_bit_img) 
# plt.show()

# plt.imshow(four_bit_img) 
# plt.show()

# plt.imshow(five_bit_img) 
# plt.show()

# plt.imshow(six_bit_img) 
# plt.show()

# plt.imshow(seven_bit_img) 
# plt.show()

# plt.imshow(eight_bit_img) 
# plt.show()

# # Combining 4 bit planes
# new_img = eight_bit_img+seven_bit_img+six_bit_img+five_bit_img
# # Display the images
# plt.imshow(new_img) 
# plt.show()
