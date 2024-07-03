import os, sys
from PIL import Image
from utils import rgb_to_binary, add_leading_zeros

def get_binary_pixel(img, width, height):
	"""
	Retrieves a string of concatenated binary representations of RGB channel values of all pixels in an image.

	Args:
	    img:    An RGB image
	    width:  Width of the image
	    height: Height of the image

	Returns:
	    A string with concatenated binary numbers representing the RGB channel values of all pixels in the image
	    where each binary number representing one channel value is 8 bits long, padded with leading zeros 
	    when necessary. Therefore, each pixel in the image is represented by 24 bit long binary sequence.
	"""
	secret_image_pixels = ''
	for col in range(width): 
		for row in range(height): 
			pixel = img[col, row]
			r = pixel[0] # providing pixel val at 0th index to r'
			g = pixel[1] # providing pixel val at 1st index to g
			b = pixel[2] # providing pixel val at 2nd index to b
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			secret_image_pixels += r_binary + g_binary + b_binary # concatenating the binary values of r,g,b together in a single string
	return secret_image_pixels

def change_binary_values(img_carrier, secret_image_pixels, width_carrier, height_carrier, width_secret, height_secret):
	"""
	Replaces the 4 least significant bits of a subset of pixels in an image with bits representing a sequence of binary
	values of RGB channels of all pixels of the image to be concealed.

	The first pixel in the top left corner is used to store the width and height of the image to be hidden, which is
	necessary for recovery of the hidden image.

	Args:
	    img_carrier:          An RGB image to be used for hiding another image
	    secret_image_pixels:  Binary string representing all pixel values of the image to be hidden
	    width_carrier:        Width of the image to be used for hiding another image
	    height_carrier:       Height of the image to be used for hiding another image
	    width_secret:         Width of the image to be hidden
	    height_secret:        Height of the image to be hidden

	Returns:
	    An RGB image which is a copy of img_carrier where the 4 least significant bits of a subset of pixels
	    are replaced with bits representing the hidden image.
	"""
	idx = 0
	for col in range(width_carrier):
		for row in range(height_carrier):
			if row == 0 and col == 0:
				width_secret_binary = add_leading_zeros(bin(width_secret)[2:], 12)
				height_secret_binary = add_leading_zeros(bin(height_secret)[2:], 12)
				w_h_binary = width_secret_binary + height_secret_binary
				img_carrier[col, row] = (int(w_h_binary[0:8], 2), int(w_h_binary[8:16], 2), int(w_h_binary[16:24], 2))
				continue
			r, g, b = img_carrier[col, row]
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			r_binary = r_binary[0:4] + secret_image_pixels[idx:idx+4]
			g_binary = g_binary[0:4] + secret_image_pixels[idx+4:idx+8]
			b_binary = b_binary[0:4] + secret_image_pixels[idx+8:idx+12]
			idx += 12
			img_carrier[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
			if idx >= len(secret_image_pixels):
				return img_carrier
	# can never be reached, but let's return the image anyway
	return img_carrier

def encode(img_carrier, img_secret):
	"""
	Loads the image to be hidden and the image used for hiding and conceals the pixel information from one image
	in the other one.

	Args:
	    img_carrier:    An RGB image used for hiding another image
	    img_secret:     An RGB image to be concealed

	Returns:
	    An RGB image which is supposed to be not very different visually from img_carrier, but contains all the information
	    necessary to recover an identical copy of the image we want to hide.
	"""
	encoded_image = img_carrier.load()
	img_secret_copy = img_secret.load()
	width_carrier, height_carrier = img_carrier.size
	width_secret, height_secret = img_secret.size
	secret_image_pixels = get_binary_pixel(img_secret_copy, width_secret, height_secret)
	encoded_image = change_binary_values(encoded_image, secret_image_pixels, width_carrier, height_carrier, width_secret, height_secret)
	return img_carrier

def main():
	"""
	The number of pixels in the image used for hiding an image must be at least (2 * number of pixels in the image to be hidden + 1)
	
    Call example:
        python encode.py img/vis.jpg img/hid.jpg img/output.png
	"""
	if len(sys.argv) <= 3 or len(sys.argv) > 4:
		print("-------------------------------------------------")
		print("## PLEASE ENTER 4 COMMAND LINE ARGUMENTS ##")
		print ("--")
		print("In the below given format")
		print("-------------------------------------------------")
		print ("--   python encode.py img/vis.jpg img/hid.jpg img/output.png")
		print("-------------------------------------------------")
		
		return
	if len(sys.argv) == 4:
		img_carrier_path = sys.argv[1] #store the path of the image in which we want to hide secret image
		img_secret_path = sys.argv[2] #store the path of the secret image
		output_path = sys.argv[3] #store the pathof output
  
  		#This function splits the given output_path into the filename and its extension. It returns a tuple where the #first element is the filename and the second element is the file extension.
		filename, file_ext = os.path.splitext(output_path) 
		# Updateing output_path variable by appending the .png extension to the filename. 
		output_path = filename + '.png'
  
	else:
		output_path = 'images/encoded_image.png'
  
	img_carrier = Image.open(img_carrier_path) #to open the image in which we want to hide secret image
	img_secret = Image.open(img_secret_path) #to open the secret image
	encoded_image = encode(img_carrier, img_secret) #encoded image
	encoded_image.save(output_path) #saving the encoded image in output path specified above

if __name__ == '__main__':
	main()