import numpy as np
import cv2
from scipy import ndimage
from skimage import filters
import glob

def OTSU_2D(imgs): #OTSU's method for each pic in the slices
     tmp = []
     for i in range(len(imgs)):
         dst = cv2.filter2D(imgs[i], -1, kernel=kernel)
         thresh = filters.threshold_otsu(dst)  # OTSU's method, returns back a auto-calculated threshold.
         print(thresh)
         otsu = (dst <= thresh) * 1.0  # 根据阈值进行分割
         tmp.append(otsu)
     return tmp

def Dilation(otsu_img): #Erosion for each OTSU-processed pic, the ROI region is showed in black
     for i in range(len(otsu_img)):
         med_denoised = ndimage.median_filter(otsu_img[i], 3) #Median-filtering
         bin_dilation = ndimage.morphology.binary_dilation(med_denoised, structure=None, iterations = 2).astype(np.float32)
         cv2.imwrite('D:/Images/Erosion/7321_15124_1/%d'%i + '.jpg', bin_dilation * 255) #Output mask in .jpg form
     return bin_dilation

images = [cv2.imread(file, 0) for file in glob.glob("D:/Images/cut/7321_15124_1/*.jpg")]
OTSU_IMG = []
BIN_EROSION = []

OTSU_IMG = OTSU_2D(images)
BIN_EROSION = Dilation(OTSU_IMG)
cv2.waitKey(0)