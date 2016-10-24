#!/usr/bin/python3.5
#
# File: simplex-algorithm.py

import copy
import math

class simplex_algorithm:
#------------------------------------------------------------------------------

    # Constructor
    #
    # @parameter simplex_tableau: Dynamic 2-dimensional array
    def __init__(self, simplex_tableau):
        """Initializes the object internal matrix with the simplex tableau."""

        self.__basic_variables = []

        # Store the simplex tableau internally
        self.__simplex_tableau = simplex_tableau
        self.__nrows = len(self.__simplex_tableau)
        # Keep track of the size of the simplex tableau
        self.__ncols = len(self.__simplex_tableau[self.__nrows - 1])

        # Determine the number of input and slack variables
        self.__slack_variable_count = self.__nrows - 1
        self.__input_variable_count = self.__ncols - \
                self.__slack_variable_count - 1

        for __index in range(0, self.__slack_variable_count):
            self.__basic_variables.append(self.__input_variable_count + __index)

#------------------------------------------------------------------------------

    def __display_simplex_tableau(self):
        """Displays the current state of the simplex tableau."""

        for __index in range(0, self.__input_variable_count):
            print(('x' + repr(__index + 1)).rjust(6), end=' ')
        for __index in range(0, self.__slack_variable_count):
            print(('s' + repr(__index + 1)).rjust(6), end=' ')
        print('b'.rjust(6))

        # Print the simplex tableau
        for row in self.__simplex_tableau:
            for column in row:
                print(repr(math.ceil(column * 100) / 100).rjust(6), end=' ')

            print()

        # Print the current solution
        print("\n                 ", end=' ')
        for __index in range(0, self.__input_variable_count):
            print(('x' + repr(__index + 1)).rjust(6), end=' ')
        for __index in range(0, self.__slack_variable_count):
            print(('s' + repr(__index + 1)).rjust(6), end=' ')
        print("\nCurrent Solution: ", end='')
        for __index in range(0, self.__ncols - 1):
            if __index in self.__basic_variables:
                __element = \
                        self.__simplex_tableau[self.__basic_variables.index(__index)]\
                        [self.__ncols - 1]
                print(repr(math.ceil(__element * 100) / 100).rjust(6), end=' ')
            else:
                print(repr(0.0).rjust(6), end=' ')

        __element = self.__simplex_tableau[self.__nrows - 1][self.__ncols - 1]
        print("    Z-value: " + repr(math.ceil(__element * 100) / 100) + "\n")

#------------------------------------------------------------------------------

    # The pivot element is located where the column of the entering variable
    # and the row of the leaving variable intersect.
    def __find_pivot_element(self):
        """Returns the row and column of the pivot element."""

        # When locating the entering variable, we only need to focus on the
        # elements in the last row that don't correspond to the z-value
        __solution_row = (self.__simplex_tableau[self.__nrows - 1])[0:-1]
        # Find the smallest number in the last row previously isolated to
        # find the pivot column (entering variable)
        __pivot_column_index = __solution_row.index(min(__solution_row))

        # Calculate all ratios between the basic variables and the elements
        # in the pivot column
        __temp_column = []
        for __row_index in range(0, self.__nrows - 1):
            # If an element in the pivot column is zero, then we can't
            # perform the ratio test.  As a result, we simply associate this
            # value with a negative 1 and then proceed as normal.
            if (self.__simplex_tableau[__row_index][__pivot_column_index] == 0):
                __ratio = -1
            else:
                __ratio = self.__simplex_tableau[__row_index][self.__ncols - 1] /\
                        self.__simplex_tableau[__row_index][__pivot_column_index]
            __temp_column.append(__ratio)
        # Find the smallest positive ratio from the previously calculated
        # ratios to find the pivot row (leaving variable)
        __pivot_row_index = \
                __temp_column.index(min([n for n in __temp_column if n > 0]))

        return __pivot_row_index, __pivot_column_index

#------------------------------------------------------------------------------

    def __apply_gj_elimination(self, row, column):
        """Performs Gauss Jordan Elimination on the simplex tableau relative
        to the element located at the row and column parameters supplied."""

        __pivot_element = self.__simplex_tableau[row][column]

        # Normalize the row containing the pivot element relative to the
        # pivot element itself
        for __column_index in range(0, len(self.__simplex_tableau[row])):
            self.__simplex_tableau[row][__column_index] = \
                    self.__simplex_tableau[row][__column_index] / __pivot_element

        # Perform the necessary row operations to make all elements in the
        # pivot column zero except the pivot element
        for __row_index in range(0, self.__nrows):
            __pivot_row = copy.deepcopy(self.__simplex_tableau[row])
            if __row_index != row:
                __multiplier = -1 * self.__simplex_tableau[__row_index][column]
                for __column_index in range(0, len(__pivot_row)):
                    __pivot_row[__column_index] = \
                            __pivot_row[__column_index] * __multiplier
                for __pivot_column_index in range(0, len(__pivot_row)):
                    self.__simplex_tableau[__row_index][__pivot_column_index] = \
                        self.__simplex_tableau[__row_index][__pivot_column_index] + \
                        __pivot_row[__pivot_column_index]

#------------------------------------------------------------------------------

    # Check if an optimal solution is found by verifying that there are no
    # negative variables in the solution row.
    def __optimal_solution_found(self):
        __optimal_solution = False

        for __element in self.__simplex_tableau[self.__nrows - 1]:
            if __element < 0:
                __optimal_solution = False
                break
            else:
                __optimal_solution = True

        return __optimal_solution

#------------------------------------------------------------------------------

    def calculate_optimal_solution(self):
        self.__display_simplex_tableau()

        while 1:
            if (self.__optimal_solution_found() == False):
                __row, __column = self.__find_pivot_element()

                self.__apply_gj_elimination(__row, __column)

                self.__basic_variables[__row] = __column

                self.__display_simplex_tableau()
            else:
                break

#------------------------------------------------------------------------------
