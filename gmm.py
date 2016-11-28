#! /usr/bin/env python

import math
import random
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from scipy.stats import norm


ITERATION_LIMIT = 500

filename = "em_data.txt"

CONVERGENCE_FACTOR = 1.00001

def parse_input(filename):
    input_data = list()
    with open(filename, 'r') as f:
        for line in f:
            input_data.append(float(line.strip()))
    return input_data

def gaussian_probability(x, mean, variance):
    probability = (1 / math.sqrt(2 * math.pi * variance)) * math.exp( ( -1 * (x - mean) ** 2) / 2 * variance)
    return probability

def expectation(input_data, mean, variance, prior, label_list):
    #Returns a list of the probabilities for each point in for each label
    label_prob_list = list()
    for label in label_list:
        gauss_prob_list = list()
        for x in input_data:
            #Calculate the probability of the node belonging to the label
            g_p = gaussian_probability(x, mean[label], variance[label])
            gauss_prob_list.append(g_p)
        label_prob_list.append(gauss_prob_list[:])

    #Now all the probabilities are calculated, need to find the posterior using the priors
    posterior_prob_list = list()
    for label in label_list:
        label_post_list = list()
        for p in range(len(label_prob_list[label])):
            label_post_list.append( (label_prob_list[label][p] * prior[label]) / sum([label_prob_list[l][p] * prior[l] for l in label_list]))
        posterior_prob_list.append(label_post_list[:])

    return posterior_prob_list


def maximize(input_data, mean, variance, prior, label_list, prob_list):
    for label in label_list:
        mean_numerator = 0
        mean_denominator = 0
        variance_numerator = 0
        variance_denominator = 0
        prior_numerator = 0
        for i in range(len(input_data)):
            mean_numerator += prob_list[label][i] * input_data[i]
            mean_denominator += prob_list[label][i] 
        mean[label] = mean_numerator / mean_denominator
        for i in range(len(input_data)):
            variance_numerator += prob_list[label][i] * ((input_data[i] - mean[label]) ** 2) 
            variance_denominator += prob_list[label][i] 
            prior_numerator += prob_list[label][i] 
        variance[label] = variance_numerator / variance_denominator
        prior[label] = prior_numerator / len(input_data)
            
def converged(old_l, l, c_f):
    for x, y in zip(old_l, l):
        if (x > y * c_f or x < y / c_f):
            return False
    return True


def main(k):

    print "Finding Distribution for " + str(k) + " Classes"
    mean = list()
    variance = list()

    reset = True
    while (reset):
        label_list = range(k)

        input_data = parse_input(filename)

        #Initialize the means, variances and priors
        mean = list()
        variance = list()
        prior = list()
        mean_interval = (max(input_data) - min(input_data)) / k
        for label in label_list:
            mean.append(random.uniform(min(input_data), max(input_data)))# + (k * label)))
            variance.append(random.uniform(1, max(input_data) - min(input_data)) / 100.0)
            prior.append(1/float(k))

        is_converged = False
        num_iterations = 0
        reset = False
        while not is_converged and not reset:
            try:
                old_mean = mean[:]
                #Expectation step:
                prob_list = expectation(input_data, mean, variance, prior, label_list)
                #Maximization step
                maximize(input_data, mean, variance, prior, label_list, prob_list)
                if converged(old_mean, mean, CONVERGENCE_FACTOR):
                    print "CONVERGED", mean, variance, prior
                    is_converged = True
                    reset = False
                num_iterations += 1
                if num_iterations > ITERATION_LIMIT:
                    print "EXCEEDED ITERATION LIMIT"
                    reset = True
            except ZeroDivisionError:
                print "EXCEPTION"
                reset = True

    #Plot the gaussians
    for label in range(k):
        mu = mean[label]
        covariance = math.sqrt(variance[label])
        rv = norm(loc = mu, scale = covariance)
        x = np.arange(0, 30, .1)
        plt.plot(x, rv.pdf(x))

    plt.title("Gussian distribution for " + str(k) + " classes")
    plt.show()
    

if __name__ == "__main__":
    main(3)
    main(4)
    main(5)


