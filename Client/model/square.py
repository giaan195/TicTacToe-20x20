class square:
    """ Tạo đối tượng ô cờ, input là toạn độ đầu x,y và chiều dài cạnh e """

    x, y, e = 0, 0, 0

    def __init__(self, x, y, e):
        self.x = x
        self.y = y
        self.e = e

    def drawing(self, csv):
        """ Vẽ ô cờ"""
        self.cell = csv.create_rectangle(self.x, self.y, self.x + self.e, self.y + self.e, outline = 'black')

    def mark(self, csv):
        """ Tô vàng ô cờ """
        # csv.create_rectangle(self.x, self.y, self.x + self.e, self.y + self.e, outline = 'black', fill = '#ffff8c')
        csv.itemconfig(self.cell, fill = '#ffff8c')

    def sign(self, csv, player):
        """ Đánh dấu ô đã đi, X hoặc O """
        margin = self.e >> 2
        if player == 0:
            csv.create_oval(self.x + margin, self.y + margin, self.x + self.e - margin, self.y + self.e - margin, outline = '#e7585f', width = 4)
        elif player == 1:
            csv.create_line(self.x + margin, self.y + margin, self.x + self.e - margin, self.y + self.e - margin, fill = '#56c786', width = 4)
            csv.create_line(self.x  + self.e - margin, self.y + margin, self.x + margin, self.y + self.e - margin, fill = '#56c786', width = 4)
