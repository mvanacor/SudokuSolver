# JMJ
import sys

import os.path
from os import path

def readSudoku(filename):

    """ This function reads a sudoku puzzle from a file and returns the read sudoku
    A sudoku puzzle is a 9x9 grid where each value is between [0-9]. 0s are blanks
    
    Note: This function assumes a valid sudoku puzzle is being read.
    Use isValidSudoku to validate

    filename - sudoku puzzle file. 
    
    Valid sudoku file formats where x = [0-9]:
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx                                                                

        x,x,x,x,x,x,x,x,x
        x,x,x,x,x,x,x,x,x
        x,x,x,x,x,x,x,x,x
        x,x,x,x,x,x,x,x,x
        x,x,x,x,x,x,x,x,x
        x,x,x,x,x,x,x,x,x
        x,x,x,x,x,x,x,x,x
        x,x,x,x,x,x,x,x,x
        x,x,x,x,x,x,x,x,x

        [[x,x,x,x,x,x,x,x,x],
        [x,x,x,x,x,x,x,x,x],
        [x,x,x,x,x,x,x,x,x],
        [x,x,x,x,x,x,x,x,x],
        [x,x,x,x,x,x,x,x,x],
        [x,x,x,x,x,x,x,x,x],
        [x,x,x,x,x,x,x,x,x],
        [x,x,x,x,x,x,x,x,x],
        [x,x,x,x,x,x,x,x,x]]
    """

    # Create a blank sudoku board
    sudoku = []

    # Return an empty puzzle if the file doesn't exist
    if not path.exists(filename):
        print('File: {0} does not exists'.format(filename))
        return sudoku

    # Return an empty puzzle if the file provided isn't a file
    if not path.isfile(filename):
        print('Provided "File": {0} is not a readable file'.format(filename))
        return sudoku

    # Read the sudoku
    try:
        f = open(filename, 'r')

        lines = f.readlines()
        for line in lines:
            # Remove space, commas, brackets
            line = line.replace(' ', '').replace(',', '').replace('[', '').replace(']', '').replace('\n', '')
            row = []
            for c in line:                
                row.append(int(c))
            
            # Add the row to the sudoku matrix
            sudoku.append(row)

        f.close()
    except IOError:
        print('Failed to open file: ' + filename)

    return sudoku

def printSudoku(sudoku):

    """ This function prints a sudoku puzzle to the standard output 
    
    sudoku - 9x9 array
    
    """

    for r in range(9):
        print(sudoku[r])

def exportSudoku(sudoku, outputFilename = ''):

    """ This function exports a sudoku puzzle to a file 
    
    sudoku - 9x9 array
    outputFilename - filename of where to output the sudoku puzzle

    Format: 
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx
        xxxxxxxxx                                                                


    """

    if '' != outputFilename:
        f = open(outputFilename,'w')
        for r in sudoku:
            for n in r:
                f.write(str(n))
            f.write('\n')
    
        f.close()        


def isValidSudoku(sudoku):

    """ This function checks if the sudoku puzzle is a 9x9 square of numbers between [0-9]. 0s are blanks

    sudoku - 9x9 array

    Note: This function only checks if the sudoku is a 9x9 array of numbers between [0-9].
    It does not check if the sudoku puzzle is solvable.

    """

    # Check that the sudoku has 9 rows
    if 9 != len(sudoku):
        return False
    
    # Check that each row has 9 numbers
    for row in sudoku:
        if 9 != len(row):
            return False

        # Check that each number is between [1-9]
        for n in row:
            if 0 > n or 9 < n:
                return False

    return True

def isNumberPossible(sudoku, row, col, num):
    """ This function checks if a value (1-9) is possible at point (row,col).
    Returns true if the number is possible for the given row and column
    
    sudoku - 9x9 array
    row - row number [0-8]
    col - column number [0-8]
    num - number value [1-9]. This number cannot already exist in the row, column, or 3x3 square

    Pre: This function assumes that each parameter is valid
    """

    # Check the row
    r = sudoku[row]
    for n in r:        
        if num == n:
            return False

    # Check the column
    for r in range(9):
        if num == sudoku[r][col]:
            return False


    # Get the start of the 3x3 square quadrant (let hand corner)
    r0 = (row // 3) * 3
    c0 = (col // 3) * 3

    # Get the end of the 3x3 square quadrant (right hand corner)
    r1 = r0 + 3
    c1 = c0 + 3

    # Check the square
    for r in range(r0, r1):
        for c in range(c0, c1):
            if num == sudoku[r][c]:
                return False

    # All good, my man
    return True

def blankSpace(sudoku):
    """ This function checks if the sudoku puzzle has a blank (0) 
    
    sudoku - 9x9 array
    """

    # Iterate through the matrix to find a blank space (0)
    for r in sudoku:
        for n in r:
            if 0 == n:
                return True
    
    # No blank spaces in the matrix
    return False

def solve(sudoku):
    """ This function solves the matrix recursively. 
    Returns True if a solution exists 

    sudoku - 9x9 array
    """

    # Check for a blank in the puzzle
    if not blankSpace(sudoku):
        return True

    # Iterate through the matrix by row and col
    for r in range(9):
        for c in range(9):
            # We found a blank space. Try to put a number in it
            if 0 == sudoku[r][c]:
                for n in range(1, 10):
                    # Check if the number is possible by row, col, and square
                    if isNumberPossible(sudoku, r, c, n):
                        sudoku[r][c] = n
                        if not solve(sudoku):
                            # That number didn't fit down the line. We'll try the next one
                            sudoku[r][c] = 0
                # If we have any blank spaces left then we failed to find a solution
                return not blankSpace(sudoku)

def printUsage():
    """ This function prints the command line usage to the standard output """
    print('Usage: SudokuSolver.py <sudokufilename> [-p print] [-o <outputfilename>]')

def printHelp():
    pass

def main(argv):

    # TODO: Implement argparse for command line arguments

    # Fail if no parameters
    if 0 == len(argv) or '' == argv[0]:
        print('Sudoku file not provided')
        printUsage()
        return

    # Help command
    if '-h' == argv[0] or '-H' == argv[0]:
        printUsage()
        return

    # Sudoku Input file
    filename = argv[0]

    # Read and try to solve the sudoku
    sudoku = readSudoku(filename)

    # Failed to even read the sudoku
    if 0 == len(sudoku):
        return

    # We were able to read it, but didn't get a valid result
    if not isValidSudoku(sudoku):
        print('Was able to read the suodku puzzle, but the result was not a 9x9 sudoku of values between [0-9]')
        return 

    # Actually solve the sudoku
    solutionFound = solve(sudoku)

    # Print the sudoku
    if 0 < argv.count('-p') or 0 < argv.count('-P'):

        if solutionFound:
            print('Solution found')
        else:
            print('No solution')

        printSudoku(sudoku)

    # Do we want to output the puzzle? TODO: This better
    printOutput = False
    outputFilename = 'out.txt'
    for arg in argv:
        # We found the print flag. We hope the next parameter is the filename...
        if '-o' == arg:
            printOutput = True
        elif printOutput:
            # Hopefully this is a filename
            outputFilename = arg
    if printOutput:
        exportSudoku(sudoku, outputFilename)

if '__main__' == __name__:
    main(sys.argv[1:])

