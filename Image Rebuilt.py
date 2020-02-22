import SimpleITK as sitk
import pydicom
import numpy as np
import cv2
import os

INPUT_FOLDER = "D:/Images/dicoms-liuguanqun/7324/15130"
images = os.listdir(INPUT_FOLDER)
images.sort()
print(images)

count = 1
lstSOPInstanceUID = []
Sortedlst = []

def convert_from_dicom_to_jpg(img, save_path, low_window = -130, high_window = 210): #Window adjustment：from -130 to 210
    ww = high_window - low_window
    newimg = (img - low_window) * ((img - low_window) > 0)
    newimg = (newimg >=ww) * ww + newimg * (newimg < ww)
    newimg = (newimg/ww * 255).astype('uint8')
    cv2.imwrite(save_path, newimg)

for i in range (len(images)): #Read the SOP Instance UID of each dicom file and arrange in ascending order
    ds1 = pydicom.read_file(INPUT_FOLDER + '/' + images[i])
    SOP_UID = ds1.SOPInstanceUID
    lstSOPInstanceUID.append(SOP_UID)

Sortedlst = sorted(lstSOPInstanceUID)

print(lstSOPInstanceUID)
print(Sortedlst)
#print(Sortedlst[1])

for i in range (len(images)):
    for j in range (len(images)):
       ds = pydicom.read_file(INPUT_FOLDER + '/' + images[j])
       outputpath = "D:/Images/output/7324_15130"
       countname = ds.SOPInstanceUID
       countfullname = countname + '.jpg'
       output_jpg_path = os.path.join(outputpath, countfullname)
       document = os.path.join(INPUT_FOLDER + '/' + images[j])
       if ds.SOPInstanceUID == Sortedlst[i]: #Rebuilt .jpg images from dicom files，images arranged based on SOPInstanceUID in ascending order
           ds_array = sitk.ReadImage(document)
           img_array = sitk.GetArrayFromImage(ds_array)

           shape = img_array.shape
           img_array = np.reshape(img_array, (shape[1], shape[2]))
           convert_from_dicom_to_jpg(img_array, output_jpg_path)
           print(ds.SOPInstanceUID)
           print(ds.InstanceNumber)
           count = count + 1
           break