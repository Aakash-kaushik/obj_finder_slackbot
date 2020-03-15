import numpy as np
from PIL import Image
from ISR.models import RDN, RRDN
import cv2

def SuperRes(name):# changes the output shown to the user/client
  img = Image.open('name')
  lr_img = np.array(img)
  rdn = RDN(weights='noise-cancel')
  sr_img = rdn.predict(lr_img)
  rrdn = RRDN(weights='gans')
  lr_img = rrdn.predict(sr_img)
  sr_img = rdn.predict(lr_img)
  cv2.imwrite("name", Image.fromarray(sr_img))
  
def frameEnhancer(frame):# changes the input to the model
  lr_img = np.array(img)
  rdn = RDN(weights='noise-cancel')
  sr_img = rdn.predict(lr_img)
  rrdn = RRDN(weights='gans')
  lr_img = rrdn.predict(sr_img)
  sr_img = rdn.predict(lr_img)
  frame = Image.fromarray(sr_img)
  return frame
  



