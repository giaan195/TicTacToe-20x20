import socket, json, threading
from time import sleep


guest = []
room = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
userName = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
roomTurn = [0, 0, 0, 0, 0]
roomStatus = [-1, -1, -1, -1, -1]
chessBoard = []

def createBoard():
    """ Chạy vòng lặp, khởi tạo các ma trận bàn cờ 20x20 có giá trị -1 """
    for _ in range(0, 5):
        b = []
        for _ in range(0, 20):
            line = []
            for _ in range(0, 20):
                line.append(-1)
            b.append(line)
        chessBoard.append(b)    
def clearBoard(id):
    """ Chạy vòng lặp, đưa các giá trị ô cờ về -1 """

    b = []
    for _ in range(0, 20):
        line = []
        for _ in range(0, 20):
            line.append(-1)
        b.append(line)
    chessBoard[id] = b

createBoard()

ServerIP = '10.0.0.19'
ServerPort = 888
bufferSize = 100
# định ngĩa các thông số socket


CaroSocketServer = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
CaroSocketServer.bind((ServerIP, ServerPort))
print('CaroServer is running!')

def broadcastRoomInfo():
    """ Sẽ gởi thông tin trạng thái các bàn cờ (0,1,2 người chơi) hiện tại tới tất cả các người chơi trong guest """
    result = str(2 - room[0].count(0)) + str(2 - room[1].count(0)) + str(2 - room[2].count(0)) + str(2 - room[3].count(0)) + str(2 - room[4].count(0))
    result = str.encode('TableStatus:' + result)
    for player in guest:
        CaroSocketServer.sendto(result, player)

def checkGuest(player):
    """ kiểm tra nếu người chơi đã vào phòng thì xóa khỏi danh sách khách (guest) """
    if player in guest: return
    for elm in room: 
        if player in elm: return
    guest.append(player)
    result = str(2 - room[0].count(0)) + str(2 - room[1].count(0)) + str(2 - room[2].count(0)) + str(2 - room[3].count(0)) + str(2 - room[4].count(0))
    result = str.encode('TableStatus:' + result)
    CaroSocketServer.sendto(result, player)

def handleMsg(player, msg):
    """ Xử lý thông điệp gởi từ client """

    if 'Hello' in msg:
        CaroSocketServer.sendto(str.encode('Welcome to CaroSocketServer'), player)
        checkGuest(player)

    elif 'Join' in msg:
        if len(msg) < 10:
            CaroSocketServer.sendto(str.encode('Error: Invalid request!'), player)
            return 
        roomId = int(msg[4])
        username = msg[5:]
        if roomId > 4 or roomId < 0:
            CaroSocketServer.sendto(str.encode('Invalid room ID'), player)
            return
        if room[roomId].count(0) == 0:
            CaroSocketServer.sendto(str.encode('Full'), player)
            return
        if player not in room[roomId]:
            for i, elm in enumerate(room[roomId]):
                if elm == 0:
                    room[roomId][i] = player
                    userName[roomId][i] = username
                    enemy = room[roomId][1-i]
                    if enemy:
                        CaroSocketServer.sendto(str.encode('EnemyJoinRoomWithUsername' + username), enemy)
                        CaroSocketServer.sendto(str.encode('SuccessJoinRoom' + str(roomId) + 'WithUID' + str(i) + 'withEnemy' +  userName[roomId][1-i]), player)
                    else:
                        CaroSocketServer.sendto(str.encode('SuccessJoinRoom' + str(roomId) + 'WithUID' + str(i)), player)
                    break
        if player in guest: guest.remove(player)
        broadcastRoomInfo()
            
    elif msg == 'Leave':
        flagNotInRoom = True
        for i in [0, 1, 2, 3, 4]:
            for j in [0, 1]:
                if room[i][j] == player:
                    room[i][j] = 0
                    CaroSocketServer.sendto(str.encode('LeaveRoomSuccess'), player)
                    if player not in guest: guest.append(player)
                    broadcastRoomInfo()
                    enemy = room[i][1-j]
                    if enemy:
                        if roomStatus[i] == 2: CaroSocketServer.sendto(str.encode('EnemyOutYouWin'), enemy)
                        else: CaroSocketServer.sendto(str.encode('EnemyOut'), enemy)
                    roomStatus[i] = -1
                    clearBoard(i)
                    flagNotInRoom = False
                    break
        if flagNotInRoom: 
            CaroSocketServer.sendto(str.encode("Error:You haven't entered the room yet"), player)

    elif msg == 'Ready':
        flagNotInRoom = True
        for i in [0, 1, 2, 3, 4]:
            for j in [0, 1]:
                if room[i][j] == player:
                    enemy = room[i][1-j]
                    if enemy:
                        if roomStatus[i] == -1:
                            roomStatus[i] = j
                        if roomStatus[i] == 1-j:
                            roomStatus[i] = 2
                            roomTurn[i] = 0
                        CaroSocketServer.sendto(str.encode('Ready' + str(roomStatus[i])), enemy)
                        CaroSocketServer.sendto(str.encode('Ready' + str(roomStatus[i])), player)
                    else: return
                    flagNotInRoom = False
                    break
        if flagNotInRoom: 
            CaroSocketServer.sendto(str.encode("Error: You haven't entered the room yet"), player)

    elif msg == 'Exit':
        for i in [0, 1, 2, 3, 4]:
            for j in [0, 1]:
                if room[i][j] == player:
                    room[i][j] = 0
                    CaroSocketServer.sendto(str.encode('LeaveRoomSuccess'), player)
                    broadcastRoomInfo()
                    enemy = room[i][1-j]
                    if enemy:
                        if roomStatus[i] == 2: CaroSocketServer.sendto(str.encode('EnemyOutYouWin'), enemy)
                        else: CaroSocketServer.sendto(str.encode('EnemyOut'), enemy)
                    roomStatus[i] = -1
                    clearBoard(i)
                    flagNotInRoom = False
                    break
        if player in guest: guest.remove(player)

    elif 'Play' in msg:
        for i in [0, 1, 2, 3, 4]:
            for j in [0, 1]:
                if room[i][j] == player and roomStatus[i] == 2 and roomTurn[i] == j:
                    if(chessBoard[i][int(msg[4:6])][int(msg[6:8])] != -1): return
                    roomTurn[i] = 1 - j
                    CaroSocketServer.sendto(str.encode('Play' + str(j) + str(msg[4:6]) + str(msg[6:8]) + str(roomTurn[i])), player)
                    CaroSocketServer.sendto(str.encode('Play' + str(j) + str(msg[4:6]) + str(msg[6:8]) + str(roomTurn[i])), room[i][1-j])
                    chessBoard[i][int(msg[4:6])][int(msg[6:8])] = j

                    check = checkWin(i, j, int(msg[4:6]), int(msg[6:8]))
                    if check:
                        CaroSocketServer.sendto(str.encode('EndGame' + str(j) + json.dumps(check)), player)
                        CaroSocketServer.sendto(str.encode('EndGame' + str(j) + json.dumps(check)), room[i][1-j])
                        roomStatus[i] = -1
                        clearBoard(i)
                        roomTurn[i] = -1
                        

    else:
        CaroSocketServer.sendto(str.encode('Error: Invalid request!'), player)

def checkWin(board, player, x, y):
    """ Sẽ kiểm tra ngang, dọc, 2 đường chéo từ ngươc cờ mới đi, xem nếu có đủ 5 quân liên tiếp thì Win """

    result = [[x, y]]
    could = 1

    tmp = x
    while(tmp >= 0):
        if chessBoard[board][tmp-1][y] == player:
            result.append([tmp-1, y])
            could += 1
            tmp -= 1
        else: break
    tmp = x
    while(tmp <= 20):
        if chessBoard[board][tmp+1][y] == player:
            result.append([tmp+1, y])
            could += 1
            tmp += 1
        else: break
    if could >= 5: return result

    result = [[x, y]]
    could = 1
    tmp = y
    while(tmp >= 0):
        if chessBoard[board][x][tmp - 1] == player:
            result.append([x, tmp -1])
            could += 1
            tmp -= 1
        else: break
    tmp = y
    while(tmp <= 20):
        if chessBoard[board][x][tmp + 1] == player:
            result.append([x, tmp + 1])
            could += 1
            tmp += 1
        else: break
    if could >= 5: return result

    result = [[x, y]]
    could = 1
    tmpx, tmpy = x, y
    while(tmpx >= 0 and tmpy >= 0):
        if chessBoard[board][tmpx - 1][tmpy - 1] == player:
            result.append([tmpx - 1, tmpy - 1])
            could += 1
            tmpx -= 1
            tmpy -= 1
        else: break
    tmpx, tmpy = x, y
    while(tmpx <= 20 and tmpy <= 20):
        if chessBoard[board][tmpx + 1][tmpy + 1] == player:
            result.append([tmpx + 1, tmpy + 1])
            could += 1
            tmpx += 1
            tmpy += 1
        else: break
    if could >= 5: return result

    result = [[x, y]]
    could = 1
    tmpx, tmpy = x, y
    while(tmpx <= 20 and tmpy >= 0):
        if chessBoard[board][tmpx + 1][tmpy - 1] == player:
            result.append([tmpx + 1, tmpy - 1])
            could += 1
            tmpx += 1
            tmpy -= 1
        else: break
    tmpx, tmpy = x, y
    while(tmpx >= 0 and tmpy <= 20):
        if chessBoard[board][tmpx - 1][tmpy + 1] == player:
            result.append([tmpx - 1, tmpy + 1])
            could += 1
            tmpx -= 1
            tmpy += 1
        else: break
    if could >= 5: return result

    return False


def ReceiveThread():
    """ Xử lý đa luồng"""

    while True:
        bytesAddressPair = CaroSocketServer.recvfrom(bufferSize)
        recvMsg = bytesAddressPair[0].decode('utf-8')
        recvAddr = bytesAddressPair[1]

        handleMsg(recvAddr, recvMsg)
        print(recvAddr, recvMsg)

thread = threading.Thread(target=ReceiveThread, args=())
thread.start()

while True:
    sleep(10)
