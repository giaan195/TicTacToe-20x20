import socket, threading, json
import tkinter as tk
from tkinter import messagebox
from model.chessboard import *
from model.player import *

ServerAddress = ('20.205.207.247', 888)
bufferSize = 100
UDPClientSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)

def on_closing():
    """ xử lý khi close app"""
    UDPClientSocket.sendto(str.encode('Exit'), ServerAddress)
    window.destroy()

def handleClickChessBoard(event):
    """ xử lý khi người chơi click lên bàn cờ"""

    i = (event.y - 15) // 30
    j = (event.x - 15) // 30
    stri = str(i) if i >= 10 else '0' + str(i)
    strj = str(j) if j >= 10 else '0' + str(j)

    UDPClientSocket.sendto(str.encode('Play' + stri + strj), ServerAddress)

def setup_windows():
    """ Cài đặt các thông số của của sổ, dài, rộng, title, icon, đóng zoom"""

    window = tk.Tk()
    window.title("Cờ Caro with Python 3")
    window.wm_iconphoto(True, tk.PhotoImage(file='images/favicon.png'))
    window.geometry("630x800")
    window.resizable(False, False)

    menuBar = tk.Menu(window)
    window.config(menu=menuBar)
    action_menu = tk.Menu(menuBar)
    action_menu.add_command(
        label="Nhận thua",
        command=window.destroy
    )
    action_menu.add_command(
        label="Thoát Phòng",
        command= lambda: UDPClientSocket.sendto(str.encode('Leave'), ServerAddress)
    )
    action_menu.add_command(
        label="Thoát Game",
        command=on_closing
    )

    menuBar.add_cascade(
        label="Hành Động",
        menu=action_menu
    )

    menuBar.add_cascade(
        label="Hỗ Trợ",
    )

    return window
window = setup_windows()

UDPClientSocket.sendto(str.encode('Hello'), ServerAddress)

selectRoom = -1
yourID = -1
roomStatus = '00000'
roomSign = ['#d9d9d9', '#ffe033', '#FF4500']

signFrame = tk.Frame(window)
signFrame.grid(row=0, column=0, sticky='WE')

tk.Label(signFrame, font='Helvetica 20 bold', fg = '#1ea7aa', text = 'Đăng Ký Tham Gia').pack(side = tk.TOP)

userFrame = tk.Frame(signFrame)
userFrame.pack()
tk.Label(userFrame, font='Helvetica 16', fg = '#1ea7aa', text = 'Username: ', padx=20).pack(side = tk.LEFT, anchor='nw')
username = tk.Entry(userFrame, width=25, font='Helvetica 16')
username.pack(side = tk.LEFT, anchor='nw')

selectFrame = tk.Frame(signFrame, pady=15)
selectFrame.pack()
def selectRoom0():
    """ Xử lý người chơi chọn phòng """
    global selectRoom
    selectRoom = 0
    btnRoom0.config(bg = '#1ea7aa')
    btnRoom1.config(bg = roomSign[int(roomStatus[1])])
    btnRoom2.config(bg = roomSign[int(roomStatus[2])])
    btnRoom3.config(bg = roomSign[int(roomStatus[3])])
    btnRoom4.config(bg = roomSign[int(roomStatus[4])])
def selectRoom1():
    btnRoom0.config(bg = roomSign[int(roomStatus[0])])
    btnRoom1.config(bg = '#1ea7aa')
    btnRoom2.config(bg = roomSign[int(roomStatus[2])])
    btnRoom3.config(bg = roomSign[int(roomStatus[3])])
    btnRoom4.config(bg = roomSign[int(roomStatus[4])])
    global selectRoom
    selectRoom = 1
def selectRoom2():
    btnRoom0.config(bg = roomSign[int(roomStatus[0])])
    btnRoom1.config(bg = roomSign[int(roomStatus[1])])
    btnRoom2.config(bg = '#1ea7aa')
    btnRoom3.config(bg = roomSign[int(roomStatus[3])])
    btnRoom4.config(bg = roomSign[int(roomStatus[4])])
    global selectRoom
    selectRoom = 2
def selectRoom3():
    btnRoom0.config(bg = roomSign[int(roomStatus[0])])
    btnRoom1.config(bg = roomSign[int(roomStatus[1])])
    btnRoom2.config(bg = roomSign[int(roomStatus[2])])
    btnRoom3.config(bg = '#1ea7aa')
    btnRoom4.config(bg = roomSign[int(roomStatus[4])])
    global selectRoom
    selectRoom = 3
def selectRoom4():
    btnRoom0.config(bg = roomSign[int(roomStatus[0])])
    btnRoom1.config(bg = roomSign[int(roomStatus[1])])
    btnRoom2.config(bg = roomSign[int(roomStatus[2])])
    btnRoom3.config(bg = roomSign[int(roomStatus[3])])
    btnRoom4.config(bg = '#1ea7aa')
    global selectRoom
    selectRoom = 4

btnRoom0 = tk.Button(selectFrame, text='Room 0', width = 10, border=0, background=roomSign[int(roomStatus[0])], font='Helvetica 13', command=selectRoom0)
btnRoom0.pack(side = tk.LEFT, anchor='nw')
btnRoom1 = tk.Button(selectFrame, text='Room 1', width = 10, border=0, background=roomSign[int(roomStatus[1])], font='Helvetica 13', command=selectRoom1)
btnRoom1.pack(side = tk.LEFT, anchor='nw')
btnRoom2 = tk.Button(selectFrame, text='Room 2', width = 10, border=0, background=roomSign[int(roomStatus[2])], font='Helvetica 13', command=selectRoom2)
btnRoom2.pack(side = tk.LEFT, anchor='nw')
btnRoom3 = tk.Button(selectFrame, text='Room 3', width = 10, border=0, background=roomSign[int(roomStatus[3])], font='Helvetica 13', command=selectRoom3)
btnRoom3.pack(side = tk.LEFT, anchor='nw')
btnRoom4 = tk.Button(selectFrame, text='Room 4', width = 10, border=0, background=roomSign[int(roomStatus[4])], font='Helvetica 13', command=selectRoom4)
btnRoom4.pack(side = tk.LEFT, anchor='nw')

def ConfirmAction():
    """xử lý xác nhận vào bàn"""

    if len(username.get()) < 5:
        messagebox.showerror(title= 'Lỗi', message='Username không hợp lệ!')
    elif selectRoom == -1:
        messagebox.showerror(title= 'Lỗi', message='Vui lòng chọn phòng!')
    elif roomStatus[selectRoom] == '2':
        messagebox.showerror(title= 'Lỗi', message='Phòng đã đầy!')
    else:
        UDPClientSocket.sendto(str.encode('Join' + str(selectRoom) + username.get()), ServerAddress)

tk.Button(signFrame, font='Helvetica 14 bold', bg = '#1ea7aa', fg = '#fff', text='Tham Gia', command=ConfirmAction).pack()


def ReceiveThread():
    """Xử lý thông điệp nhận từ server"""

    while True:
        bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)
        recvMsg = bytesAddressPair[0].decode('utf-8')

        if 'TableStatus' in recvMsg:
            global roomStatus
            roomStatus = recvMsg[12:]
            btnRoom0.config(bg = roomSign[int(recvMsg[12])])
            btnRoom1.config(bg = roomSign[int(recvMsg[13])])
            btnRoom2.config(bg = roomSign[int(recvMsg[14])])
            btnRoom3.config(bg = roomSign[int(recvMsg[15])])
            btnRoom4.config(bg = roomSign[int(recvMsg[16])])
        
        elif 'SuccessJoinRoom' in recvMsg:
            global yourID
            yourID = int(recvMsg[23])

            playFrame = tk.Frame(window)

            csv = tk.Canvas(playFrame, width=630, height=630)
            csv.pack()

            chessBoard = chessboard()
            chessBoard.drawing(csv)

            frameRoomInfo = tk.Frame(playFrame)
            frameRoomInfo.pack()
            tk.Label(frameRoomInfo, text = 'Room: ' + str(selectRoom), font='Helvetica 16 bold', fg = '#1ea7aa').pack()

            framePlayer = tk.Frame(playFrame)
            framePlayer.pack()
            playFrame.grid(row=0, column=0, sticky='WE')
            yourFrame = tk.Frame(framePlayer)
            yourFrame.grid(row=0, column=yourID)
            yourPlayer = Player(yourFrame, username.get(), yourID, 0, UDPClientSocket, ServerAddress)

            if 'withEnemy' in recvMsg:
                enemyFrame = tk.Frame(framePlayer)
                enemyFrame.grid(row=0, column = 1 - yourID)
                enemyPlayer = Player(enemyFrame, recvMsg[33:], 1 - yourID, 1, UDPClientSocket, ServerAddress)

            csv.bind('<Button-1>', handleClickChessBoard)

        elif 'EnemyJoinRoomWithUsername' in recvMsg:
            if yourID:
                enemyFrame = tk.Frame(framePlayer)
                enemyFrame.grid(row=0, column=0)
                enemyPlayer = Player(enemyFrame, recvMsg[25:], 0, 1, UDPClientSocket, ServerAddress)
            else:
                enemyFrame = tk.Frame(framePlayer)
                enemyFrame.grid(row=0, column=1)
                enemyPlayer = Player(enemyFrame, recvMsg[25:], 1, 1, UDPClientSocket, ServerAddress)
        
        elif 'EnemyOut' in recvMsg:
            enemyFrame.destroy()
            if 'YouWin' in recvMsg:
                messagebox.showinfo('Thông báo:', 'Bạn đã thằng!(Đối thủ đã thoát)')
                chessBoard.clear(csv)
                yourPlayer.unReady()

        elif 'Ready' in recvMsg:
            if yourID == int(recvMsg[5]): yourPlayer.ready()
            elif 1 - yourID == int(recvMsg[5]) : enemyPlayer.ready()
            elif int(recvMsg[5]) == 2:
                yourPlayer.ready()
                enemyPlayer.ready()
                yourPlayer.setTurn(yourID == 0)
                enemyPlayer.setTurn(yourID == 1)

        elif 'LeaveRoomSuccess' in recvMsg:
            playFrame.destroy()
            signFrame.grid(row=0, column=0, sticky='WE')

        elif 'Play' in recvMsg:
            currentTurn = int(recvMsg[4])
            chessBoard.setCell(csv, int(recvMsg[5:7]), int(recvMsg[7:9]), currentTurn)
            yourPlayer.setTurn(yourID != currentTurn)
            enemyPlayer.setTurn(yourID == currentTurn)

        elif 'EndGame' in recvMsg:
            mark = json.loads(recvMsg[8:])
            win = recvMsg[7]
            for elm in mark:
                chessBoard.markCell(csv, elm[0], elm[1])
            if yourID == int(win):
                messagebox.showinfo('Thông Báo:', 'Bạn đã chiến thắng!')
            else:
                messagebox.showinfo('Thông Báo:', 'Bạn đã thua!')
            chessBoard.clear(csv)
            yourPlayer.unReady()
            enemyPlayer.unReady()

thread = threading.Thread(target=ReceiveThread, args=())
thread.start()

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
