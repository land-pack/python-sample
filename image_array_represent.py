from PIL import Image
from numpy import array

pil_im = Image.open('ada.png')

im = array(pil_im)

im_gray = array(pil_im.convert('L'),'f')

if __name__ == '__main__':
	print im.shape,im.dtype
	print im[299,75]
	
	print im_gray.shape,im_gray.dtype
	print im_gray[299,75]
	
