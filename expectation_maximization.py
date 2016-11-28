#! /usr/bin/env python

import math
import random

NUM_CLASSES = 3

def parse_input(filename):
    values = list()
    with open(filename, 'r') as f:
        for line in f:
            values.append(float(line.strip()))
    return values

def gaussian_probability(x, mean, covariance, prior):
    probability = math.exp((-1/float(covariance)) * ((x - mean)**2)) * prior
    return probability

def main():
    #Initialize values
    #Repeat until convergence:
    #find the expectation for each class
    #Maximize them
    #Values to initialize - means, covariances, priors
    #First, parse the input
    input_filename = "em_data.txt"
    input_values = parse_input(input_filename)

    #Initialize the values
    prior = [1/float(NUM_CLASSES)] * NUM_CLASSES
    mean = []
    covariance = []
    for i in range(NUM_CLASSES):
        mean.append(float(random.randrange(int(max(input_values)))))
        covariance.append(float(random.randrange(int(max(input_values) - min(input_values)))))
    class_labels = range(NUM_CLASSES)
    is_converged = False

    while not is_converged:
        #initialize the list of points
        is_converged = False
        old_mean = mean[:]
        old_covariance = covariance[:]
        old_prior = prior[:]
        gaussian_prob_list = list()
        #Find the expected value of each point
        for point in input_values:
            #Find the probability of each class
            prob_list = list()
            for i in range(NUM_CLASSES):
                prob_list.append(gaussian_probability(point, mean[i], covariance[i], prior[i]))
            gaussian_prob_list.append(prob_list)

        #Now find the new values of mean and variance
        for i in range(NUM_CLASSES):
            mean_numerator, mean_denominator, prior_numerator, prior_denominator, covariance_numerator, covariance_denominator = 0,0,0,0,0,0
            for x_j, prob_list in zip(input_values, gaussian_prob_list):
                g_p = prob_list[i]
                mean_numerator += g_p * x_j
                mean_denominator += x_j
                prior_numerator += x_j
                covariance_numerator = g_p * ((x_j - math.sqrt(covariance[i])) ** 2)
                covariance_denominator = g_p

            mean[i] = mean_numerator / float(mean_denominator)
            covariance[i] = covariance_numerator / float(covariance_denominator)
            prior[i] = prior_numerator / float(len(gaussian_prob_list))

        print mean, covariance, prior
        if mean == old_mean:
            is_converged = True

    print mean, covariance, prior


if __name__ == "__main__":
    main()
