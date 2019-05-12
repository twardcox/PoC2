
Run (Accesskey R)
  
Save (Accesskey S)
  
Download
  
Fresh URL
  
Open Local
  
Reset (Accesskey X)
  
Viz mode
 CodeSkulptor 
Docs
  
Demos
  
Tutorial
 
1
"""
2
Visualizing the execution of several 
3
simple recursive functions
4
"""
5
 
6
def collatz(num, count):
7
    """
8
    Given n, repeatedly perform n = f(n) where
9
    f(n) = n / 2 if n is even
10
    f(n) = 3 * n + 1 is n is odd
11
    Return number of iterations of this redution
12
    """
13
    if num == 1:
14
        return count
15
    elif (num % 2) == 0:
16
        return collatz(num / 2, count + 1)
17
    else:
18
        return collatz(3 * num + 1, count + 1)
19
    
20
print( collatz(5, 0))
21
 
22
 
23
def quicksort(num_list):
24
    """
25
    Recursive O(n log(n)) sorting algorithm
26
    Takes a list of numbers
27
    Returns sorted list of same numbers
28
    """
29
    if num_list == []:
30
        return num_list
31
    else:
32
        pivot = num_list[0]
33
        lesser = [num for num in num_list if num < pivot]
34
        pivots = [num for num in num_list if num == pivot]
35
        greater = [num for num in num_list if num > pivot]
36
        return quicksort(lesser) + pivots + quicksort(greater)
37
    
38
 
39
#print( quicksort([4, 5, 3, 1]))
40
 
41
 
42
 
43
 
44
 

CodeSkulptor was built by Scott Rixner and is based upon CodeMirror and Skulpt. Viz mode was built by Terry Tang and utilizes Online Python Tutor's visualization code.