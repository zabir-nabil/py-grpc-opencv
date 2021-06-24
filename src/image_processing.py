import numpy as np
import cv2

# mean filter
def mean(img):
  if len(img.shape) == 2 or (len(img.shape) == 3 and img.shape[-1] == 1):
    # single channel
    img = img.reshape(img.shape[0], img.shape[1])
    img_c = img.copy()
    # print(img_c)
    # set filter
    for i in range(img.shape[0]):
      for j in range(img.shape[1]):
        img_c[i,j] = int(np.mean(img[max(0, i-1): min(img.shape[0], i+2),  max(0, j-1): min(img.shape[1], j+2)])) # int casting is important for image
    
    return img_c
  else: # 3 channel image
    # 3 channel
    img_c = img.copy()
    # print(img_c)
    # set filter
    for ch in range(img.shape[2]):
      for i in range(img.shape[0]):
        for j in range(img.shape[1]):
          img_c[i,j,ch] = int(np.mean(img[max(0, i-1): min(img.shape[0], i+2),  max(0, j-1): min(img.shape[1], j+2), ch])) # int casting is important for image
    
    return img_c

# rotate
# grab the dimensions of the image and calculate the center of the
# image
def rotate_img(image, deg):
  (h, w) = image.shape[:2]
  (cX, cY) = (w // 2, h // 2)
  # rotate our image by 45 degrees around the center of the image
  M = cv2.getRotationMatrix2D((cX, cY), deg, 1.0)
  rotated = cv2.warpAffine(image, M, (w, h))
  return rotated

def rotate(img, flag):
  if flag == "NINETY_DEG": # Positive rotations are counter clockwise.
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img
  elif flag == "ONE_EIGHTY_DEG":
    img = rotate_img(img, 180)
    return img
  elif flag == "TWO_SEVENTY_DEG":
    img = rotate_img(img, 270)
    return img
  else:
    return img

