#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import sys
import getopt

import nltk
import pandas as pd
import numpy as np


def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print("building language models...")

    # This is an empty method
    # Pls implement your code below
    

    # open the input file for building the LM. Split the label and string accordingly
    try:
        file = open(in_file, encoding="utf8")
    except:
        print(f"Unable to open input file, please check for errors with {in_file}")
        return

    try:
        labels = []
        strings = []
        for line in file:
            label, string = line.split(" ", 1)
            label = label.lower()
            string = string.lower()
            
            labels.append(label)
            strings.append(string.strip('\n'))
    except:
        print(f"Unable to process {in_file}")
        return

    try:
        # vocabulary is a dictionary that simply indicates whether a fourgram exists or not
        vocab = {}
        
        # language model contains the fourgrams specific to a language
        language_model = {}
        for label in labels:
            language_model[label] = {}

        # with strings, create the character based 4-gram. We will ignore padding of <START> and <END>
        # we will further clean the 4-grams    
        
        # for every string that we have, each corresponding to one label
        for i, string in enumerate(strings):
            # turn the string into fourgrams
            fourgrams = list(nltk.ngrams(string, 4))

            # for every fourgram tuple inside the fourgrams list, we add to the vocabulary
            for fourgram in fourgrams:
                vocab[fourgram] = vocab.get(fourgram, 0) + 1
                
                # we further add the fourgram tuple count to the correct language within our language models
                language_model[labels[i]][fourgram] = language_model[labels[i]].get(fourgram, 0) + 1
            

        # perform add-one smoothing for our three languages based on the full vocabulary set
        # this adds in the fourgrams that are in the other languages as well
        for fourgram in vocab.keys():
            for language in language_model:
                language_model[language][fourgram] = language_model[language].get(fourgram, 0) + 1

        # perform probability conversion - we need the full count of all the fourgrams for each language
        for language in language_model:
            total_fourgrams = sum(language_model[language].values())

            # convert each fourgram count into a probability
            for fourgram in language_model[language].keys():
                language_model[language][fourgram] = language_model[language][fourgram] / total_fourgrams
    except:
        print("Unable to generate language model")
        return

    return language_model


def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    # This is an empty method
    # Pls implement your code below

    
    # open the input file that contains the test sentences
    try:
        file = open(in_file, encoding="utf8")
    except:
        print(f"Unable to open input file, please check for errors with {in_file}")
        return


    try:
        strings_original = [] 
        strings = []

        for line in file:
            strings_original.append(line)
            string = line.lower()
            strings.append(string.strip('\n'))
        
        label_predictions = []
        output_text = []
    except:
        print(f"Unable to process {in_file}")
        return
    
    try:
        # for every string that we have, that needs to be given one label as a prediction 
        for i, string in enumerate(strings):
            # turn the string into fourgrams
            fourgrams = list(nltk.ngrams(string, 4))

            # for every fourgram tuple inside the fourgrams list, we check against the language_model dictionary built from the training step
            # we then compute the probabilities for each language and take the highest probability as the assigned label 
            language_probability = {"malaysian": 0, "indonesian": 0, "tamil": 0}
            fourgrams_matched = {"malaysian": 0, "indonesian": 0, "tamil": 0}

            # for every fourgram in a string, we look up the associated probabilities by language and get the overall probability of the string 
            for fourgram in fourgrams:
                for language in LM.keys():
                    # return the probability associated with the fourgram for a particular language
                    # default return value is 1 because the next step where we log the probability will give 0 for log(1)
                    # this is because the assignment states to "Ignore the four-gram if it is not found in the LMs"
                    fourgram_probability = LM[language].get(fourgram, 1)

                    # we sum the log probability to avoid underflow from repeated multiplication of very small probabilities 
                    language_probability[language] = language_probability[language] + np.log(fourgram_probability)

                    # if we get probability 1, that means we did not find the fourgram in our language_model
                    if fourgram_probability != 1:
                        fourgrams_matched[language] = fourgrams_matched[language] + 1

            # we select the language with maximum probability as the label
            label_predictions.append(max(language_probability, key=language_probability.get))

            # we further verify if it is a feasible deduction - if there are very few fourgrams that match that language, then it is likely to be a foreign language
            # it is possible to have all languages match zero fourgrams, in which case the probability value will be 0 for all, and this is also a case to classify as foreign language
            
            # consider the probability values that we have from the language model - they are all <1, and therefore log(probability) will always be negative
            # given the large number of fourgrams in our language models, we would expect the resultant sum of probability to be very negative
            # therefore we can set a threshold that if the maximum language probability is not negative enough, it is unlikely to be from any of our languages
            # we set a single 10% probability as the threshold - recall that we need repeated additions of negative log probabilities, hence this is a logical cutouff
            if language_probability[label_predictions[i]] > np.log(0.01):
                label_predictions[i] = "other"
            
            # we set an arbitrary threshold that in order for the prediction to be considered valid, we must at least have 40% of the fourgrams in the string be identified from the language
            # the setting of 40% is arbitrary, but simply serves to ensure that at least some portion of our string has been matched with fourgrams from the language
            # of course, 40% might be very high, but to optimize this parameter will require more training and data to accurately determine the value 
            elif fourgrams_matched[label_predictions[i]] <= len(fourgrams) * 0.4:
                label_predictions[i] = "other"
            
            # we craft the output text in preparation for the output file, in the format of {label} {string_original}
            output_text.append(f"{label_predictions[i]} {strings_original[i]}")
    except:
        print("Unable to generate predictions")
        return
    
    try:
        # with our final predicted label, we are to follow the format of input.train.txt for our output file
        with open(out_file, 'w') as file:
            file.writelines("%s" % line for line in output_text)
    except:
        print(f"Unable to create output file, please check for errors with {out_file}")
        return

    return


def usage():
    print(
        "usage: "
        + sys.argv[0]
        + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"
    )


input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "b:t:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == "-b":
        input_file_b = a
    elif o == "-t":
        input_file_t = a
    elif o == "-o":
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
