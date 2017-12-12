#!/usr/bin/env python3

import argparse
import re
from collections import defaultdict


class DetAutomato(object):

    def __init__(self, start_state, transitions, final_states):
        self.start_state = str(start_state)
        self.curr_state = str(start_state)
        self.final_states = list(map(str, final_states))
        self.state_map = defaultdict(dict)
        for trans in transitions:
            self.state_map[trans[0]][trans[2]] = trans[4]


class NonDetAutomato(object):

    def __init__(self):
        pass

# this kind of implementation can just ignore the number of final states and number of transitions.
# so we can use a smaller input file
def readfile(filename):
    integers_regex = re.compile('\d+')
    # Regular expressions problem
    transitions_regex = re.compile('\d \w \d')
    input = open(filename, 'r')
    num_of_states = int(input.readline())
    start_state = int(input.readline())
    num_of_final_states = int(input.readline())
    final_states = integers_regex.findall(input.readline())
    final_states = list(map(int, final_states))
    num_of_events = int(input.readline())
    transitions = []
    for i, line in enumerate(input):
        transitions.append(str(transitions_regex.findall(line)[0]))
    return_vector = str(start_state), final_states, transitions
    return return_vector;


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    start_state, final_states, transitions = readfile(args.input_file)
    automato = DetAutomato(start_state, transitions, final_states)
    prompt_list = ['YES', 'yes', 'y', 'Y']
    question = 'YES'
    word = ''
    while question in prompt_list:
        print('Please insert a word to the automato:')
        del word
        word = input()

        # Case empty string
        if not word:
            print('Empty String.')
            print("You want to continue? Type yes for another try:")
            question = input()
            continue

        valid = True
        for event in word:
            if event in automato.state_map[automato.curr_state]:
                prev_state = automato.curr_state
                automato.curr_state = automato.state_map[automato.curr_state][event]
                print('Transition from state {} in state {}'.format(prev_state, automato.curr_state))
            else:
                print('automato {}'.format(automato.curr_state))
                print('Not a valid word. Automato finished in state {}'.format(automato.curr_state))
                valid = False
                break

        # Case deadlock
        if not valid:
            automato.curr_state = start_state
            print("You want to continue? Type yes for another try:")
            question = input()
            continue

        # Case final state or not
        if automato.curr_state in automato.final_states:
            print('Valid word. Automato finished in state {}'.format(automato.curr_state))
        else:
            print('Automato finished in state {} that is not final.'.format(automato.curr_state))

        automato.curr_state = start_state
        print('You want to continue? Type yes for another try:')
        question = input()
