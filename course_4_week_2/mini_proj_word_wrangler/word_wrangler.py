"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import math

WORDFILE = "assets_scrabble_words3.txt"

#listA = [  "b", "c", "d", "d", "g"]
#listB = ["a", "a","c", "c", "f", "g", "g"]


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """

    new_list = []
    prev_word = ""
    for ele in range(len(list1)):
        curr_word = list1[ele]

        if curr_word != prev_word:
            new_list.append(curr_word)
        elif curr_word == prev_word:
            pass
        prev_word = curr_word    
    
    return new_list

#print str(remove_duplicates(listA))
#print str(remove_duplicates([8, 8, 8, 8, 8]))
#expected [8] but received []

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    n_list1 = remove_duplicates(list(list1))
    n_list2 = remove_duplicates(list(list2))
#    print "list1: ", str(n_list1)
#    print "list2: ", str(n_list2)
#    sort_list = []
    
    sort_list = [val for val in n_list1 if val in n_list2]
        
    return sort_list

#print str(intersect([7, 10, 15], [10]))
#expected [10] but received []


#print str(intersect(listB, listA))

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    
    n_list1 = []
    n_list2 = []
    new_list = []
    
    for ele1 in range(len(list1)):
        n_list1.append(list1[ele1])
        
    for ele2 in range(len(list2)):
        n_list2.append(list2[ele2])

    while bool(n_list1) and bool(n_list2):
        
        if n_list1[0] < n_list2[0]:
            new_list.append(n_list1.pop(0))
        else:
            new_list.append(n_list2.pop(0))
            
    return new_list + n_list1 + n_list2 

#print str(merge(listA, listB))
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    
    if (len(list1) == 1 or len(list1) == 0):
        return list1
    
    length = len(list1)
    mid = int(math.floor(length/2))
    n_list1 = []
    n_list2 = []
    
    for ele1 in range(mid):
        n_list1.append(list1[ele1])
        
    for ele2 in range(mid, length):
        n_list2.append(list1[ele2])
        
    sorted_first = merge_sort(n_list1)
    sorted_second = merge_sort(n_list2)
    result = merge(sorted_first, sorted_second) 
    
    return result

#print str(merge_sort(merge(listA, listB)))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """

    start_string = []
    
    if word == "":
        return [word]
    start_word = word[0]
    remain = word[1:]
    next_string = []
    next_string = gen_all_strings(remain)
    for string in next_string:
        if string == "":
            new_string = start_word
            start_string.append(new_string)
        else:
            for ele1 in range(len(string)+1):
                front = string[0:ele1]
                back = string[ele1:]
                new_string = front + start_word + back
                start_string.append(new_string)
    return start_string + next_string

#print str(gen_all_strings("hello"))

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    
    data = []
    for line in netfile.readlines():
        word = line.strip()
        data.append(word)
    
    return data

#print str(load_words(WORDFILE))

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()

    
    