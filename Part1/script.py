#420 Sudoku puzzles solved! Congratulations!! Here is your flag: flag{f34r1355_5ud0ku_c0nqu3r0r}
import pexpect 
import copy 
child = pexpect.spawn('./sudoku')
flag = ''

def read_board(puzzle_state):
    puzzle_state = puzzle_state.replace(".","0")
    puzzle_state = puzzle_state.splitlines()
    board = []
    print(len(puzzle_state))
    for i in range(len(puzzle_state)):
        print(f"line #{i}", puzzle_state[i])
    #rows = puzzle_state[2:5] + puzzle_state[6:9] + puzzle_state[10:13]
    rows = [line for line in puzzle_state if '|' in line]
    for i in range(len(rows)):
        row_list = rows[i].split()
        row_list = row_list[1:4] + row_list[5:8] + row_list[9:12]
        
        #if i <9:
        board.append([int(num) for num in row_list])
    #print(rows[0][2])
    return board
    #for j in range(9):
        #print(board[j][0])

def find_empty_location(board, l):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                l[0] = row
                l[1] = col
                return True
    return False

def used_in_row(board, row, num):
    return any(board[row][col] == num for col in range(9))

def used_in_col(board, col, num):
    return any(board[row][col] == num for row in range(9))

def used_in_box(board, box_start_row, box_start_col, num):
    return any(board[i][j] == num for i in range(box_start_row, box_start_row + 3) for j in range(box_start_col, box_start_col + 3))

def check_location_is_safe(board, row, col, num):
    return (not used_in_row(board, row, num) and
            not used_in_col(board, col, num) and
            not used_in_box(board, row - row % 3, col - col % 3, num))

def solve_sudoku(board):
    l = [0, 0]
    if not find_empty_location(board, l):
        return True
    row, col = l[0], l[1]
    for num in range(1, 10):
        if check_location_is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def num_empty_cells(board):
    empty_count = 0
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                empty_count +=1
    return empty_count
         
def looping(puzzle_state, i):
    print('i puzzle',i)
    if i >= 420:
        solved = "solved 420 puzzles"
        return solved
    board = read_board(puzzle_state)
    real_board = copy.deepcopy(board)
    print("Input Board:")
    for row in real_board:
        print(' '.join(map(str,row)))
    if solve_sudoku(real_board):
        solved_board = [row for row in real_board]
        print("solved sudoku:")
        for row in solved_board:
            print(" ".join(map(str, row))) 
    print("real puzzle")
    for row in board:
        print(' '.join(map(str,row)))
    del real_board

    for row in range(9):
        for col in range(9):
                         #child.expect('Enter row (0-8), column (0-8), and number (1-9) to fill (space-separated):', timeout=5)
                if  board[row][col] == 0:
                    move = f"{row} {col} {solved_board[row][col]}"
                    try:
                    #child.expect('Enter row \\(0-8\\), column \\(0-8\\), and number \\(1-9\\) to fill \\(space-separated\\):', timeout=10)
                        child.sendline(move)
                        print(f"moved {move}")
                        print("Num Empty Cells:")
                        print(num_empty_cells(board))

                            #print(f"Board after move {move}:")
                        if num_empty_cells(board) > 1:
                        #print('Num Empty Cells',num_empty_cells(real_board))
                        #child.expect('Enter row \\(0-8\\), column \\(0-8\\), and number \\(1-9\\) to fill \\(space-separated\\):', timeout=10)
                        #child.sendline(move)
                        #print(f"moved {move}")
                            del board
                            child.expect('Sudoku Board:', timeout=10)
                            child.expect('Enter row \\(0-8\\), column \\(0-8\\), and number \\(1-9\\) to fill \\(space-separated\\):', timeout=10)
                            new_puzzle_state = child.before.decode()
                            board = read_board(new_puzzle_state)
                        else:
                        #print('Num Empty Cells',num_empty_cells(real_board))
                        #child.expect('Enter row \\(0-8\\), column \\(0-8\\), and number \\(1-9\\) to fill \\(space-separated\\):', timeout=10)
                        #child.sendline(move)
                        #print(f"moved {move}")
                            del solved_board
                            del board
                            pattern = f'Congratulations! Sudoku #{i+1} solved!'
                            child.expect(pattern, timeout=10) 
                            child.expect('Enter row \\(0-8\\), column \\(0-8\\), and number \\(1-9\\) to fill \\(space-separated\\):', timeout=10)
                            new_puzzle_state = child.before.decode()
                        #new_board = read_board(new_puzzle_state)
                            #del puzzle_state
                            looping(new_puzzle_state, i+1)

                    except pexpect.TIMEOUT:
                        print(f"Timeout after sending move: {move}")
                else:
                    continue
            
if __name__ == '__main__':
    try:
        child.expect('Here is your Puzzle:', timeout=10)
        child.expect('Enter row \\(0-8\\), column \\(0-8\\), and number \\(1-9\\) to fill \\(space-separated\\):', timeout=10)
        puzzle_state = child.before.decode()
        #board = read_board(puzzle_state)
        looping(puzzle_state, 0)
    except pexpect.TIMEOUT:
        print("Timeout waiting for intial puzzle")
    finally:
        child.close()