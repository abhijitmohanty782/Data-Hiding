import os, sys
from PIL import Image
from utils import rgb_to_binary

def extract_hidden_pixels(image, width_carrier, height_carrier, pixel_count):
	"""
	Extracts a sequence of bits representing a sequence of binary values of 
	all pixels of the hidden image.
	The information representing a hidden image is stored in the 4 least significant
	bits of a subset of pixels of the visible image.

	Args:
	    image:            An RGB image to recover a hidden image from
	    width_carrier:    Width of the visible image
	    height_carrier:   Height of the visible image
	    pixel_count:      Number of pixels in the hidden image

	Returns:
	    A binary string representing pixel values of the hidden image
	"""
	secret_image_pixels = ''
	idx = 0
	for col in range(width_carrier):
		for row in range(height_carrier):
			if row == 0 and col == 0:
				continue
			r, g, b = image[col, row]
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			secret_image_pixels += r_binary[4:8] + g_binary[4:8] + b_binary[4:8]
			if idx >= pixel_count * 2:
				return secret_image_pixels
	return secret_image_pixels

def reconstruct_image(image_pixels, width, height):
	
	image = Image.new("RGB", (width, height))
	image_copy = image.load()
	idx = 0
	for col in range(width):
		for row in range(height):
			r_binary = image_pixels[idx:idx+8]
			g_binary = image_pixels[idx+8:idx+16]
			b_binary = image_pixels[idx+16:idx+24]
			image_copy[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
			idx += 24
	return image
	
def decode(image):
	"""
	Loads the image to recover a hidden image from, retrieves the information about the
	size of the hidden image stored in the top left pixel of the visible image,
	extracts the hidden binary pixel values from the image and reconstructs the hidden
	image.

	Args:
	    image:    An RGB image to recover a hidden image from

	Returns:
	    A recovered image, which was hidden in the binary representation of the visible image
	"""
	image_copy = image.load()
	width_carrier, height_carrier = image.size
	r, g, b = image_copy[0, 0]
	r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
	w_h_binary = r_binary + g_binary + b_binary
	width_hidden = int(w_h_binary[0:12], 2)
	height_hidden = int(w_h_binary[12:24], 2)
	pixel_count = width_hidden * height_hidden
	secret_image_pixels = extract_hidden_pixels(image_copy, width_carrier, height_carrier, pixel_count)
	decoded_image = reconstruct_image(secret_image_pixels, width_hidden, height_hidden)
	return decoded_image

def main():
	"""
	Opens an image which contains information of a hidden image,
	recovers the hidden image and saves it in a specified or
	default location.

	Call example:
	    python decode.py img/output.png img/res.png
	"""
	if len(sys.argv) <= 2 or len(sys.argv) > 3:
		print("-------------------------------------------------")
		print("## PLEASE ENTER 3 COMMAND LINE ARGUMENTS ##")
		print ("--")
		print("In the below given format")
		print("-------------------------------------------------")
		print ("--   python decode.py img/output.png img/res.png")
		print("-------------------------------------------------")
		return
	if len(sys.argv) == 3:
		img_path = sys.argv[1]
		output_path = sys.argv[2]
		filename, file_ext = os.path.splitext(output_path)
		output_path = filename + '.png'
	else:
		output_path = 'images/decoded_image.png'
  
	decoded_image = decode(Image.open(img_path))
	decoded_image.save(output_path)

if __name__ == '__main__':
	main()