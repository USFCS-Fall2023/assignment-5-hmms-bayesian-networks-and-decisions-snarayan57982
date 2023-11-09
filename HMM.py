

import random
import argparse
import codecs
import os
#import numpy

# observations
class Observation:
    def __init__(self, stateseq, outputseq):
        self.stateseq  = stateseq   # sequence of states
        self.outputseq = outputseq  # sequence of outputs
    def __str__(self):
        return ' '.join(self.stateseq)+'\n'+' '.join(self.outputseq)+'\n'
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.outputseq)

# hmm model
class HMM:
    def __init__(self, transitions={}, emissions={}):
        """creates a model from transition and emission probabilities"""
        ## Both of these are dictionaries of dictionaries. e.g. :
        # {'#': {'C': 0.814506898514, 'V': 0.185493101486},
        #  'C': {'C': 0.625840873591, 'V': 0.374159126409},
        #  'V': {'C': 0.603126993184, 'V': 0.396873006816}}

        self.transitions = transitions
        self.emissions = emissions

    ## part 1 - you do this.
    def load(self, basename):
        """reads HMM structure from transition (basename.trans),
        and emission (basename.emit) files,
        as well as the probabilities."""

        transitions = {}
        emissions = {}

        # Load transition probabilities
        with open(basename + '.trans', 'r') as trans_file:
            for line in trans_file:
                tokens = line.strip().split()
                if len(tokens) == 3:
                    state_from = tokens[0]
                    state_to = tokens[1]
                    prob = float(tokens[2])

                    if state_from not in transitions:
                        transitions[state_from] = {}
                    transitions[state_from][state_to] = prob

        # Load emission probabilities
        with open(basename + '.emit', 'r') as emit_file:
            for line in emit_file:
                tokens = line.strip().split()
                if len(tokens) == 3:
                    state = tokens[0]
                    observation = tokens[1]
                    prob = float(tokens[2])

                    if state not in emissions:
                        emissions[state] = {}
                    emissions[state][observation] = prob

        self.transitions = transitions
        self.emissions = emissions

    ## you do this.
    def generate(self, n):
        """return an n-length observation by randomly sampling from this HMM."""
        #observation = Observation([], [])  # Create an empty Observation

        # Start from the initial state ('#') yum
        current_state = '#'
        states_seq = []
        words_seq = []

        for _ in range(n):
            #transitions
            transitions = self.transitions.get(current_state, {})
            states = list(transitions.keys())
            probabilities = list(transitions.values())
            current_state = np.random.choice(states, p = probabilities)

            #emissions
            emissions = self.emissions.get(current_state, {}) #bro the error is because of a . not a , PLZ
            observation = list(emissions.keys())
            probabilities = list(emissions.values())
            emit_word = np.random.choice(observation, p = probabilities)
            words_seq.append(emit_word)

        return states_seq, words_seq

            # randomly select the next state based on transition probabilities wait no i changes this change it
        #return observation

    ## you do this: Implement the Viterbi alborithm. Given an Observation (a list of outputs or emissions)
    ## determine the most likely sequence of states.

    def viterbi(self, observation): #like the usc school of engineering
        """given an observation,
        find and return the state sequence that generated
        the output sequence, using the Viterbi algorithm.
        """
        states = list(self.transitions.keys())
        states.remove('#')
        numOfstates = len(states)
        numObservation = len(observation)

        epsilon = 1e-10 #gets rid of log warning

        viterbiMatrix = np.full((numOfstates, numObservation))

def main():
    model = HMM()
    model.load('two_english')

    print("Transitions: ")
    print(model.transitions)

    print("Emissions: ")
    print(model.emissions)

    print("Sample transitions probablities for '#' state: ")
    if '#' in model.transitions:
        print(model.transitions['#'])
    else:
        print("No '#' state found (transitions)")

    print("Sample emissions probabilities for 'c' state: ")
    if 'c' in model.emissions:
        print(model.emissions['c'])
    else:
        print("No 'C' state found (emissions)")

if __name__ == "__main__":
    main()



