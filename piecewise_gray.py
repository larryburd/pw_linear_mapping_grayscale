##########################################################
# Author: Laurence Burden
# Date: 20250407
# Class: Digital Image Processing
# Professor: Dr. Roya Choupani
# Purpose: To apply a piecewise linear function given a
#           filepath to a photo, a lower limit, and
#           an upper limit.  The program can be run by
#           providing all 3 arguments up activation, or
#           through a guided mode by using zero arguments
##########################################################

import sys
import os.path
from enum import Enum
import cv2 as cv
import numpy as np

# REGION: Helper functions
# Enum for argument types
class checkType:
  PATH = 1
  UPPERLIM = 2
  LOWERLIM = 3

# Returns a truthy value based on if the input is a valid file path
def check_is_path(p):
  return os.path.isfile(p)

# Returns true if input is an integer
def check_is_int(i):
  try:
    int(i) + 1
    return True 
  except:
    return False

# Checks that value is in the range of 0 to 255
def check_in_range(i):
  if i >= 0 and i <= 255:
    return True
  else:
    return False

# Outputs error message if the incorrect input
# is not 'q' or 'Q'. Exits if the input is 'q' or 'Q' 
def check_for_exit(s, CHECK_TYPE):
  if CHECK_TYPE == checkType.PATH:
    text_insert = "filepath"
  elif CHECK_TYPE == checkType.LOWERLIM or CHECK_TYPE == checkType.UPPERLIM:
    text_insert = "integer"
  
  if s == 'q' or s == 'Q':
    exit()
  else:
    print("Invalid ", text_insert, " Entered.  Please enter a valid ", text_insert, " or enter 'q' to quit.")
    return
# END REGION
  
# REGION: Primary functions
# Function to apply the piecewise linear function to the given image
def piecewise_func(args):
  filepath = args[0]
  lower_limit = args[1]
  # Remove 15 if upper limit is above 240 to ensure no overflows occur
  upper_limit = args[2] - 15 if args[2] > 240 else args[2]
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
      # add 15 if the value is between the provided
      # limits. Then add it to the new output image, 
      # otherwise add the pixel with no transformation
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

# Interactive mode to get arguments if app is run with none.
# Each input is validated before passing the arguments to the piecewise func.
def guided_args():
  args = []
  
  # Get a valid filepath from the user
  while True:
    filepath = input("Enter the path to the desired image: ")
    if check_is_path(filepath):
      args.append(filepath)
      break
    else:
      check_for_exit(filepath, checkType.PATH)
      
  
  # Get the lower limit integer
  while True:
    lower_lim = input("Enter an integer between 0-255 for the lower limit: ")
    if check_is_int(lower_lim) and check_in_range(int(lower_lim)):
      args.append(int(lower_lim))
      break
    else:
      check_for_exit(lower_lim, checkType.LOWERLIM)

  # Get the upper limit integer
  while True:
    upper_lim = input("Enter an integer between 0-255 for the upper limit: ")
    if check_is_int(upper_lim) and check_in_range(int(upper_lim)):
      args.append(int(upper_lim))
      break
    else:
      check_for_exit(upper_lim, checkType.UPPERLIM)
  
  piecewise_func(args)

# Check that arguments conform to the 
# needed requirements and exit if they don't.
def inline_args_mode(args):
  # Check first (second in array) argument for being a valid path
  if not check_is_path(args[1]):
    print("\nThe provided filepath is not valid.")
    exit()
  else: 
    filepath = args[1]

  # check that args 3 and 4 are integers
  if check_is_int(args[2]) and check_is_int(args[3]):
    upper_lim = int(args[3])
    lower_lim = int(args[2])
    # Check that integers are in the correct range
    if check_in_range(upper_lim) and check_in_range(lower_lim):
      # Everything is validated, call the gray scale transform
      args = [filepath, lower_lim, upper_lim]
      piecewise_func(args)
    else:
      print("\nThe limits of the function are not valid integers, or it is outside the range of 0-255.")
      exit()

def main():
  # Get all arguments passed in via command line
  args = sys.argv
  num_args = len(args)

  # We check for 1 or 4 args because this python file is arg[0] in the command
  if num_args == 4:
    inline_args_mode(args)
  elif num_args == 1:
    guided_args()
  else:
    print("\nThe program expects exactly 0 or 3 arguments.", \
    "\nProviding no arguments will start guided use mode. Otherwise, provide:",
    "\nArg 1: The path to the image for processing.",
    "\nArg 2: The lower limit, as an integer, for the piecewise linear mapping.", \
    "\nArg 3: The upper limit, as an integer, for the piecewise linear mapping.")
    
    exit()
# END REGION

# Start the program
main()