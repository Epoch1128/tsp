import numpy as np

# map related
num_city = 9
# SA related
t0 = 280 # temperature at time 0
l = 100 * num_city  # iter times
alpha = 0.92 # the temperature decay
SA_mode = 'exp' # "demo" or "exp" when you choos demo then set the iters below <=15

# A* related
max_step = 1e3
# GA related
Pc = 0.4
Pm = 0.01
N = 1000
# Experiments related
iters = 1000
if num_city == 10:
    map = np.array(
        [
            [0.4, 0.4439],
            [0.2439, 0.1463],
            [0.1707, 0.2293],
            [0.2293, 0.761],
            [0.5171, 0.9414],
            [0.8732, 0.6536],
            [0.6878, 0.5219],
            [0.8488, 0.3609],
            [0.6683, 0.2536],
            [0.6195, 0.2634]
        ]
    )

elif num_city == 20:
    map = np.array(
        [
            [5.294, 1.558],
            [4.286, 3.622],
            [4.719, 2.774],
            [4.185, 2.23],
            [0.915, 3.821],
            [4.771, 6.041],
            [1.524, 2.871],
            [3.447, 2.111],
            [3.718, 3.665],
            [2.649, 2.556],
            [4.399, 1.194],
            [4.66, 2.949],
            [1.232, 6.44],
            [5.036, 0.244],
            [2.71, 3.14],
            [1.072, 3.454],
            [5.855, 6.203],
            [0.194, 1.862],
            [1.762, 2.693],
            [2.682, 6.097]
        ]
    )

else:
    map = np.array(
        [
            [0.4, 0.4439],
            [0.2439, 0.1463],
            [0.1707, 0.2293],
            [0.2293, 0.761],
            [0.5171, 0.9414],
            [0.8732, 0.6536],
            [0.6878, 0.5219],
            [0.8488, 0.3609],
            [0.6683, 0.2536],
            [0.6195, 0.2634]
        ]
    )[:num_city]