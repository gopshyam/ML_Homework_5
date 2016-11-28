#! /usr/bin/env python

from sklearn.mixture import GaussianMixture
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import sys

n_components = 3

if (len(sys.argv) > 1):
    n_components = int(sys.argv[1])

filename = "em_data.txt"

def parse_input_data(filename):
    input_data = list()
    with open(filename, 'r') as f:
        for line in f:
            input_data.append(float(line.strip()))
    return input_data


input_data = parse_input_data(filename)

gmm = GaussianMixture(n_components = n_components, covariance_type = 'spherical')
gmm.fit(np.array(input_data).reshape(-1,1))

print dir(gmm)
print gmm.means_, gmm.covariances_, gmm.weights_

for mean, covariance in zip(gmm.means_, gmm.covariances_):
    rv = norm(loc = mean, scale = covariance)
    x = np.arange(0, 30, .1)
    plt.plot(x, rv.pdf(x))

plt.title("Gaussian Distribution for " + str(n_components) + " classes")
plt.show()
