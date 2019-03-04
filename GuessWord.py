# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:50:07 2019

@author: Nataliya_Pavych
"""

import random
import numpy as np


def TopicChoice(symbol):
    """From which file words shoud be loaded according to user choice"""
    KeyChoice = {
                'A': 'TestData\Amphibians.txt', 
                'a': 'TestData\Amphibians.txt',
                'B': 'TestData\Birds.txt', 
                'b': 'TestData\Birds.txt',
                'M': 'TestData\Mammals.txt',
                'm': 'TestData\Mammals.txt'
    }
    return KeyChoice.get(symbol)

def PrintAttemptCount(current: int, total: int):  
    """Print the number of attempts"""
    print("Now you are taking {0} from {1} attempts.".format(current, total))
    
def GuessingByLetters(Word):
    """Guessing letters in the word"""
    GuessedWord = list(''.join(('?' for i in range(len(Word)))))
    Letters = []
    AttemptCount = 1
    MaxAttempt = len(SecretWord)+1                  # Max attempt can be less than length of the word 
    print('Now word to guess is: \n')
    print(''.join(GuessedWord))
    print('You have '+str(MaxAttempt)+' attemps')
    PrintAttemptCount(AttemptCount, MaxAttempt)
    Alphabet = 'abcdefghijklmnopqrstuvwxyz'
    while AttemptCount < MaxAttempt+1:
        Attempt = input('Enter a letter \n').lower()
        if not Attempt in Alphabet:                 #check input
            print('Enter a letter from a-z ')
        elif Attempt in Letters:                    #check if letter has been already used   
            print('You have already guessed that letter!')
        else:
            Letters.append(Attempt)
            if Attempt in SecretWord:
                print('Correct !')
                for i in range(0, len(SecretWord)):
                    if SecretWord[i] == Attempt:
                        GuessedWord[i] = Attempt
                print(''.join(GuessedWord))
                if not '?' in GuessedWord:
                    print('You won!')
                    print('You took '+str(AttemptCount)+' attemps')
                    break
                AttemptCount += 1
                PrintAttemptCount(AttemptCount, MaxAttempt)
            else:
                print('The letter is not in the word. Try Again!')
                AttemptCount += 1
                PrintAttemptCount(AttemptCount, MaxAttempt)
            if AttemptCount == MaxAttempt+1:
                print(' Sorry, you lost! The secret word was {0}'.format(SecretWord.upper()))                                                
                
# Main section
TopicList=['Amphibians','Birds','Mammals']
print('Choose a topic:')
print(' A if the topic is '+str(TopicList[0]))
print(' B if the topic is '+str(TopicList[1]))
print(' M if the topic is '+str(TopicList[2]))
try:
    Topic=''
    while Topic=='' or Topic not in ['A','a','B','b','M','m']:
        Topic=input('Try enter A or B or M \n')     # User chooses a topic
        FileName=TopicChoice(Topic)                 # File with proper word list
except:
    print()
         
WordList = np.loadtxt(FileName,                     #Loading word list from a file
                      delimiter='\n',
                      dtype=str)
print(WordList)                                     # for test/hints purposes       

SecretWord = random.choice(WordList)                #Picking random word

GuessingByLetters(SecretWord)