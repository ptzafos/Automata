#!/usr/bin/env python3

import sys
import argparse
import re


class Automato(object):

    state_map = {}

    """Docstring for Automato. """

    def __init__(self):
        """TODO: to be defined1. """


class State(object):

    """Docstring for . """

    def __init__(self):
        """TODO: to be defined1. """

def readfile(filename):

    integers_regex = re.compile('\d+')
    #Regular expressions problem
    transitions_regex = re.compile('\d \w \d')
    
    input = open(filename,'r')
    num_of_states = int(input.readline())
    start_state = int(input.readline())
    num_of_final_states = int(input.readline())
    final_states = integers_regex.findall(input.readline())
    final_states = list(map(int, final_states))
    num_of_events = int(input.readline())
    transitions = []
    for i, line in enumerate(input):
       transitions.append(transitions_regex.findall(line))
        
    pass
        
if __name__=="__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument("input_file")
   args = parser.parse_args()
   readfile(args.input_file)

   automato = Automato()
   ##insert new keys
   automato.state_map['']
