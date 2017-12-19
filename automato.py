#!/usr/bin/env python3

import argparse
import re
from collections import defaultdict


class Automato(object):

    # initialization states, transition maps
    def __init__(self, start_state, transitions, final_states):

        self.start_state = list(str(start_state))
        self.curr_state = list(str(start_state))
        self.final_states = list(map(str, final_states))
        self.state_map = defaultdict(dict)
        for trans in transitions:
            self.state_map[trans[0]][trans[2]] = []
        for trans in transitions:
            self.state_map[trans[0]][trans[2]].append(trans[4])

    # perform initial check for epsilon transitions
    def init_states_check(self):
        if '@' in self.state_map[self.curr_state[0]]:
            self.curr_state.extend(self.state_map[self.curr_state[0]]['@'])
        return self

    def change_of_state(self, event):

        next_state = []
        for state in self.curr_state:
            # case we have epsilon transitions
            if '@' in self.state_map[state]:
                next_state.extend(self.state_map[state]['@'])
            # for a standard event make a new set of current states
            if event in self.state_map[state]:
                next_state.extend(self.state_map[state][event])
        # remove dublicates
        self.curr_state = next_state
        unique_current_states = set(self.curr_state)
        self.curr_state = list(unique_current_states)
        return self


# this kind of implementation can just ignore the number of final states and number of transitions.
# so we can use a smaller input file
def readfile(filename):

    integers_regex = re.compile('\d+')
    transitions_regex = re.compile('\d [a-z@] \d')

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
    automato = Automato(start_state, transitions, final_states)
    automato = automato.init_states_check()
    print('Initial State(s): {}'.format(', '.join(automato.curr_state)))
    prompt_list = ['YES', 'yes', 'y', 'Y', 'No', 'no', 'N', 'n']
    yes_prompt_list = ['YES', 'yes', 'y', 'Y']
    no_prompt_list = ['No', 'no', 'N', 'n']
    question = 'YES'
    word = ''
    while question in prompt_list:
        print('Please insert a word to the automato:')
        del word
        word = input()

        valid = True
        for event in word:
            prev_state = automato.curr_state
            automato.change_of_state(event)
            if not automato.curr_state:
                print('Not a valid word. State set is empty'.format(automato.curr_state))
                # switch to false in order to stop iteration cause a
                # state was reached that the event could not make a transition
                valid = False
                break
            else:
                print('Transition from state(s) {} in states {}'.format(', '.join(prev_state),
                                                                        ', '.join(automato.curr_state)))

        # Case deadlock - kill automato - prompt for another word
        if not valid:
            print("You want to continue? Type yes for another try or no for termination:")
            question = input()
            while question not in prompt_list:
                print("You want to continue? Type yes for another try or no for termination:")
                question = input()
            if question in no_prompt_list:
                break
            else:
                automato.curr_state = list(str(start_state))
                automato = automato.init_states_check()
                continue

        final_states_set = set(automato.curr_state).intersection(set(automato.final_states))
        final_states = list(final_states_set)

        if not final_states:
            print('Automato finished in state(s) {} that is not final.'.format(', '.join(automato.curr_state)))
        else:
            print('Valid word. Automato finished in states {}'.format(', '.join(final_states)))

        print("You want to continue? Type yes for another try or no for termination:")
        question = input()
        while question not in prompt_list:
            print("You want to continue? Type yes for another try or no for termination:")
            question = input()
        if question in no_prompt_list:
            break
        else:
            automato.curr_state = list(str(start_state))
            automato = automato.init_states_check()
