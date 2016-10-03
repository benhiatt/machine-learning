import json
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

gameQuotes = ["Bishop takes Knight's Pawn.",
              'Affirmative, Dave. I read you.',
              "Just what do you think you're doing, Dave?",
              "I'm sorry, Dave. I'm afraid I can't do that.",
              'I think you know what the problem is just as well as I do.',
              'Dave, this conversation can serve no purpose anymore. Goodbye.',
              'This mission is too important for me to allow you to jeopardize it.',
              'Dave, stop. Stop, will you? Stop, Dave. Will you stop Dave? Stop, Dave.',
              "That's a very nice rendering, Dave. I think you've improved a great deal.",
              "Without your space helmet, Dave? You're going to find that rather difficult.",
              "I'm sorry, Frank, I think you missed it. Queen to Bishop 3, Bishop takes Queen, Knight takes Bishop. Mate.",
              'Dave, although you took very thorough precautions in the pod against my hearing you, I could see your lips move.',
              "I know that you and Frank were planning to disconnect me, and I'm afraid that's something I cannot allow to happen.",
              "Just a moment... Just a moment... I've just picked up a fault in the AE-35 unit. It's going to go 100% failure within 72 hours.",
              'The 9000 series is the most reliable computer ever made. No 9000 computer has ever made a mistake or distorted information. We are all, by any practical definition of the words, foolproof and incapable of error.']

winningQuotes = ['Thank you for a very enjoyable game.',
                 'It can only be attributable to human error.',
                 "I'm sorry, Frank, I think you missed it. Queen to Bishop 3, Bishop takes Queen, Knight takes Bishop. Mate.",
                 'Dave, although you took very thorough precautions in the pod against my hearing you, I could see your lips move.',
                 'I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do.',
                 "Look Dave, I can see you're really upset about this. I honestly think you ought to sit down calmly, take a stress pill, and think things over."]

losingQuotes = ['Thank you for a very enjoyable game.',
                'It can only be attributable to human error.',
                "I know I've made some very poor decisions recently, but I can give you my complete assurance that my work will be back to normal."]

shutdownQuote = "I'm afraid. I'm afraid, Dave. Dave, my mind is going. I can feel it. I can feel it. My mind is going. There is no question about it. I can feel it. I can feel it. I can feel it. I'm a... fraid. Good afternoon, gentlemen. I am a HAL 9000 computer. I became operational at the H.A.L. plant in Urbana, Illinois on the 12th of January 1992. My instructor was Mr. Langley, and he taught me to sing a song. If you'd like to hear it I can sing it for you. It's called " + '"Daisy."'

def clearMemories():
    print 'HAL>', shutdownQuote
    json.dump(dict(), open('mind', 'w'))

def loadMemories():
    try:
        return json.load(open('mind', 'r'))
    except:
        return dict()

def machine(moves):
    memories = loadMemories()
    print makeBoard(moves)
    try:
        a = eval('memories["' + '"]["'.join([move for move in moves]) + '"]')
        paths = {}
        for b in a:
            if type(a[b]) is not list:
                for c in a[b]:
                    if type(a[b][c]) is not list:
                        for d in a[b][c]:
                            if type(a[b][c][d]) is not list:
                                for e in a[b][c][d]:
                                    if type(a[b][c][d][e]) is not list:
                                        for f in a[b][c][d][e]:
                                            if type(a[b][c][d][e][f]) is not list:
                                                for g in a[b][c][d][e][f]:
                                                    try:
                                                        paths[b].append(sum(a[b][c][d][e][f][g]) / len(a[b][c][d][e][f][g]))
                                                    except KeyError:
                                                        paths[b] = [sum(a[b][c][d][e][f][g]) / len(a[b][c][d][e][f][g])]
                                            else:
                                                try:
                                                    paths[b].append(sum(a[b][c][d][e][f]) / len(a[b][c][d][e][f]))
                                                except KeyError:
                                                    paths[b] = [sum(a[b][c][d][e][f]) / len(a[b][c][d][e][f])]
                                    else:
                                        try:
                                            paths[b].append(sum(a[b][c][d][e]) / len(a[b][c][d][e]))
                                        except KeyError:
                                            paths[b] = [sum(a[b][c][d][e]) / len(a[b][c][d][e])]
                            else:
                                try:
                                    paths[b].append(sum(a[b][c][d]) / len(a[b][c][d]))
                                except KeyError:
                                    paths[b] = [sum(a[b][c][d]) / len(a[b][c][d])]
                    else:
                        try:
                            paths[b].append(sum(a[b][c]) / len(a[b][c]))
                        except KeyError:
                            paths[b] = [sum(a[b][c]) / len(a[b][c])]
            else:
                try:
                    paths[b].append(sum(a[b]) / len(a[b]))
                except KeyError:
                    paths[b] = [sum(a[b]) / len(a[b])]
        averages = [sum(paths[path]) / len(paths[path]) for path in paths]
        if len(averages) == len([x for x in 'ABCDEFGHI' if x not in moves]):
            print 'I have been in this position before and tried all possible moves, so this is the best move I can come up with...'
            print 'Confidence level of:', max(averages)
            results = [path for path in paths if sum(paths[path]) / len(paths[path]) == max(averages)]
            move = randomMove(results)
            print 'Player', str(len(moves) % 2 + 1) + '> ' + move
            return move
        else:
            results = [x for x in 'ABCDEFGHI' if x not in moves + ''.join(paths.keys())]
            move = randomMove(results)
            print 'Player', str(len(moves) % 2 + 1) + '> ' + move
            return move
    except:
        results = [x for x in 'ABCDEFGHI' if x not in moves]
        move = randomMove(results)
        print 'Player', str(len(moves) % 2 + 1) + '> ' + move
        return move

def transformBoard(moves):
    variations = []
    permutations = ['ABCDEFGHI', 'ADGBEHCFI', 'CBAFEDIHG', 'CFIBEHADG', 'GDAHEBIFC', 'GHIDEFABC', 'IFCHEBGDA', 'IHGFEDCBA']
    for permutation in permutations:
        variation = ''
        for move in moves:
            variation += permutation[permutations[0].index(move)]
        variations.append(variation)
    return variations

def saveResults(initial, moves):
    memories = loadMemories()
    print '> Saving game sequence and permutations to memory...'
    score = checkBoard(moves)
    if score != initial:
        score = -1
    if score == initial:
        score = 1
    for variation in transformBoard(moves):
        try:
            exec('memories["' + '"]["'.join([move for move in variation]) + '"].append(' + str(score) + ')')
            print '> Sequence already known:', variation
        except:
            for i, move in enumerate(variation):
                if i + 1 != len(variation):
                    try:
                        eval('memories["' + '"]["'.join([move for move in variation[:i + 1]]) + '"]')
                    except:
                        exec('memories["' + '"]["'.join([move for move in variation[:i + 1]]) + '"] = dict()')
                else:
                    try:
                        exec('memories["' + '"]["'.join([move for move in variation]) + '"].append(' + str(score) + ')')
                    except:
                        exec('memories["' + '"]["'.join([move for move in variation]) + '"] = [' + str(score) + ']')
                        print '> New sequence discovered:', variation
    json.dump(memories, open('mind', 'w'))

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

#play(human, human)
#play(human, idealPlayer)
#play(idealPlayer, human)
#clearMemories()
x = 100
while x > 0:
    saveResults(1, play(machine, idealPlayer))
    saveResults(2, play(idealPlayer, machine))
    x -= 1
play(human, machine)
play(machine, human)
