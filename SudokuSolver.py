import sys

def readSudoku(filepath):

    """ This function reads a sudoku puzzle from a file """

    # Create a blank sudoku board
    sudoku = []

    f = open(filepath, 'r')

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

    return sudoku

def printSudoku(sudoku):

    """ This function prints a sudoku puzzle to the standard output """

    for r in range(9):
        print(sudoku[r])

def exportSudoku(sudoku, outputFilename = ''):

    """ This function exports a sudoku puzzle to a file """

    if '' != outputFilename:
        f = open(outputFilename,'w')
        for r in sudoku:
            for n in r:
                f.write(str(n))
            f.write('\n')
    
        f.close()        

def isNumberPossible(sudoku, row, col, num):
    """This function checks if a value (1-10) is possible at point (row,col)"""

    # Check the row
    r = sudoku[row]
    for n in r:        
        if num == n:
            return False

    # Check the column
    for r in range(0, 9):
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
    """ This function checks if the sudoku puzzle has a blank (0) """

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

def main(argv):

    # Sudoku Input file
    filename = ''
    if 0 != len(argv) and '' != argv[0]:
        filename = argv[0]
    else:
        filename = 'sudoku1.txt'

    # Read and try to solve the sudoku
    sudoku = readSudoku(filename)
    solutionFound = solve(sudoku)

    # Print the sudoku
    if 0 < argv.count('-p') or 0 < argv.count('-P'):

        if solutionFound:
            print('Solution found')
        else:
            print('No solution')

        printSudoku(sudoku)

    # Output to file
    exportSudoku(sudoku, 'out.txt')

if '__main__' == __name__:
    main(sys.argv[1:])