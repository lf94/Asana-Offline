#
# A way to visualize exported asana data.
#
# Lee Fallat 2014
#

import json
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Asana:
	def __init__(self):
		self.tasks = []
	
	def read(self, files):
		for filepath in files:
			with open(filepath, "r") as fh:
				self.tasks.extend(json.loads(fh.read())['data'])
			
			
	def taskClicked(self):
			rowSelected = self.window.sender().selectionModel().currentIndex().row()
			self.task_desc.setText(self.tasks[rowSelected]['notes'])
	
	def render(self):
		app = QApplication(sys.argv)
		window = QWidget()
		self.window = window
		window.setWindowTitle("Asana Tasks")
		
		hsplit = QHBoxLayout(window)
		task_view = QVBoxLayout(window)
		task_assignee_view = QHBoxLayout(window)
		task_desc_view = QVBoxLayout(window)
		
		task_table = QTableView(window)
		task_table.setShowGrid(False)
		task_table.horizontalHeader().setVisible(True)
		
		task_table.horizontalHeader().setStretchLastSection(True)
		task_table.verticalHeader().setVisible(False)
		task_desc = QTextEdit(window)
		task_desc.isReadOnly = True
		self.task_desc = task_desc
		task_model = QStandardItemModel(len(self.tasks), 2, task_table)
		task_model.setHorizontalHeaderItem(0, QStandardItem("Assignee"))
		task_model.setHorizontalHeaderItem(1, QStandardItem("Task"))
		project_name_label = None
		
		total_tasks = len(self.tasks)
		for number in range(total_tasks):
			try:
				tokenized_name = self.tasks[number]['assignee']['name'].split(" ")
			except TypeError:
				tokenized_name = [ "-", "-" ]
			
			if not project_name_label:
				project_name_label = QLabel(self.tasks[number]['projects'][0]['name'], window)
			
			abbreviated_name = tokenized_name[0][0]+tokenized_name[1][0]
			name_item = QStandardItem(abbreviated_name)
			name_item.setFlags(Qt.NoItemFlags)
			task_item =  QStandardItem(self.tasks[number]['name'])
			task_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
			task_table.clicked.connect(self.taskClicked)
			task_model.setItem(number, 0, name_item)
			task_model.setItem(number, 1, task_item)
		
		task_table.setModel(task_model)
		for number in range(len(self.tasks)):
			if self.tasks[number]['completed']:
				task_table.hideRow(number)
		task_assignee_view.addWidget(task_table)
		task_view.addWidget(project_name_label)
		task_view.addLayout(task_assignee_view)
		task_desc_view.addWidget(task_desc)
		hsplit.addLayout(task_view)
		hsplit.addLayout(task_desc_view)
		window.show()
		sys.exit(app.exec_())
		
a = Asana()
a.read(sys.argv[1:])
a.render()