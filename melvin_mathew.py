from PIL import Image
import sys


def read_image(file_name):
	f = Image.open(file_name)
	return f.load()

def write_image(file_name, pixels, resolution):
	img = Image.new('RGB', tuple(resolution))
	outp = img.load()

	for i in range(0, resolution[0]):
		for j in range(0, resolution[1]):
			outp[i,j] = pixels[i,j]

	img.show()


def main():
	#YourProgram.exe C:/myDir/myImage.rgb 4000 3000 1 O2

	image_file_name = sys.argv[1]
	resolution = [int(sys.argv[2]), int(sys.argv[3])]
	process_type = int(sys.argv[4])
	"""
	In the down sample case, use
		1. Specific/Random sampling where you choose a specific pixel
		2. Gaussian smoothing where you choose the average of a set of samples

	In the up sample case, use
		1. Nearest neighbor to choose your up sampled pixel
		2. Bilinear/Cubic interpolation
	"""
	standard_format = {
		'O1': [1920, 1080],
		'O2': [1280, 720],
		'O3': [640, 480]
	}
	process_format = standard_format[sys.argv[5]]

	# Read file
	input_pixels = read_image(image_file_name)

	write_image('asd.bmp', input_pixels, process_format)

main()