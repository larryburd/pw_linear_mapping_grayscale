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
import cv2 as cv
import numpy as np

ARG_NAMES = ['filepath', 'r1', 'r2', 's1', 's2']
slopes = [0,0,0] # Filled based on input into arg_values
arg_values = { # will be filled with user input
  'filepath': "",
  'r1': 0,
  'r2': 0,
  's1': 0,
  's2': 0
}

# REGION: Helper functions
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

# Checks that each value is in the range of 0 to 255
def check_in_range(num):
  if num or num == 0:
    return (num >= 0 and num <= 255)
  else:
    return (arg_values["r1"] >= 0 and arg_values["r1"] <= 255 \
    and arg_values["r2"] >= 0 and arg_values["r2"] <= 255 \
    and arg_values["s1"] >= 0 and arg_values["s1"] <= 255 \
    and arg_values["s2"] >= 0 and arg_values["s2"] <= 255)

# Outputs error message if the incorrect input
# is not 'q' or 'Q'. Exits if the input is 'q' or 'Q' 
def check_for_exit(s):
  if s == 'q' or s == 'Q':
    exit()
  else:
    print("\nThe supplied input does not conform to the need parameters.\nFilepaths must be an existing file. \
          \nAll other values must be an integer between 0-255. \
          \nPlease, try again or enter Q to quit.\n")
# END REGION
  
# REGION: Primary functions
# Caluculates the slopes for the 3 segments in the piecewise function
def get_slopes():
  slopes[0]= (arg_values['s1'] / arg_values['r1'])
  slopes[1]= (arg_values['s2'] - arg_values['s1']) / (arg_values['r2'] - arg_values['r1'])
  slopes[2] = (255 - arg_values['s2']) / (255 - arg_values['r2'])

# Function to apply the piecewise linear function to the given pixel
def piecewise_func(pix_val):
  # Perform a seperate linear equation based on which "bucket"
  # the pixel value falls into. 
  if (0 <= pix_val and pix_val <= arg_values['r1']):
    return slopes[0] * pix_val
  elif (arg_values['r1'] < pix_val and pix_val <= arg_values['r2']):
    return slopes[1] * (pix_val - arg_values['r1']) + arg_values['s1']
  else:
    return slopes[2] * (pix_val - arg_values['r2']) + arg_values['s2'] 

# Apply transform to the image and show the results
def transform_image():
  im1 = cv.imread(arg_values["filepath"])
  im2 = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)

  # Get the vertical and horizontal resolutions
  row = im2.shape[0]
  col = im2.shape[1]
  
  # Empty image to be filled later
  im3 = np.zeros((row,col), np.uint8)

  # Apply piece wise func to each pixel
  for i in range(row):
    for j in range(col):
      im3[i,j] = piecewise_func(im2[i,j])

  # Show original gray scale image and the transformed image
  cv.imshow("Original Image as Gray Scale", im2)
  cv.imshow("After Linear Transformation", im3)

  cv.waitKey(0)
  cv.destroyAllWindows()

# Interactive mode to get arguments if app is run with none.
# Each input is validated before passing the arguments to the piecewise func.
def guided_inputs():
  num_input = 6
  i = 1 # skip the first argument

  # Get inputs from user and perform input validation before assigning 
  # the value to the appropriate arg_value
  while i < num_input:
    temp_input = input(f'Enter value for {ARG_NAMES[i - 1]}: ')
    if ARG_NAMES[i - 1] == ARG_NAMES[0]:
      if check_is_path(temp_input):
        arg_values["filepath"] = temp_input
        i += 1
      else:
        check_for_exit(temp_input)
        continue
    elif i > 1 and i < num_input + 1:
      if check_is_int(temp_input) and check_in_range(int(temp_input)): 
       arg_values[ARG_NAMES[i - 1]]= int(temp_input)
       i += 1
      else:
        check_for_exit(temp_input)
        continue
  
# Check that arguments conform to the 
# needed requirements, create new image if so,
# and exit if they don't.
def inline_args_mode(args):
  try:
    arg_values["filepath"] = args[1]
    arg_values["r1"] = int(args[2])
    arg_values["r2"] = int(args[3])
    arg_values["s1"] = int(args[4])
    arg_values["s2"] = int(args[5])

    # Check first (second in array) argument for being a valid path
    if not check_is_path(arg_values["filepath"]):
      print("\nThe provided filepath is not valid.")
      exit()

    # check that supplied thresholds are integers between 0 - 255
    if check_in_range(False):
      # Everything is validated
      return
  except Exception as e:
    print(e)
    print("\nThe limits of the function are not valid integers, or it is outside the range of 0-255.")
    exit()

def main():
  # Get all arguments passed in via command line
  args = sys.argv
  num_args = len(args)

  # We check for 1 or 6 args because this python file is arg[0] in the command
  if num_args == 6:
    inline_args_mode(args)
  elif num_args == 1:
    guided_inputs()
  else:
    print("\nThe program expects exactly 0 or 3 arguments.", \
    "\nProviding no arguments will start guided use mode. Otherwise, provide:",
    "\nArg 1: The path to the image for processing.",
    "\nArg 2: r1 for the piecewise linear mapping.", \
    "\nArg 3: r2 for the piecewise linear mapping.", \
    "\nArg 4: s1 for the piecewise linear mapping.", \
    "\nArg 5: s2 for the piecewise linear mapping.")
    exit()

  get_slopes()
  transform_image()
# END REGION

# Start the program
main()