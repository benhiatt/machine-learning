import numpy as np
from random import randint

def splitMoves(moves):
    X, O = [], []
    for i, move in enumerate(moves):
        if i % 2 == 0:
            X.append(move)
        else:
            O.append(move)
    return X, O

def makeBoard(moves):
    board = '''     |     |     
 [A] | [B] | [C] 
_____|_____|_____
     |     |     
 [D] | [E] | [F] 
_____|_____|_____
     |     |     
 [G] | [H] | [I] 
     |     |     '''
    X, O = splitMoves(moves)
    for move in X:
        board = board.replace('[' + move + ']', ' X ')
    for move in O:
        board = board.replace('[' + move + ']', ' O ')
    return board

def containsWin(moves):
    if (('A' in moves and (('B' in moves and 'C' in moves) or ('E' in moves and 'I' in moves) or ('D' in moves and 'G' in moves))) or ('B' in moves and 'E' in moves and 'H' in moves) or ('C' in moves and (('E' in moves and 'G' in moves) or ('F' in moves and 'I' in moves))) or ('D' in moves and 'E' in moves and 'F' in moves) or ('G' in moves and 'H' in moves and 'I' in moves)):
        return True
    return False

def checkBoard(moves):
    if len(moves) < 5:
        return False
    X, O = splitMoves(moves)
    if containsWin(X):
        return 1
    if containsWin(O):
        return 2
    if len(moves) == 9:
        return 0
    return False

def human(moves):
    print makeBoard(moves)
    move = raw_input('Player ' + str(len(moves) % 2 + 1) + '> ').upper()
    while (move in moves) or (move not in 'ABCDEFGHI'):
        move = raw_input('Please try again, Player ' + str(len(moves) % 2 + 1) + '> ').upper()
    return move

def alphabeta(initial, moves, alpha, beta):
    winner = checkBoard(moves)
    if winner or len(moves) == 9:
        if winner == initial:
            return 1
        if winner != 0:
            return -1
        return 0
    player = (len(moves) % 2) + 1
    for move in [move for move in 'ABCDEFGHI' if move not in moves]:
        val = alphabeta(initial, moves + move, alpha, beta)
        if player == initial:
            if val > alpha:
                alpha = val
            if alpha >= beta:
                return beta
        else:
            if val < beta:
                beta = val
            if beta <= alpha:
                  return alpha
    if player == initial:
        return alpha
    else:
        return beta

def randomMove(moves):
    return moves[randint(0, len(moves) - 1)]

def idealPlayer(moves):
    corners = 'ACGI'
    center = 'E'
    sides = 'BDFH'
    print makeBoard(moves)
    if len(moves) == 0:
        move = randomMove(corners)
        print 'Player', str(len(moves) % 2 + 1) + '> ' + move
        return move
    a = -2
    choices = []
    for move in [move for move in 'ABCDEFGHI' if move not in moves]:
        val = alphabeta((len(moves) % 2) + 1, moves + move, -2, 2)
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    move = randomMove(choices)
    print 'Player', str(len(moves) % 2 + 1) + '> ' + move
    return move

def translateBoard(moves):
    board = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    X, O = splitMoves(moves)
    return [1 if pos in X else -1 if pos in O else 0 for pos in board]

def machine(moves):
    pass

def genExamplesSolutions(batchSize):
    board = 'ABCDEFGHI'
    examples = []
    while len(examples) < batchSize:
        example = []
        length = randint(0, 8)
        while len(example) < length:
            availible = [x for x in board if x not in example and not checkBoard(example + [x])]
            if len(availible) == 0:
                break
            move = randomMove(availible)
            example.append(move)
        examples.append(example)
    solutions = []
    for example in examples:
        solutions.append(idealPlayer(''.join(example)))
    solutions = [translateBoard(examples[i] + [solution]) for i, solution in enumerate(solutions)]
    examples = [translateBoard(example) for example in examples]
    return examples, solutions

def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

def train(examples, solutions):
    X = np.array(examples)            
    y = np.array(solutions)
    np.random.seed(1)
    syn0 = 2*np.random.random((9,9)) - 1
    syn1 = 2*np.random.random((9,9)) - 1
    for j in xrange(600000000):
        l0 = X
        l1 = nonlin(np.dot(l0,syn0))
        l2 = nonlin(np.dot(l1,syn1))
        l2_error = y - l2
        if (j% 10000) == 0:
            print "Error:" + str(np.mean(np.abs(l2_error)))
        l2_delta = l2_error*nonlin(l2,deriv=True)
        l1_error = l2_delta.dot(syn1.T)
        l1_delta = l1_error * nonlin(l1,deriv=True)
        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)
        return l2

def play(player1, player2):
    moves = ''
    winner = checkBoard(moves)
    while (not winner) and (len(moves) < 9):
        if len(moves) % 2 == 0:
            moves += player1(moves)
        else:
            moves += player2(moves)
        winner = checkBoard(moves)
    print makeBoard(moves)
    if winner:
        print 'Player', str(winner), 'wins!'
    else:
        print "It's a tie!!"
    return moves

examples, solutions = genExamplesSolutions(3)
print train(examples, solutions)
