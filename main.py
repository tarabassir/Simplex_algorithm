#!/usr/bin/python3.5
#
# File: main.py

import simplex_algorithm

# get number of variables 
var_num = eval(input("Enter number of variables: "))
# get number of constraints
const_num = int(input("Enter number of constraints: "))

coe = []
coe_temp = []
b_temp = []
b = []
eq = []
matrix = []
slack_temp = []
slack = []

for i in range (0, const_num):
    for j in range(0, const_num - 1):
        slack_temp.append(0)
    slack_temp.insert(i, 1)
    slack.append([n for n in slack_temp])
    slack_temp.clear()

for i in range(1, const_num + 1):
    for j in range(1, var_num + 1):
        coe_temp.append(int(input("For constraint " + repr(i) + \
                " enter variable " + repr(j) + "'s coefficient: ")))
    coe.append([n for n in coe_temp])
    coe_temp.clear()
    
for i in range(1,const_num+1):
    b_temp.append(int(input("For constraint " + repr(i) + " enter value of b: ")))
    b.append([n for n in b_temp])
    b_temp.clear()
    
for i in range(1, var_num + 1):
    eq.append(int(input("Enter variable " + repr(i) + " coefficient in equation: ")))   

for i in range(0, const_num):
        eq.append(0)
eq.append(int(input("Enter b value of equation: ")))

simplex = []
simplex_row = []

for __index in range(0, len(slack)):
    simplex_row.extend(coe[__index])
    simplex_row.extend(slack[__index])
    simplex_row.extend(b[__index])
    simplex.append([n for n in simplex_row])
    simplex_row.clear()

simplex.append(eq)

print()

# Calculate the optimal solution from the simplex tableau created from 
# the user input
simplex_algorithm = simplex_algorithm.simplex_algorithm(simplex)

simplex_algorithm.calculate_optimal_solution()
