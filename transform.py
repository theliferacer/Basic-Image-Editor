import cv2
import math
import numpy as np
from PIL import Image

#Resizing an image
def Resize(image):
	np_img = np.array(image)
	#Resizing the image by maintaining the aspect ratio r
	r = 600/np_img.shape[0]
	M = int(np_img.shape[1]*r)
	if M >= 1200:
		M = 1200
	else:
		M = M
	dim = (M,600)
	stretch_near = cv2.resize(np_img, dim,interpolation = cv2.INTER_AREA)
	pil_img = Image.fromarray(stretch_near)
	
	return pil_img

#Gamma Transformation, with gamma value: 'g' 
def Gamma(img,g):
	img_array = np.array(img)#Converting from Image to N-D array
	length = len(img_array.shape)#To check if the image is grayscale or RGB
	c = 255/(255**g)
	if length == 2:
		typ = "gray"
		img_hsv = img.copy()
		img_hsv_array = np.array(img_hsv)

		for i in range(0,img_hsv_array.shape[0]):
			for j in range(0,img_hsv_array.shape[1]):
				p_ij = img_hsv_array[i,j] #Intensity value of the pixel (i,j)
				s_ij = c*(p_ij**g) #gamma transform s = c*(r^g)
				img_hsv_array[i,j] = s_ij 
		final_image_array = img_hsv_array

	else:
		typ = "RGB"
		img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)#convering RGB image to HSV format
		img_hsv_array = np.array(img_hsv)
		for i in range(0,img_hsv_array.shape[0]):
			for j in range(0,img_hsv_array.shape[1]):
				p_ij = img_hsv_array[i,j,2] #V value of the pixel (i,j)
				s_ij = c*(p_ij**g) #gamma transform s = c*(r^g)
				img_hsv_array[i,j,2] = s_ij
		final_image_array = cv2.cvtColor(img_hsv_array,cv2.COLOR_HSV2RGB)#Converting hsv image back to RGB

	pil_img = Image.fromarray(final_image_array) #Converting cv2 image to PIL image to display in the gui

	return pil_img

#Histogram Equalization
def Histogram(img):
	img_array = np.array(img)
	length = len(img_array.shape)
	if length == 2:
		typ = "gray"
		img_hsv = img.copy()
		img_hsv_array = np.array(img_hsv)
		r_k, n_k = np.unique(img_hsv_array, return_counts = True)
	else:
		typ = "RGB"
		img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
		img_hsv_array = np.array(img_hsv)
		r_k, n_k = np.unique(img_hsv_array[:,:,2], return_counts = True) #gives no.of pixels n_k in the intensity level r_k

	M = img_hsv_array.shape[0]
	N = img_hsv_array.shape[1] #MxN number of pixels
	p_r = n_k/(M*N) #probability of an occurrence of a pixel of level r_k
	cump_r = np.cumsum(p_r) #Cumulative sum
	s_k = 255*cump_r #transformation for equalization of intensities
	s_k = np.rint(s_k) #Rounding off to nearesr integers

	Iter = dict(zip(r_k,s_k)) #mapping r_k and s_k
	def replace(r):
		return Iter[r] #replacing original r_k with s_k
	replace_v = np.vectorize(replace) #Replacing via vectorisation

	if typ == "RGB":
		img_hsv_array[:,:,2] = replace_v(img_hsv_array[:,:,2])
		final_image_array = cv2.cvtColor(img_hsv_array, cv2.COLOR_HSV2RGB) #Converting hsv image back to RGB
	else:
		img_hsv_array = replace_v(img_hsv_array)
		final_image_array = img_hsv_array
	pil_img = Image.fromarray(final_image_array)
	
	return pil_img

#Logarithmic transformation
def Logarithm(img):
	'''s = c*log(1+r)
	c - scaling constant, chosen such that we get the 
	maximum output value corresponding to the bit size used
	so c = 255/(log(1+255))'''
	c = 255/(math.log10(256))
	img_array = np.array(img)
	length = len(img_array.shape)
	if length == 2:
		typ = "gray"
		img_hsv = img.copy()
		img_hsv_array = np.array(img_hsv, dtype = 'float32')

		def log_r(i,j):
			r = img_hsv_array[i,j]
			l = math.log10(1+r)
			return c*l
		for i in range(0,img_hsv_array.shape[0]):
			for j in range(0,img_hsv_array.shape[1]):
				img_hsv_array[i,j] = log_r(i,j)

	else:
		typ = "RGB"
		img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
		img_hsv_array = np.array(img_hsv)
		
		def log_r(i,j):
			r = img_hsv_array[i,j,2]#Intensity value of the pixel (i,j)
			l = math.log10(1+r)
			return c*l
		for i in range(0,img_hsv_array.shape[0]):
			for j in range(0,img_hsv_array.shape[1]):
				img_hsv_array[i,j,2] = log_r(i,j)
		img_hsv_array = cv2.cvtColor(img_hsv_array,cv2.COLOR_HSV2RGB)

	final_image_array = img_hsv_array
	pil_img = Image.fromarray(final_image_array)

	return pil_img

#Negative Intensity Transformation
def Negative(img):
	img_array = np.array(img)
	length = len(img_array.shape)
	L = 255 #0 to 255 Intensity Levels
	if length == 2:
		typ = "gray"
		img_hsv = img.copy()
		img_hsv_array = np.array(img_hsv)

		for i in range(0,img_hsv_array.shape[0]):
			for j in range(0,img_hsv_array.shape[1]):
				p_ij = img_hsv_array[i,j]
				s_ij = L-p_ij
				img_hsv_array[i,j] = s_ij
		final_image_array = img_hsv_array

	else:
		typ = "RGB"
		img_array = np.array(img)
		for i in range(0,img_array.shape[0]):
			for j in range(0,img_array.shape[1]):
				for a in range(0,img_array.shape[2]):	
					p_ij = img_array[i,j,a]
					s_ij = L-p_ij
					img_array[i,j,a] = s_ij
		final_image_array = img_array
	pil_img = Image.fromarray(final_image_array)

	return pil_img

def Convolution(image, kernel, padding = 1):
	#Flipping the kernel (so we can take sum products directly)
	kernel = np.flipud(np.fliplr(kernel))
	x_k = kernel.shape[0]
	y_k = kernel.shape[1]
	p = int(padding)
	length = len(image.shape)

	if length == 2:
		typ = "gray"
		img_gray = image.copy()

		#Padding the Image
		padded_img = np.zeros((image.shape[0] + 2*p, image.shape[1] + 2*p))
		padded_img[1*p:-1*p,1*p:-1*p] = img_gray

		#Convolved image
		conv_img = np.zeros_like(image)

		#Computing convolution in a loop
		for y in range(image.shape[1]):
			for x in range(image.shape[0]):
				conv_img[x,y] = (kernel * padded_img[x: x+x_k, y: y+y_k]).sum()
				#Sum Products
	else:
		typ = "RGB"
		img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

		#Padding the Image
		padded_img = np.zeros((image.shape[0] + 2*p, image.shape[1] + 2*p,3),np.float32)
		padded_img[1*p:-1*p,1*p:-1*p,:] = img_hsv

		conv_img = img_hsv.copy()

		conv_img[:,:,2] = np.zeros_like(img_hsv[:,:,2])

		#Computing convolution in a loop
		for y in range(image.shape[1]):
			for x in range(image.shape[0]):
				conv_img[x,y,2] = (kernel * padded_img[x: x+x_k, y: y+y_k,2]).sum()
				#Sum Products
		conv_img = cv2.cvtColor(conv_img,cv2.COLOR_HSV2RGB)

	
	return conv_img


def Blur(img,b):
	pd = (b-1)/2
	c = b**2
	k = np.ones((b,b),np.float32)/c
	image_array = np.array(img)
	conv_img = Convolution(image_array,k,pd)
	pil_img = Image.fromarray(conv_img)
	
	return pil_img

def Sharp(img,s):
	if s%2 == 0:
		b = s+1
	else:
		b = s
	k = np.ones((b,b),np.float32)/b**2
	img_array = np.array(img)
	length = len(img_array.shape)

	if length > 2:
		typ = "RGB"	
		hsv_img_array = cv2.cvtColor(img_array,cv2.COLOR_RGB2HSV)
		channel_v = hsv_img_array[:,:,2]
		blur_v = Convolution(channel_v,k,padding = (b-1)/2)	
		mask = channel_v - blur_v
		sharp = mask + channel_v
		hsv_img_array[:,:,2] = sharp
		hsv_img_array[:,:,2] = np.clip(hsv_img_array[:,:,2],0,255)
		shp_img_array = cv2.cvtColor(hsv_img_array,cv2.COLOR_HSV2RGB)

	else:
		typ = "gray"
		hsv_img_array = img_array
		channel_v = hsv_img_array
		blur_v = Convolution(channel_v,k,padding = (b-1)/2)
		mask = channel_v - blur_v
		sharp = mask + channel_v
		hsv_img_array = sharp
		hsv_img_array = np.clip(hsv_img_array,0,255)
		shp_img_array = hsv_img_array

	pil_img = Image.fromarray(shp_img_array)
	return pil_img
