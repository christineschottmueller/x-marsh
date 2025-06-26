"""
helper_function.py

Contains helper function for running the x-marsh model:

- lineregress: summarizes elevation trends via linear regression.

suppports main function x-marsh model.
"""
import numpy as np

def lineregress(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    # Convert inputs to numpy arrays for ease of computation
    x = np.array(x)
    y = np.array(y)

    x_mean = np.mean(x)
    y_mean = np.mean(y)

    cov_xy = np.sum((x - x_mean) * (y - y_mean))
    var_x = np.sum((x - x_mean) ** 2)

    slope = cov_xy / var_x
    
    return slope
    