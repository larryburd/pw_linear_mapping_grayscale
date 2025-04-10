####################################################################
# Author: Laurence Burden
# Date:  20250409
# Purpose: To plot the mappting that will be used in 
#           a piecewise linear function for grayscale stretching
####################################################################


import matplotlib.pyplot as plt
import numpy as np

ARG_NAMES = ['r1', 'r2', 's1', 's2']
arg_values = { # will be filled with user input
  'r1': 0,
  'r2': 0,
  's1': 0,
  's2': 0
}
slopes = [0,0,0] # Filled based on values input into arg_values

# Validate input section
def check_is_int(i):
  try:
    int(i) + 1
    return True 
  except:
    return False

def check_in_range(i):
  if i >= 0 and i <= 255:
    return True
  else:
    return False

# Get threshold values
def get_thresholds_input():
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

# Caluculates the slopes for the 3 segments in the piecewise function
def get_slopes():
  slopes[0]= (arg_values['s1'] / arg_values['r1'])
  slopes[1]= (arg_values['s2'] - arg_values['s1']) / (arg_values['r2'] - arg_values['r1'])
  slopes[2] = (255 - arg_values['s2']) / (255 - arg_values['r2'])
  

def print_plot(img1, img2):
  xpoints = img2
  ypoints = img1

  fig = plt.figure()
  pl = fig.add_subplot()
  pl.set_title('Piecewise Linear Function Mapping', fontsize=15)
  pl.set_xlabel('Input Pixel Value', fontsize=12)
  pl.set_ylabel('Output Pixel Value', fontsize=12)
  pl.text(10,190,f'Thresholds: \nr1: {arg_values["r1"]}\nr2: {arg_values["r2"]} \n' + \
          f's1: {arg_values["s1"]}\ns2: {arg_values["s2"]}', bbox={
            'facecolor': 'grey', 'alpha': 0.5, 'pad': 10})
  pl.annotate(f'({arg_values["s1"]}, {arg_values["r1"]})', xy=(arg_values['s1'], arg_values['r1']), \
              xytext=(arg_values['s1']+5, arg_values['r1']-20), fontsize=12)
  pl.annotate(f'({arg_values["s2"]}, {arg_values["r2"]})', xy=(arg_values['s2'], arg_values['r2']), \
              xytext=(arg_values['s2']+5, arg_values['r2']-20), fontsize=12)

  pl.plot(xpoints, ypoints)
  plt.show()
  

def piecewise_func(pix_val:int):
  # Perform a seperate linear equation based on whcih "bucket"
  # the pixel value falls into. 
  if (0 <= pix_val and pix_val <= arg_values['r1']):
    return slopes[0] * pix_val
  elif (arg_values['r1'] < pix_val and pix_val <= arg_values['r2']):
    return slopes[1] * (pix_val - arg_values['r1']) + arg_values['s1']
  else:
    return slopes[2] * (pix_val - arg_values['r2']) + arg_values['s2'] 

def main():
  orig_img = np.arange(256)
  apply_linear_func = np.vectorize(piecewise_func)

  get_thresholds_input()
  
  get_slopes()

  new_img = apply_linear_func(orig_img)

  print_plot(orig_img, new_img)

main()
