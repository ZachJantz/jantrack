# Jantrack Loading popup v01
# Zach Jantz
# 2/4/2024
# Jantrack file transfer pop up


from PyQt5 import QtCore, QtWidgets




class Jantrack_Loading(QtWidgets.QWidget):

	def __init__(self):

		super().__init__()

		self.setGeometry(200,200,500,200)
		self.setTitle("Jantrack Loading")
		