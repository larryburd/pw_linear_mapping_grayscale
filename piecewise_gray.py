##########################################################
# Author: Laurence Burden
# Date: 20250407
# Class: Digital Image Processing
# Professor: Dr. Roya Choupani
##########################################################

import sys
import os.path
import cv2 as cv
import numpy as np

# Check that arguments conform to the 
# needed requirements and exit if they don't.
# TODO: Add interactive mode to get arguments if app is run with none.
def check_args(args):
  # Return an error if number of args is not exactly 3
  n = len(args) #Number of arguments passed in

  if n != 4:
    print("\nThe program expects exactly 3 arguments.\nArg 1: The path to \
the image for processing.\nArg 2: The lower limit, as an integer,\
for the piecewise linear mapping.\nArg 3: The lower upper limit, as an\
integer, for the piecewise linear mapping.")
    print("Number of args: ", n)
    exit()

  # Check first (second in array) argument for being a valid path
  is_path = os.path.isfile(args[1])
  
  if not is_path:
    print("\nThe provided filepath is not valid.")
    exit()

  # check that args 3 and 4 are integers
  # Cast to integer, because args are passed in as strings
  try:
    arg2 = int(args[2]) + 1
    arg3 = int(args[3]) + 1
  except:
    print("\nThe limits of the function are not valid integers.")
    exit()
  
def piecewise_func(args):
  filepath = args[1]
  lower_limit = int(args[2])
  # Remove 15 if upper limit is above 240 to ensure no overflows occur
  upper_limit = int(args[3]) - 15 if args[3] > 240 else args[3]
  im1 = cv.imread(filepath)
  im2 = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)

  # Get the vertical and horizontal pixel count of the original image
  row = im1.shape[0]
  col = im1.shape[1]

  # Create an "empty" image of all zeros with the same
  # dimensions as the original
  im3 = np.zeros((row,col), np.uint8)

  for i in range(row):
    for j in range(col):
      pixel = im2[i,j]

      # For each pixel in the gray scale image
      # add 15 if the value is less than upper limit
      # and lower than the lower limt. Then add
      # it to the new output image, otherwise
      # add the pixel with no transformation
      if pixel <= lower_limit or pixel >= upper_limit:
        im3[i,j] = pixel
      else:
        im3[i,j] = pixel + 15
  
  # Show original gray scale image and the transformed image
  cv.imshow("Original Image as Gray Scale", im2)
  cv.imshow("After Linear Transformation", im3)

  cv.waitKey(0)
  cv.destroyAllWindows()

#TODO create function to map piecewise function


def main():
  args = sys.argv
  check_args(args)
  piecewise_func(args)

main()