####################################################################
# Author: Laurence Burden
# Date:  20250409
# Purpose: To plot the mappting that will be used in 
#           a piecewise linear function for grayscale stretching
####################################################################


import matplotlib.pyplot as plt
import numpy as np
from enum import Enum

ARG_NAMES = ['r1', 'r2', 's1', 's2']

arg_values = {
  'r1': 0,
  'r2': 0,
  's1': 0,
  's2': 0
}

# Validate input section
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

# Get threshold values
def get_thresholds():
  num_input = 4
  i = 0

  while i < num_input:
    temp_int = input(f'Enter the integer for {ARG_NAMES[i]}: ')
    if check_is_int(temp_int) and check_in_range(int(temp_int)):
      arg_values[ARG_NAMES[i]] = int(temp_int)
      i += 1
    else:
      print("The supplied input does not conform to the parameters of an int between 0 and 255.  Please, try again.")
      continue

def get_slopes():
  slope_a = arg_values['s1'] / arg_values['r1']
  slope_b = (arg_values['s2'] - arg_values['s1']) / (arg_values['r2'] - arg_values['r1'])
  slope_c = (255 - arg_values['s2']) / (255 - arg_values['r2'])
  return [slope_a, slope_b, slope_c]

def print_plot(img1, img2):
  xpoints = img1
  ypoints = img2
  plt.plot(xpoints, ypoints)
  plt.show()
  

def piecewise_func(pix_val:int):
  slopes = get_slopes()

  if (0 <= pix_val and pix_val <= arg_values['r1']):
    return slopes[0] * pix_val
  elif (arg_values['r1'] < pix_val and pix_val <= arg_values['r2']):
    return slopes[1] * (pix_val - arg_values['r1']) + arg_values['s1']
  else:
    return slopes[2] * (pix_val - arg_values['r2']) + arg_values['s2'] 

def main():
  orig_img = np.arange(256)
  linear_func = np.vectorize(piecewise_func)

  get_thresholds()
  
  new_img = linear_func(orig_img)
  print(len(new_img))

  print_plot(orig_img, new_img)

main()
