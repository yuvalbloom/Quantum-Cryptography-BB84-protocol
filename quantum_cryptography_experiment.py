# imports
import numpy as np
import pandas as pd
from numpy import random
import scipy
import matplotlib.pyplot as plt
import math
import endecrypt # might need to download this module


# + base is 0 and 90 degrees in the half wave plate
# x base is 45 and -45 degrees in the half wave plate

# See experiment instructions for theory explanation and experiment steps

# Functions

########################################################################################################################
# First Section - Alice & Bob without Eve
def random_without_eve(length):
    # Generate random base for Alice, Bob, and random bits for Alice
    # Change length for number of bits sent by Alice to Bob and size of base chosen
    
    alice_bit = random.randint(2, size=length)
    
    # for random number generation, 0 is + base and 1 is x base, NOT TO CONFUSE WITH BITS 0 AND 1
    alice_base = ['+' if i == 0 else 'x' for i in random.randint(2, size=(length))]
    bob_base = ['+' if i == 0 else 'x' for i in random.randint(2, size=(length))]
    
    return [alice_bit, alice_base, bob_base]



def simulation_without_eve(alice_base, alice_bit, bob_base):
    # simulation for bob's bits to compare to experiment
    # input is the generated random bases (Alice and Bob) and random bits (Alice)
    # The simulation is used as the 'theoretical' result to compare to the experimental results
    
    bob_bit = []
    n = len(alice_bit)
    
    for i in range(n):
        if alice_base[i] == bob_base[i]: 
            # if the bases are the matching for Alice and Bob, 100% that the bit is the same
            bob_bit.append(alice_bit[i])
        else: 
            # if the bases are not matching for Alice and Bob, 50% that the bit is the same,
            # therefore another random number is generated for this bit
            temp = random.randint(2, size=(1))
            bob_bit.append(temp[0])
    
    return bob_bit



def create_key(alice_base, alice_bits, bob_base, bob_bits):
    # function that creates the key for Alice and Bob
    
    n = len(alice_base)
    
    # initialize base array to compare between Alice and Bob
    matched_base = [None for j in range(n)]
    
    # initialize bit array to compare between alice and bob
    matched_bits = [None for j in range(n)]
    
    # counter to check how many bits are matching/not matching
    # The counter here could be used in order to check for errors during the experiment - if neccesary
    count_true = 0
    count_false = 0
    
    
    # check for matching bases
    # None values in the array are non matching bases
    for i in range(n):
        if alice_base[i] == bob_base[i]:
            matched_base[i] = alice_base[i]
    
    # check for matching bits
    # None values in the array are non matching bits
    for i in range(n):
        if matched_base[i] != None:
            if alice_bits[i] == bob_bits[i]:
                matched_bits[i] = True
                count_true += 1
            elif alice_bits[i] != bob_bits[i]:
                matched_bits[i] = False
                count_false += 1
    
    # count total of bits compared
    total_count = count_true + count_false
    
    accuracy = count_true / n # should be around 50%
    
    # create key
    # should be similar if alice_bits array is used, if there are no errors - we assume for the moment there are none
    res_key = [bob_bits[i] for i in range(n) if matched_base[i] != None]
    
    return [res_key, len(res_key), total_count, count_true, count_false, accuracy]



def shorten_key(data,key):
    # shortens key if it is longer than the given data
    # the key should be the same length as the data for the binary addition
    if len(key) < len(data):
        print('Error - key should be longer than the data')
        return 'Error!'
    return [key[i] for i in range(len(data))]



def encryption(data,key):
    # function which creates the encrypted message using the key created between Alice and Bob
    # using simple binary addition
    # Used by Alice
    
    if len(data) != len(key):
        # if the key is longer than the data, shorten the key
        key = shorten_key(data,key)
    
    encrypted_message = [None for j in range(len(data))]
    
    # binary addition
    for i in range(len(data)):
        if (data[i] == 0 and key[i] == 0) or (data[i] == 1 and key[i] == 1):
            encrypted_message[i] = 0
        elif (data[i] == 1 and key[i] == 0) or (data[i] == 0 and key[i] == 1):
            encrypted_message[i] = 1
            
    return encrypted_message



def decryption(message,key):
    # function which recreates the original message using the key created between Alice and Bob
    # The message argument here is the encrypted message Bob recieves from Alice
    # This function is the same as the encryption function, using simple binary addition
    # Used by Bob
    return encryption(message,key)


def string_to_binary(string):
    # finds the binary value of the message
    # Notice for this experiment purposes, the first two integers are discarded for the used message
    # Should generally be 3, but missing the first zero in this case
    # These first integers are used to differ from lower/upper case letters, which is not used in this experiment for the given key
    return endecrypt.encode(string, 'binary')
    
def binary_to_string(binary):
    # finds the string of the binary value
    # input should be a single string of 1's and 0's accordingly with whitespace between each letter
    # Should enter each letter with the first three integers: Lowercase - 011, Uppercase - 010
    return endecrypt.decode(binary, 'binary')

def string_converter(binary_lst):
    # this function creates an alphabet message from a the binary code
    word_length = 5 # as explained, every word is given as a 5 letter binary code for the message sent
    
    # split the list to different words
    temp = [binary_lst[i:i + 5] for i in range(0, len(binary_lst), 5)]

    bin_data = ''

    for i in range(len(temp)):
        temp[i] = [0,1,0] + temp[i] # add the uppercase digits, can change to lowercase using [0,1,1]
        str_temp = ' ' # notice the whitespace at the beginning of every letter
        res_temp = ' ' # another temporary variable
        for j in range(len(temp[i])): 
            # loop through every word
            str_temp = str(temp[i][j]) # change to string values
            res_temp += str_temp
        bin_data += res_temp
    
    bin_data = bin_data[1:] # delete the first whitespace from the string
    
    binary_values = bin_data.split() # split on whitespace to convert each letter separatley

    res_string = ""
    
    for binary_value in binary_values:
        temp_int = int(binary_value, 2) # create binary value of item
        temp_char = chr(temp_int) # find the letter using the binary alphabet
        res_string += temp_char
    
    return res_string

def binary_converter(string):
    # converts string or message to binary list which corresponds to the message Alice wants to send
    # initialize lists 
    temp_lst = []
    res_lst = []
    
    for character in string:
        # convert to binary
        temp_lst.append(bin(ord(character))[2:].zfill(8))
        
    for i in range(len(temp_lst)):
        # delete three first binary numbers as explained for message
        temp_lst[i] = temp_lst[i][3:]
        
    for j in range(len(temp_lst)):
        # create message as one list of binary numbers to send to Bob via the channel
        for k in range(len(temp_lst[j])):
            res_lst.append(int(temp_lst[j][k]))
    return res_lst



def compare_keys(key1,key2):
    # compare between keys for Alice and Bob
    if key1 != key2:
        return False
    return True


###########################################################################################################################
# Second Section - Alice & Bob with Eve

def random_with_eve(length):
    # Generate random base for Alice, Bob, Eve and random bits for Alice
    # Change length for number of bits sent by Alice to Bob and size of base chosen
    # Note that there are two bases for Eve which are generated randomly - incident base and transmitted base
    
    alice_bit = random.randint(2, size=length)
    
    # for random number generation, 0 is + base and 1 is x base, NOT TO CONFUSE WITH BITS 0 AND 1
    alice_base = ['+' if i == 0 else 'x' for i in random.randint(2, size=(length))]
    bob_base = ['+' if i == 0 else 'x' for i in random.randint(2, size=(length))]
    eve_base_inc = ['+' if i == 0 else 'x' for i in random.randint(2, size=(length))]
    eve_base_tran = ['+' if i == 0 else 'x' for i in random.randint(2, size=(length))]
    
    return [alice_bit, alice_base, bob_base, eve_base_inc, eve_base_tran]

def simulation_with_eve(alice_base,alice_bit,bob_base,eve_base_inc,eve_base_tran):
    # simulation for bob's and eve's bits to compare to experiment
    # input is the generated random bases (Alice, Bob, and two Eve bases) and random bits (Alice)
    # The simulation is used as the 'theoretical' result to compare to the experimental results
    
    # Note here, used two different bases for Eve similar to the experiment itself to create real randomness,
    # where Eve does not really know the true base that Alice sends the bit in.
    
    bob_bit = []
    eve_bit = []
    
    n = len(alice_base)
    m = len(eve_base_tran)
    
    # Eve's part
    for i in range(n):
        if alice_base[i] == eve_base_inc[i]:
            eve_bit.append(alice_bit[i])
        else:
            temp = random.randint(2, size=(1))
            eve_bit.append(temp[0])
    
    # Bob's part
    # Eve's transmitted base
    for j in range(m):
        if eve_base_tran[j] == bob_base[j]:
            bob_bit.append(eve_bit[j])
        else:
            temp = random.randint(2, size=(1))
            bob_bit.append(temp[0])
    
    return [bob_bit, eve_bit]


# function which checks if Eve is listening on the channel between Alice and Bob
# theoretically, the accuracy should be around 25% if there is an evesdropper
# Note only Alice and Bob check their bases and bits
def check_eve(alice_base, bob_base, alice_bits, bob_bits):
    
    n = len(alice_base)
    
    # initialize base and bits to compare between alice and bob
    matched_base = [None for j in range(n)]
    matched_bits = [None for j in range(n)] 
    
    # counter to check how many bits are matching/not matching
    count_true = 0
    count_false = 0
    
    # Check for matching bases
    # None values are non matching bases
    for i in range(n):
        if alice_base[i] == bob_base[i]:
            matched_base[i] = alice_base[i]
    
    # Check for matching bits in the matching bases
    # None values are none matching bases for these bits
    for i in range(n):
        if matched_base[i] != None:
            if alice_bits[i] == bob_bits[i]:
                matched_bits[i] = True
                count_true += 1
            elif alice_bits[i] != bob_bits[i]:
                matched_bits[i] = False
                count_false += 1
    
    # count total of bits compared
    total_count = count_true + count_false
    
    accuracy = count_true / len(alice_bits) # should be around 25% for matching bases
    
    if accuracy >= 0.15 and accuracy <= 0.40: # should be approx 25% so range is chosen for some margin error
        print('Accuracy:',accuracy)
        print('Total Count of Bits Sent by Alice:',len(alice_bits))
        print('Total Count of matching base:',total_count)
        print('Number of bits Not matching:',count_false)
        print('Number of bits matching:',count_true)
        print('Eve is Evesdropping, Create New Key!')
        return
    else:
        print('Accuracy:',accuracy)
        print('Total Count of Bits Sent by Alice:',len(alice_bits))
        print('Total Count of matching base:',total_count)
        print('Number of bits Not matching:',count_false)
        print('Number of bits matching:',count_true)
        print('Key is safe, continue to encryption')
        return 