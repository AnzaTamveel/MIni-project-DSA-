import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import Qt

class DisplayPage(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window properties
        self.setWindowTitle('Data Structures and Sorting Algorithms')
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(600, 600)  # Set minimum size to GIF's actual size
        self.setStyleSheet("""
            background-color: #2e2e2e;
            border-top: 2px solid #98c3bf;
            border-bottom: 2px solid #98c3bf;
        """)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Add a spacer item to push the content up a bit
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create and style the 'Sorting Algorithm' label
        sa_label = QLabel('Sorting Algorithms')
        sa_label.setFont(QFont('Helvetica Neue', 28, QFont.Bold))
        sa_label.setStyleSheet("color: #98c3bf; background-color: rgba(0, 0, 0, 0);")
        sa_label.setAlignment(Qt.AlignCenter)

        # Add the label to the layout
        layout.addWidget(sa_label)

        # Add another spacer item to push the content left a bit
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Create a QLabel for the GIF background
        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(0, 0, 600, 400)
        self.gif_label.setScaledContents(True)  # Make the GIF responsive

        # Load the GIF
        self.movie = QMovie('D:\\BSCS\\3rd Semester\\DSA\\MINI Project\\open.gif')
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        self.setLayout(layout)

        self.gif_label.lower()
        self.resizeEvent = self.on_resize

    def on_resize(self, event):
        self.gif_label.setGeometry(0, 0, self.width(), self.height())
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DisplayPage()
    window.show()
    sys.exit(app.exec_())
