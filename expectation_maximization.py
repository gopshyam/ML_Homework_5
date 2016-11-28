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
    probability = (1 / math.sqrt(2 * math.pi * covariance)) *  math.exp((-1/float(2.0 * covariance)) * ((x - mean)**2)) * prior
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
    mean = list()
    covariance = []
    for i in range(NUM_CLASSES):
        mean.append(random.uniform(min(input_values), max(input_values)))
        covariance.append(random.uniform(1, (max(input_values) - min(input_values))/10))
    class_labels = range(NUM_CLASSES)
    is_converged = False

    print mean, covariance, prior
    while not is_converged:
        #initialize the list of points
        class_point_list = list()
        for i in range(NUM_CLASSES):
            class_point_list.append(list())
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
            #prob_sum = sum(prob_list)
            #prob_list = [x/prob_sum for x in prob_list]
            class_index = prob_list.index(max(prob_list))
            class_point_list[class_index].append([point, prob_list])
            gaussian_prob_list.append(prob_list)

        #Now find the new values of mean and variance
        for i in range(NUM_CLASSES):
            mean_numerator, mean_denominator, prior_numerator, prior_denominator, covariance_numerator, covariance_denominator = 0,0,0,0,0,0
            for x_j, prob_list in class_point_list[i]:
                g_p = prob_list[i]
                mean_numerator += g_p * x_j
                mean_denominator += x_j

            mean[i] = mean_numerator / float(mean_denominator)


            for x_j, prob_list in class_point_list[i]:
                g_p = prob_list[i]
                prior_numerator += x_j
                covariance_numerator += g_p * ((x_j - mean[i]) ** 2)
                covariance_denominator += g_p

            covariance[i] = covariance_numerator / float(covariance_denominator)
            prior[i] = prior_numerator / float(len(input_values))

        print mean, covariance, prior
        if mean == old_mean:
            print "CONVERGED"
            is_converged = True

    print mean, covariance, prior


if __name__ == "__main__":
    main()
