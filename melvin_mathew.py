from PIL import Image
import sys

import datetime


def read_image(file_name):
    f = Image.open(file_name)
    return f.load()


def write_image(file_name, pixels, resolution):
    img = Image.new('RGB', tuple(resolution))
    outp = img.load()

    for i in range(0, resolution[0]):
        for j in range(0, resolution[1]):
            outp[i, j] = pixels[i, j]

    img.show()
    img.save(file_name)


def random_down_sampling(pixels, resolution, new_resolution):
    img = Image.new('RGB', tuple(new_resolution))
    outp = img.load()

    x_scale = resolution[0] * 1.0 / new_resolution[0]
    y_scale = resolution[1] * 1.0 / new_resolution[1]

    prev_i_scale = prev_j_scale = 0
    for i in range(new_resolution[0]):
        if i == 0:
            i_scale = x_scale
        else:
            i_scale = i * x_scale
        for j in range(new_resolution[1]):
            if j == 0:
                j_scale = y_scale
            else:
                j_scale = j * y_scale
            outp[i, j] = pixels[int(i_scale), int(j_scale)]

    return outp


def average_pixels(pixels, i_min, i_max, j_min, j_max):
    r = 0
    g = 0
    b = 0
    n = (i_max - i_min) * (j_max - j_min)

    for i in range(i_min, i_max):
        for j in range(j_min, j_max):
            r += pixels[i, j][0]
            g += pixels[i, j][1]
            b += pixels[i, j][2]

    return (r / n, g / n, b / n)


def gaussian_down_sampling(pixels, resolution, new_resolution):
    img = Image.new('RGB', tuple(new_resolution))
    outp = img.load()

    x_scale = resolution[0] * 1.0 / new_resolution[0]
    y_scale = resolution[1] * 1.0 / new_resolution[1]

    prev_i_scale = prev_j_scale = 0
    for i in range(new_resolution[0]):
        if i == 0:
            i_scale = int(x_scale)
        else:
            i_scale += x_scale
        prev_j_scale = 0
        for j in range(new_resolution[1]):
            if j == 0:
                j_scale = y_scale
            else:
                j_scale += y_scale
            outp[i, j] = average_pixels(pixels, int(prev_i_scale), int(
                i_scale), int(prev_j_scale), int(j_scale))

            prev_j_scale = j_scale + 1

        prev_i_scale = i_scale + 1

    return outp


def nearest_neighbor_up_sampling(pixels, resolution, new_resolution):
    img = Image.new('RGB', tuple(new_resolution))
    outp = img.load()

    x_scale = new_resolution[0] * 1.0 / resolution[0]
    y_scale = new_resolution[1] * 1.0 / resolution[1]

    for i in range(new_resolution[0]):
        i_scale = int(i / x_scale)
        for j in range(new_resolution[1]):
            outp[i, j] = pixels[i_scale, int(j / y_scale)]

    return outp


def bilinear_up_sampling(pixels, resolution, new_resolution):
    img = Image.new('RGB', tuple(new_resolution))
    outp = img.load()

    x_scale = resolution[0] * 1.0 / new_resolution[0]
    y_scale = 1.0 * resolution[1] / new_resolution[1]

    for i in range(new_resolution[0]):
        i_scale = i * x_scale
        i_int = int(i_scale)
        i_delta = i_scale - i_int
        if i_int >= resolution[0] - 1:
            	i_int -= 1
        for j in range(new_resolution[1]):
            j_scale = j * y_scale
            j_int = int(j_scale)
            j_delta = j_scale - j_int
            if j_int >= resolution[1] - 1:
            	j_int -= 1
            a = [x * i_delta * (1 - j_delta) for x in pixels[i_int + 1, j_int]]
            b = [x * (1 - i_delta) * (1 - j_delta)
                 for x in pixels[i_int, j_int]]
            c = [x * (1 - i_delta) * j_delta for x in pixels[i_int, j_int + 1]]
            d = [x * i_delta * j_delta for x in pixels[i_int + 1, j_int + 1]]
            outp[i, j] = tuple([int(a[k] + b[k] + c[k] + d[k]) for k in range(3)])

    return outp


def main():
    # YourProgram.exe C:/myDir/myImage.rgb 4000 3000 1 O2

    now = datetime.datetime.now()
    upsample_functions = [nearest_neighbor_up_sampling, bilinear_up_sampling]
    downsample_functions = [random_down_sampling, gaussian_down_sampling]

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

    if process_format[0] < resolution[0]:
        modified_pixels = downsample_functions[
            process_type - 1](input_pixels, resolution, process_format)
    else:
        modified_pixels = upsample_functions[
            process_type - 1](input_pixels, resolution, process_format)

    write_image('result.bmp', modified_pixels, process_format)
    print "Image (name: 'result.bmp') saved"
    print datetime.datetime.now() - now
    # write_image('original1.bmp', input_pixels, resolution)

main()
