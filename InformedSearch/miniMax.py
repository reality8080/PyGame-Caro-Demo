from checkWin import checkWin
from isFullBoard import isBoardFull
from MarkSquare import markSquare

def evaluateBoard(checkBoard,boardRows,boardCols):
    score = 0
    for row in range(boardRows):
        for col in range(boardCols):
            if checkBoard[row][col] == 2:  # AI
                score += 10
            elif checkBoard[row][col] == 1:  # Người chơi
                score -= 10
    if checkWin( checkBoard,2):
        return 1000
    elif checkWin( checkBoard,1):
        return -1000
    return score

#Thuat toan tim kiem toi uu MiniMax
maxDepth=4
def minimax(minimaxBoard, boardRows, boardCols, depth, isMaximizing,alpha,beta):
    score=evaluateBoard(minimaxBoard,boardRows,boardCols)
    if score==1000 or score == -1000 or isBoardFull(minimaxBoard, boardRows, boardCols) or depth>=maxDepth:
        return score
    if isMaximizing:
        bestScore = -float('inf')
        # Lặp qua tất cả các ô
        for row in range(boardRows):
            for col in range(boardCols):
                if minimaxBoard[row][col] == 0:
                    minimaxBoard[row][col] = 2
                    bestScore=max(bestScore,minimax(minimaxBoard,boardRows, boardCols, depth+1, False,alpha,beta))
                    # Gọi đệ quy và lưu điểm với lớn nhất cho AI
                    minimaxBoard[row][col] = 0
                    alpha = max(alpha, bestScore)
                    if beta <=alpha:
                        break
        return bestScore
    else:
        bestScore = float('inf')
        for row in range(boardRows):
            for col in range(boardCols):
                if minimaxBoard[row][col] == 0:
                    minimaxBoard[row][col] = 1
                    bestScore = min(bestScore, minimax(minimaxBoard, boardRows, boardCols, depth+1,True,alpha,beta))                    
                    minimaxBoard[row][col] = 0
                    beta=min(beta,bestScore)
                    if beta <=alpha:
                        break
        return bestScore
# Duyệt qua từng ô và suy diễn ra ô có điểm số cao nhất
def bestMoveMiniMax(board, boardRows, boardCols):
    bestScore=-float('inf')
    move=(-1,-1)
    for row in range (boardRows):
        for col in range(boardCols):
            if board[row][col]==0:
                # Thử đánh
                board[row][col]=2
                # Lấy điểm số lớn nhất
                score= minimax(board,boardRows, boardCols, 0,False,-float('inf'),float('inf'))
                board[row][col]=0
                # kiểm tra điểm số cao nhất
                if score>bestScore:
                    bestScore=score
                    move=(row,col)
    if move != (-1,-1):
        markSquare(board,move[0], move[1],player=2)
        return True
    return False