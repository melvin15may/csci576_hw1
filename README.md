This assignment will help you gain a practical understanding of Resampling and Filtering and how it affects visual media types like images and videos.
Firstly, you will have to write a program to display images in the RGB format. We have also provided a Microsoft Visual C++ project and java to display images. This source has been provided as a reference for students who may not know how to read and display images. You are free to use this as a start, or write your own in any language of your choice (no matlab please!), as long as your program can be easily evaluated on our UCS computer systems.
You will take an image an input in a 4:3 aspect ratio, which will be a high resolution image (4000x3000) or a low resolution image (400x300). Your program will generate an output image which will be one of the following standard formats
* O1: 1920x1080
* O2: 1280x720
* O3: 640x480

In each case, depending on your input size, you will need to either down sample or up sample the image. In each case implement these two methods to choose your sample value.
* In the down sample case, use
  * Specific/Random sampling where you choose a specific pixel
  * Gaussian smoothing where you choose the average of a set of samples
* In the up sample case, use
  * Nearest neighbor to choose your up sampled pixel
  * Bilinear/Cubic interpolation

Correspondingly you will have five input parameters to your program
* FileName (string) – gives you the location of the file containing the image.
* Width (int) – width of the image in pixels.
* Height (int) – height of the image in pixels.
* Resampling method (int) – has values of 1 or 2. You will have to determine whether the image is being up sampled or down sampled and decide accordingly.
* Output format (string) – can have values O1, O2 or O3 for the three formats discussed above.

To invoke your program we will compile it and run it at the command line as
```YourProgram.exe C:/myDir/myImage.rgb 4000 3000 1 O2```
The expectation here is that your program will read the image of size 4000x3000 and down sample it to 1280x720 and use specific/random sampling to decide each pixel value in the output.
