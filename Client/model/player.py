import tkinter as tk
from PIL import ImageTk, Image


class Player:
    """ Tạo đối tượng người chơi, nhập vào các thông số như: frame(ô ở giao diện), tên, id.. """
    time = '10m 0s'

    def __init__(self, frame, name, id, enemy, UDPClientSocket, ServerAddress) -> None:
        self.frame = frame
        self.name = name
        self.id = id
        self.avatar = ImageTk.PhotoImage(Image.open("images/player" + str(id) + ".png"))

        tk.Label(frame, image=self.avatar).grid(row=0, column = 1 - id, rowspan=3)
        self.lblName = tk.Label(frame, text=name, font='Helvetica 12 bold', width=15).grid(row=0, column = id, sticky="WSE")

        self.lblTime = tk.Label(frame, text=self.time, bg = '#C0C0C0')
        self.lblTime.grid(row=1, column=  id, sticky="WNE")
        self.btnReady = tk.Button(frame, text = 'Sẵn Sàng', bg='#1ea7aa', border=0, command = lambda: self.reading(UDPClientSocket, ServerAddress))
        self.btnReady.grid(row=2, column = id, sticky="WE")
        frame.config(highlightthickness=3)

        if enemy:
            self.btnReady.config(state="disabled", bg = '#3cdadd')

    def reading(self, UDPClientSocket, ServerAddress):
        """xử lý Sẵn sàng"""
        UDPClientSocket.sendto(str.encode('Ready'), ServerAddress)

    def ready(self):
        """chuyển đổi trạn thái thành đã Sẵn sàng"""
        self.btnReady.config(text='Đã Sẵn Sàng', state="disabled", bg = '#3cdadd')

    def unReady(self):
        """chuyển đổi trạn thái thành chưa Sẵn sàng"""
        self.btnReady.config(state="active", bg = '#1ea7aa', text='Sẵn Sàng')
        self.frame.config(highlightbackground = '#eeeeee')

    def setTurn(self, condition):
        """Chỉ dịnh lượt chơi"""
        if condition:
            self.frame.config(highlightbackground = '#3cdadd')
        else:
            self.frame.config(highlightbackground = '#eeeeee')

    def updateTime(self, time):
        m = time // 60
        s = time % 60
        self.time = m + 'm' + " " + s + 's'
        self.lblTime.config(text=self.time)