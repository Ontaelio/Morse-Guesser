from random import *
from time import sleep
import requests
import json

from mc_wordsets import *

## some additinal globals
## (defaults are in mc_wordsets file)
morse_code = get_codes('morse-code.json')
answers = []

try:
    import winsound
except ImportError:
    ## some code needed here for alternative ways to produce
    ## beep on non-Windows systems
    print('Sounds available only on Windows systems, sorry.')
    sound_on = False
    def play_sound(frequency, duration):
        pass
else:
    if sound_on: print('Sound is ON')
    else: print('Sound is OFF')
    def play_sound(frequency, duration):
        ''' play a single beep sound '''
        winsound.Beep(frequency, duration)

## sound stuff
def play_dit():
    ''' play a single dit '''
    play_sound(morse_frequency, dit_duration)
    sleep(dit_duration/1000)

def play_dah():
    ''' play a single dah '''
    play_sound(morse_frequency, dit_duration*3)
    sleep(dit_duration/1000)

def play_space():
    ''' be silent for two dits '''
    sleep(dit_duration/500)

def play_long_space():
    ''' be silent for six dits '''
    sleep((dit_duration*6)/1000)
    
def play_morse(string):
    '''
    play a single dit or dah followed by empty dit
    (if sound is off, just print it)
    '''
    for ditdah in string:
        if ditdah == '\t': print(' ', end = '')
        else: print(ditdah, end = '')
        if sound_on:
            if ditdah == '.': play_dit()
            elif ditdah == '-': play_dah()
            elif ditdah == ' ': play_space()
            elif ditdah == '\t': play_long_space()
    print()

## game functions
def morse_encode(word):
    '''
    Encode a word into Morse code
    '''

    encoded_word = ''
    for letter in word.lower():
        encoded_word += morse_code[letter] + ' '

    return encoded_word

def print_statistics(answers):
    '''
    Print game stats for the current session (all tries)
    '''
    print('Total words:', len(answers))
    print('Correct answers:', answers.count(True))
    print('Incorrect answers:', answers.count(False))

def select_wordset():
    '''
    Lets the player choose the wordset,
    returns wordset and definitions, if needed,
    or 0 if error or Quit
    '''
    
    print('Select words source:\n'
          '1: Practice set\n'
          '2: Local wordset\n'
          '3: Fetch wordset from the Web\n'
          '4: Non-existent words\n'
          'Q: Quit')
    mode_select = input('>')
    if mode_select.upper() not in ['1', '2', '3', '4', 'Q']:
        print('Err, what? I assume that was Q.')
        mode_select = 'Q'

    if mode_select.upper() == 'Q':
        print('Bye!')
        return 0, 0
    print()
    if mode_select == '1': return fetch_from_simple()
    if mode_select == '2': return fetch_from_hard()
    if mode_select == '3': return fetch_from_net()
    if mode_select == '4': return false_words()

## Ok, let's start!
## The program is pretty small, so no real reason to wrap it in main function
    
print("Let's do some Morse decoding!")
words, definitions = select_wordset()

## the whole game session in a cycle
## check whether words actually hold anything
while words:
    
    for k in range(len(words)):

        word = words[k]

        print(f'Word {k+1}: ', end = '')
        play_morse(morse_encode(word))
        answer = input('> ')

        ## just in case some multi-words are present somewhere
        check_word = word.replace(' ','')
        answer = answer.replace(' ','')
        
        if answer.lower() == check_word.lower():
            print(f'Correct!')
            answers.append(True)
        else:
            print(f'Incorrect, the word was {word.capitalize()}!')
            answers.append(False)

        if definitions:
            print(f"({definitions[k].rstrip()})")

        print()

    ## print statistics for the current game session
    print_statistics(answers)
    print()
    words, definitions = select_wordset()
