from model.square import *


class chessboard:
    """Tạo bàn cờ từ những ô cờ"""
    sell = []

    def __init__(self) -> None:
        for i in range(0, 20):
            line = []
            for j in range(0, 20):
                x = 15 + j*30
                y = 15 + i*30
                line.append(square(x, y, 30))
            self.sell.append(line)

    def drawing(self, csv):
        """ chạy vòng lặp, tạo 20x20 ô cờ từ class ô cờ"""
        for i in range(0, 20):
            for j in range(0, 20):
                self.sell[i][j].drawing(csv)

    def setCell(self, csv, i, j, player):
        """ Đánh dấu là X hoặc O"""
        if i >= 0 and i < 20 and j >= 0 and j < 20:
            self.sell[i][j].sign(csv, player)

    def markCell(self, csv, i, j):
        """ Tô vàng ô cờ"""
        if i >= 0 and i < 20 and j >= 0 and j < 20:
            self.sell[i][j].mark(csv)

    def handleClick(self, event, csv, player):
        """ Xử lý event click bàn cờ"""
        i = (event.y - 15) // 30
        j = (event.x - 15) // 30
        self.setCell(csv, i, j, player)

    def clear(self, csv):
        """ dọn dẹp bàn cờ"""
        csv.delete('all')
        self.drawing(csv)