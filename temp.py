import random
import sys

from PyQt5.QtCore import pyqtSignal, QBasicTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QFrame, QApplication, QLabel, QLayout, QWidget


# creating game window
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # creating a status bar to show result
        self.statusbar = self.statusBar()

        # creating a board object
        self.board = Board(self)

        # adding border to the status bar
        self.statusbar.setStyleSheet("border : 2px outset; border-radius:10px;")
        self.statusbar.setSizeGripEnabled(False)

        # calling showMessage method when signal received by board
        self.board.msg2statusbar[str].connect(self.statusbar.showMessage)

        # adding board as a central widget
        self.setCentralWidget(self.board)

        # setting title to the window
        self.setWindowTitle("Snake")

        # setting geometry to the window
        self.setGeometry(560, 240, 800, 600)

        # starting the board object
        self.board.start()

        # showing the main window
        self.show()


# creating a board class that inherits QFrame
class Board(QFrame):
    # creating signal object
    msg2statusbar = pyqtSignal(str)

    # speed of the snake
    SPEED = 50

    # block width and height
    WIDTHBLOCKS = 30
    HEIGHTBLOCKS = 20

    # constructor
    def __init__(self, parent):
        super(Board, self).__init__(parent)

        # creating a timer
        self.timer = QBasicTimer()

        # snake
        self.snake = [[5, 10], [5, 11]]

        # current x head
        self.current_x_head = self.snake[0][0]
        # current y head
        self.current_y_head = self.snake[0][1]

        # food list
        self.food = []

        # growing is false
        self.grow_snake = False

        # board list
        self.board = []

        # direction
        self.direction = 1

        # called drop food method
        self.drop_food()
        self.drop_food()

        # setting focus
        self.setFocusPolicy(Qt.StrongFocus)

        self.is_on = True

        self.widget = QWidget()

    # square width
    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHBLOCKS

    # square height
    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTBLOCKS

    # start method
    def start(self):
        # msg for status bar
        # score = current len - 2
        self.msg2statusbar.emit(str(len(self.snake) - 2))

        # starting timer
        self.timer.start(Board.SPEED, self)

        self.setStyleSheet("background-color: 0xE3F18D")

        # snake
        self.snake = [[5, 10], [5, 11]]

        # current x head
        self.current_x_head = self.snake[0][0]
        # current y head
        self.current_y_head = self.snake[0][1]

        # food list
        self.food = []

        # growing is false
        self.grow_snake = False

        # board list
        self.board = []

        # direction
        self.direction = 1

        # called drop food method
        self.drop_food()
        self.drop_food()

    # paint event
    def paintEvent(self, event):

        # creating painter object
        painter = QPainter(self)

        # getting rectangle
        rect = self.contentsRect()

        # board top
        boardtop = rect.bottom() - Board.HEIGHTBLOCKS * self.square_height()

        # drawing snake
        for pos in self.snake:
            self.draw_snake(painter, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())

        for pos in self.food:
            self.draw_food(painter, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())

    # drawing square
    def draw_snake(self, painter, x, y):
        # color
        color = QColor(0x228B22)

        # painting rectangle
        painter.fillRect(x + 1, y + 1, self.square_width() - 2, self.square_height() - 2, color)

    def draw_food(self, painter, x, y):
        # color
        color = QColor(0xBE2576)

        # painting rectangle
        painter.fillRect(x + 1, y + 1, self.square_width() - 2, self.square_height() - 2, color)

    def keyPressEvent(self, event):
        # getting key pressed
        key = event.key()

        # if left key pressed
        if key == Qt.Key_Left:
            # if direction is not right
            if self.snake[0][0] - self.snake[1][0] != 1:
                # set direction to right
                self.direction = 1

        # if right key pressed
        elif key == Qt.Key_Right:
            # if direction is not left
            if self.snake[0][0] - self.snake[1][0] != -1:
                # set direction to right
                self.direction = 2

        # if down key pressed
        elif key == Qt.Key_Down:
            # if direction is not up
            if self.snake[0][1] - self.snake[1][1] != -1:
                # set direction to down
                self.direction = 3

        # if up key pressed
        elif key == Qt.Key_Up:
            # if direction is not down
            if self.snake[0][1] - self.snake[1][1] != 1:
                # set direction to up
                self.direction = 4

        elif key == Qt.Key_Return and (not self.is_on):
            self.start()

    # move snake
    def move_snake(self):
        # if direction is left change its position
        if self.direction == 1:
            self.current_x_head, self.current_y_head = self.current_x_head - 1, self.current_y_head

            # if it goes beyond left wall
            if self.current_x_head < 0:
                self.current_x_head = Board.WIDTHBLOCKS - 1

        # right
        if self.direction == 2:
            self.current_x_head, self.current_y_head = self.current_x_head + 1, self.current_y_head

            # if it goes beyond right wall
            if self.current_x_head >= Board.WIDTHBLOCKS:
                self.current_x_head = 0

        # down
        if self.direction == 3:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head + 1

            # if it goes beyond down wall
            if self.current_y_head >= Board.HEIGHTBLOCKS:
                self.current_y_head = 0

        # up
        if self.direction == 4:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head - 1

            # if it goes beyond up wall
            if self.current_y_head < 0:
                self.current_y_head = Board.HEIGHTBLOCKS - 1

        # changing head position
        head = [self.current_x_head, self.current_y_head]
        # insert head in snake list
        self.snake.insert(0, head)

        # if snake grow is False
        if not self.grow_snake:
            # pop the last element
            self.snake.pop()
        else:
            # show msg in status bar
            self.msg2statusbar.emit(str(len(self.snake) - 2))
            # make grow_snake to false
            self.grow_snake = False

    def timerEvent(self, event):
        # checking timer id
        if event.timerId() == self.timer.timerId():
            # call move snake method
            self.move_snake()
            # call food collision method
            self.is_food_collision()
            # call is suicide method
            self.is_suicide()
            # update()
            self.update()

    def is_suicide(self):
        if self.snake[0] in self.snake[1:]:
            self.msg2statusbar.emit(str("Game Ended -- Final Score: ") + str(len(self.snake) - 2))
            self.setStyleSheet("background-color: black;")
            self.timer.stop()
            self.is_on = False
            self.update()
            # form = Ui_Form()
            # form.setupUi(self.widget)
            # form.lineEdit.setText(str(len(self.snake) - 2))
            #self.widget.show()

    def is_food_collision(self):
        for pos in self.food:
            if pos == self.snake[0]:
                self.food.remove(pos)
                self.drop_food()
                self.grow_snake = True

    def drop_food(self):
        x = random.randint(0, self.WIDTHBLOCKS - 1)
        y = random.randint(0, self.HEIGHTBLOCKS - 1)
        while [x, y] in self.snake:
            x = random.randint(0, self.WIDTHBLOCKS - 1)
            y = random.randint(0, self.HEIGHTBLOCKS - 1)

        self.food.append([x, y])
        print([x, y])


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon(r"snake-logo.png"))
    window = Window()
    sys.exit(app.exec_())
