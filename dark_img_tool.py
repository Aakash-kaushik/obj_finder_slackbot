import cv2 
import numpy as np
import glob 

def dark_detect_hist(img):
  gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  dark_part=cv2.inRange(gray,0,30)
  bright_part=cv2.inRange(gray,200,255)

  dark_pixel=np.sum(dark_part>0)
  bright_pixel=np.sum(bright_part>0)
  total_pixel=np.size(gray)
  
  if dark_pixel/total_pixel>0: #the thresholds are set to 0 because they are different for different situations and we couldn't get them right for general cases
    return 1
  if bright_pixel/total_pixel>0: #threshold set to 0
    return 0

#function to detect dark image
def dark_detect(img):
  #img=cv2.imread("rick.jpg")
  lab=cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
  l,a,b=cv2.split(lab)
  l_blur=cv2.GaussianBlur(l,(11,11),5)
  x,y=l.shape
  percent=3/100
  row_percent=int(percent*x)
  col_percent=int(percent*y)
  #maxval=np.array([0])
  num_maxval=0
  maxval_sum=0

  for i in range (1,x-1):
    if i%row_percent==0:
      for j in range (1,y-1):
        if j%col_percent==0:
          img_seg=l_blur[i:i+3,j:j+3]
          (minval,maxval,minloc,maxloc)=cv2.minMaxLoc(img_seg)
        
          maxval_sum=maxval_sum+maxval
          num_maxval=num_maxval+1

  avg_maxval=int(maxval_sum/num_maxval)
  if avg_maxval<90:  #the threshold doesn't works properly
    return 1
  else:
    return 0

#function to enhance dark image
def enhance(dark_check):
  if dark_check==1:
    cap=cv2.VideoCapture(0)
    temp_retval,average=cap.read()
    average=average.astype(np.float)
    for i in range(100):
      retval,frame=cap.read()
      average+=frame

    average=average/100
    output=cv2.normalize(average,None,0,255,cv2.NORM_MINMAX)
    return output
  else:
    return 0

