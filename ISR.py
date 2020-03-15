import numpy as np
from PIL import Image
from ISR.models import RDN, RRDN

def SuperRes(lr_img):
  rdn = RDN(weights='noise-cancel')
  sr_img = rdn.predict(lr_img)
  rrdn = RRDN(weights='gans')
  lr_img = rrdn.predict(sr_img)
  sr_img = rdn.predict(lr_img)
  Image.fromarray(sr_img)



