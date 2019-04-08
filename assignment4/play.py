
import pexpect, board_util, simple_board, gtp_connection

player1='gomoku4/Gomoku4.py'
player2='flat_mc_player/Gomoku3.py'

win1=0
win2=0
numTimeout=0
draw=0
timeout = 5

def getMove(p,color):
    p.sendline('genmove '+color)
    p.expect([pexpect.TIMEOUT,'= [A-Z][0-9]','= resign','= pass'])
    if p.after==pexpect.TIMEOUT:
        return 'timeout'
    return p.after.decode("utf-8")[2:]

def playMove(p,color,move):
    p.sendline('play '+color+' '+move)

def setupPlayer(p):
    p.sendline('boardsize 7')
    p.sendline('clear_board')
    p.sendline('timelimit {}'.format(timeout))

def playSingleGame(alternative=False):
    if not alternative:
        p1=pexpect.spawn('python3 '+player1,timeout=timeout+1)
        p2=pexpect.spawn('python3 '+player2,timeout=timeout+1)
    else:
        p1=pexpect.spawn('python3 '+player2,timeout=timeout+1)
        p2=pexpect.spawn('python3 '+player1,timeout=timeout+1)

    ob=pexpect.spawn('python3 flat_mc_player/Gomoku3.py')
    setupPlayer(p1)
    setupPlayer(p2)
    result=None
    numTimeout=0
    sw=0

    board = simple_board.SimpleGoBoard(7)

    while 1:
        if sw==0:
            move=getMove(p1,'b')
            assert(move!='pass')
            if move=='resign':
                result=2
                break
            elif move=='timeout':
                result=2
                break
            playMove(p2,'b',move)
            playMove(ob,'b',move)

            move = gtp_connection.move_to_coord(move, 7)
            move = board.pt(move[0], move[1])
            board.play_move_gomoku(move, 1)
            
        else:
            move=getMove(p2,'w')
            assert(move!='pass')
            if move=='resign':
                result=1
                break
            elif move=='timeout':
                result=1
                break
            playMove(p1,'w',move)
            playMove(ob,'w',move)

            move = gtp_connection.move_to_coord(move, 7)
            move = board.pt(move[0], move[1])
            board.play_move_gomoku(move, 2)
            

        sw=1-sw
        print(move)
        print(board_util.GoBoardUtil.get_twoD_board(board))


        ob.sendline('gogui-rules_final_result')
        ob.expect(['= black','= white','= draw','= unknown'])
        status=ob.after.decode("utf-8")[2:]


        if status=='black':
            result=1
            break
        elif status=='white':
            result=2
            break
        elif status=='draw':
            result=0
            break
        else:
            assert(status=='unknown')
    print(status)

    return result,numTimeout

def playGames(numGame=5):
    global win1,win2,draw,numTimeout
    for i in range(0,numGame):
        if(i<numGame/2):
            alter=False
        else:
            alter=True
        result,timeout=playSingleGame(alternative=alter)

        
        if timeout>0:
            numTimeout+=1
        else:
            if result==0:
                draw+=1
            else:
                if result==1 and alter==False or result==2 and alter==True:
                    win1+=1
                else:
                    assert(result==1 and alter==True or result==2 and alter==False)
                    win2+=1

def outputResult():
    print('player1 win',win1,'player2 win',win2,'draw',draw)

playGames()
outputResult()
