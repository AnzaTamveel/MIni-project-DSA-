from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
from scraper_thread import ScraperWorker
from Opening import DisplayPage
import requests
from SearchingAlgo import (search_by_filter)
from sorting_algorithms import (
    insertion_sort,
    merge_sort,
    bubble_sort,
    selection_sort,
    counting_sort,
    radix_sort,
    bucket_sort,
    shell_sort, heap_sort, quick_sort , comb_sort
)


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.csv_file_path = "" 
        self.setupUi()
        self.splash_screen = DisplayPage()
        self.splash_screen.show()

        QtCore.QTimer.singleShot(5000, self.close_splash_and_show_main)

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)
    
    def close_splash_and_show_main(self):
        self.splash_screen.close()
        self.show()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1000, 800)
         

    # Central widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet("background-color: #323232; color: lightgrey;")
        self.setCentralWidget(self.centralwidget)

    # Layout for the central widget
        self.mainLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

    # Top border (horizontal line)
        self.topBorder = self.createBorderFrame(QtCore.Qt.Horizontal)
        self.mainLayout.addWidget(self.topBorder, 0, 0, 1, 3)

    # Left border (vertical line)
        self.leftBorder = self.createBorderFrame(QtCore.Qt.Vertical)
        self.mainLayout.addWidget(self.leftBorder, 1, 0, 1, 1)

    # Main content area (will go here)
        self.contentArea = QtWidgets.QWidget(self.centralwidget)
        self.contentLayout = QtWidgets.QVBoxLayout(self.contentArea)
        self.contentArea.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addWidget(self.contentArea, 1, 1, 1, 1)

    # Right border (vertical line)
        self.rightBorder = self.createBorderFrame(QtCore.Qt.Vertical)
        self.mainLayout.addWidget(self.rightBorder, 1, 2, 1, 1)

    # Bottom border (horizontal line)
        self.bottomBorder = self.createBorderFrame(QtCore.Qt.Horizontal)
        self.mainLayout.addWidget(self.bottomBorder, 2, 0, 1, 3)

    # Add other UI components inside the content area
        self.addComponents()

    # Adding CSV and URL buttons
        self.addDataImportButtons()
      
    # Setting the menu bar and status bar
        self.menubar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def createBorderFrame(self, orientation):
        """Creates a QFrame for the border with a solid color."""
        frame = QtWidgets.QFrame(self.centralwidget)
        if orientation == QtCore.Qt.Horizontal:
            frame.setFixedHeight(10)
            frame.setStyleSheet("background-color: black;")
            frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        else:  # Vertical
            frame.setFixedWidth(10)
            frame.setStyleSheet("background-color: black;")
            frame.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

        return frame
    def addComponents(self):

        # Column names for the checkboxes
        column_names = [
            "Name", "Profile Link", "Title", "Location", 
            "Rate per Hour", "Job Success Score", "Total Earnings", "Category"
        ]

        # Scraping Controls GroupBox
        self.scrapingControls = QtWidgets.QGroupBox("Scraping Controls", self.contentArea)
        self.scrapingControls.setStyleSheet("color: lightgrey; font-size: 16px;")
        self.scrapingLayout = QtWidgets.QHBoxLayout(self.scrapingControls)

        self.sort_asc_button = QtWidgets.QPushButton("Sort Ascending")
        self.sort_asc_button.clicked.connect(self.sort_ascending)
        self.scrapingLayout.addWidget(self.sort_asc_button)

        self.sort_desc_button = QtWidgets.QPushButton("Sort Descending")
        self.sort_desc_button.clicked.connect(self.sort_descending) 
        self.scrapingLayout.addWidget(self.sort_desc_button)

        self.startButton = QtWidgets.QPushButton("Start", self.scrapingControls)
        self.startButton.clicked.connect(self.scrape_url)
        self.pauseButton = QtWidgets.QPushButton("Pause", self.scrapingControls)
        self.resumeButton = QtWidgets.QPushButton("Resume", self.scrapingControls)
        self.stopButton = QtWidgets.QPushButton("Stop", self.scrapingControls)

        self.scrapingLayout.addWidget(self.startButton)
        self.scrapingLayout.addWidget(self.pauseButton)
        self.scrapingLayout.addWidget(self.resumeButton)
        self.scrapingLayout.addWidget(self.stopButton)

        self.progressBar = QtWidgets.QProgressBar(self.scrapingControls)
        self.progressBar.setValue(0)
        self.progressBar.setStyleSheet("""
            QProgressBar {
                background-color: black;  /* Default black background */
                color: lightgrey;  /* Progress text color */
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;  /* Center the progress text */
            }
            QProgressBar::chunk {
                background-color: green;  /* Green progress chunk */
            }
        """)
        self.scrapingLayout.addWidget(self.progressBar)

        self.contentLayout.addWidget(self.scrapingControls)

        self.sortingControls = QtWidgets.QGroupBox("Sorting Options", self.contentArea)
        self.sortingControls.setStyleSheet("color: lightgrey; font-size: 16px;")
        self.sortingLayout = QtWidgets.QGridLayout(self.sortingControls)  # Change to grid layout

        # checkboxes for sorting options in two columns
        self.sortingCheckboxes = {}
        for i, name in enumerate(column_names):
            checkbox = QtWidgets.QCheckBox(name)
            self.sortingCheckboxes[name] = checkbox
            row = i // 4 
            col = i % 4 
            self.sortingLayout.addWidget(checkbox, row, col) 
                
        self.sortingAlgoComboBox = QtWidgets.QComboBox(self.sortingControls)
        self.sortingAlgoComboBox.addItems([
            "Insertion Sort", "Merge Sort", "Bubble Sort", "Selection Sort", 
            "Counting Sort", "Radix Sort", "Bucket Sort",
            "Shell Sort", "Heap Sort", "Quick Sort", "Comb Sort" 
        ])
        self.sortButton = QtWidgets.QPushButton("Sort", self.sortingControls)
        self.sortButton.clicked.connect(self.sort_data)

        self.sortingLayout.addWidget(self.sortingAlgoComboBox, 2, 0, 1, 2) 
        self.sortingLayout.addWidget(self.sortButton, 2, 2, 1, 2) 

        self.contentLayout.addWidget(self.sortingControls)

        # Searching Controls GroupBox
        self.searchControls = QtWidgets.QGroupBox("Search Options", self.contentArea)
        self.searchControls.setStyleSheet("color: lightgrey; font-size: 16px;")
        self.searchLayout = QtWidgets.QGridLayout(self.searchControls)

        self.searchCheckboxes = {}
        for i, name in enumerate(column_names):
            checkbox = QtWidgets.QCheckBox(name)
            self.searchCheckboxes[f"Column {i + 1}"] = checkbox
            row = i // 4 
            col = i % 4
            self.searchLayout.addWidget(checkbox, row + 1, col) 

        self.searchInput = QtWidgets.QLineEdit(self.searchControls)
        self.searchInput.setPlaceholderText("Enter search query")
        self.searchInput.setStyleSheet("""
            QLineEdit {
                border: 2px solid grey;  /* Solid grey border */
                color: lightgrey;  /* Text color */
                padding: 5px;
                border-radius: 5px;
            }
            QLineEdit::placeholder {
                color: grey;  /* Placeholder text color */
            }
        """)

        self.searchButton = QtWidgets.QPushButton("Search", self.searchControls)
        self.searchButton.clicked.connect(self.search_data)

        self.searchLayout.addWidget(self.searchInput, 3, 0, 1, 2)  
        self.searchLayout.addWidget(self.searchButton, 3, 2, 1, 2)  

        self.filterOptionGroup = QtWidgets.QButtonGroup(self.searchControls)
        self.andFilter = QtWidgets.QRadioButton("AND")
        self.orFilter = QtWidgets.QRadioButton("OR")
        self.notFilter = QtWidgets.QRadioButton("NOT")
        self.andFilter.setChecked(True)

        self.containsFilter = QtWidgets.QRadioButton("Contains")
        self.startsWithFilter = QtWidgets.QRadioButton("Starts With")
        self.endsWithFilter = QtWidgets.QRadioButton("Ends With")

        self.filterOptionGroup.addButton(self.andFilter)
        self.filterOptionGroup.addButton(self.orFilter)
        self.filterOptionGroup.addButton(self.notFilter)
        self.filterOptionGroup.addButton(self.containsFilter)
        self.filterOptionGroup.addButton(self.startsWithFilter)
        self.filterOptionGroup.addButton(self.endsWithFilter)

        self.searchLayout.addWidget(self.andFilter, 4, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.searchLayout.addWidget(self.orFilter, 4, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.searchLayout.addWidget(self.notFilter, 4, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.searchLayout.addWidget(self.containsFilter, 4, 3, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.searchLayout.addWidget(self.startsWithFilter, 4, 4, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.searchLayout.addWidget(self.endsWithFilter, 4, 5, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.contentLayout.addWidget(self.searchControls)

        self.entityList = QtWidgets.QTableWidget(self.contentArea)
        self.entityList.setSelectionBehavior(QtWidgets.QTableWidget.SelectColumns)
        self.entityList.setColumnCount(8)
        self.entityList.setHorizontalHeaderLabels(column_names)
        self.entityList.setStyleSheet("background-color: black; color: lightgrey; gridline-color: grey;")
        self.entityList.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #323232; color: lightgrey; }")

        self.entityList.horizontalHeader().setStretchLastSection(True)
        self.entityList.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.contentLayout.addWidget(self.entityList)

        self.clearButton = QtWidgets.QPushButton("Clear Data", self.contentArea)
        self.clearButton.setStyleSheet("color: lightgrey; font-size: 16px;")
        self.clearButton.clicked.connect(self.clear_table)

        self.contentLayout.addWidget(self.clearButton)
        self.contentLayout.addSpacing(20)     
    def addDataImportButtons(self):
        self.dataImportControls = QtWidgets.QGroupBox("Data Import Options", self.contentArea)
        self.dataImportControls.setStyleSheet("color: lightgrey; font-size: 16px;")
        self.dataImportLayout = QtWidgets.QHBoxLayout(self.dataImportControls)

        self.importCsvButton = QtWidgets.QPushButton("Import CSV", self.dataImportControls)
        self.importCsvButton.clicked.connect(self.import_csv)

        self.urlInput = QtWidgets.QLineEdit(self.dataImportControls)
        self.urlInput.setPlaceholderText("Enter URL...")
        self.urlInput.setText("https://www.freelancer.pk/freelancers/skills")
        self.urlInput.setStyleSheet("color: lightgrey; font-size: 16px;")


        self.dataImportLayout.addWidget(self.importCsvButton)
        self.dataImportLayout.addWidget(self.urlInput)

        self.contentLayout.addWidget(self.dataImportControls)
        
        self.timeTakenLabel = QtWidgets.QLabel("Time Taken: 0 seconds", self.contentArea)
        self.timeTakenLabel.setStyleSheet("color: lightgrey; font-size: 16px;")
        self.contentLayout.addWidget(self.timeTakenLabel)

    def sort_ascending(self):
        # Get selected column indices from checkboxes
        selected_column_indices = [
            index for index, (name, checkbox) in enumerate(self.sortingCheckboxes.items()) 
            if checkbox.isChecked()
        ]

        if not selected_column_indices:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select at least one column to sort.")
            return

        # Sort the indices in ascending order
        sorted_indices = sorted(selected_column_indices)

        for column_index in sorted_indices:
            self.sort_asc_for_column(column_index)

    def sort_asc_for_column(self, column_index):
        if column_index < 0 or column_index >= self.entityList.columnCount():
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid column index provided.")
            return

        data = self.get_data_from_table()
        
        # Use the column index to sort
        sorted_data = data.sort_values(by=data.columns[column_index]).reset_index(drop=True)

        self.populate_table(sorted_data)

    def sort_descending(self):
        # Get selected column indices from checkboxes
        selected_column_indices = [
            index for index, (name, checkbox) in enumerate(self.sortingCheckboxes.items()) 
            if checkbox.isChecked()
        ]
        
        if not selected_column_indices:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select at least one column to sort.")
            return

        # Sort the indices in ascending order
        sorted_indices = sorted(selected_column_indices)

        for column_index in sorted_indices:
            self.sort_desc_for_column(column_index)

    def sort_desc_for_column(self, column_index):
        if column_index < 0 or column_index >= self.entityList.columnCount():
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid column index provided.")
            return

        data = self.get_data_from_table()
        
        # Use the column index to sort
        sorted_data = data.sort_values(by=data.columns[column_index], ascending=False).reset_index(drop=True)

        self.populate_table(sorted_data)

    def import_csv(self):
        """Function to import data from a CSV file."""
        options = QtWidgets.QFileDialog.Options()
        filePath, __ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (.csv);;All Files ()", options=options)
        if filePath:
            try:
                self.csv_file_path = filePath 
                # Loading the CSV file using pandas
                data = pd.read_csv(filePath)
                # Clear the table and populate it with the new data
                self.populate_table(data)
                QtWidgets.QMessageBox.information(self, "Success", "CSV file imported successfully!")
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to import CSV file: {str(e)}")

    def scrape_url(self):
        """Function to scrape data from a URL."""
        base_url = self.urlInput.text()
        if not base_url:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter a URL.")
            return
        self.worker = ScraperWorker(base_url)
        self.worker.finished.connect(self.on_scraping_finished)
        self.worker.progress.connect(self.update_progress)
        self.worker.start()

    def stop_scraping(self):
        """Function to stop the scraping process."""
        if hasattr(self, 'worker'):
            self.worker.stop_scrap = True
            QtWidgets.QMessageBox.warning(self, "Stopping", "Stopping the scraping process...")
    def on_scraping_finished(self, data):
        """Handles the data after scraping is finished."""
        self.populate_table(data)
        QtWidgets.QMessageBox.information(self, "Success", "Scraping completed successfully!")

    def update_progress(self, scraped_items, total_items):
        """Update progress bar based on items scraped."""
        percentage = int((scraped_items / total_items) * 100)
        self.progressBar.setValue(percentage)
        self.progressBar.setFormat(f"Scraped {scraped_items} of {total_items} items ({percentage}%)") 
        
    def populate_table(self, data):
        """Populate the table with the given data."""
        self.entityList.setRowCount(len(data))
        for i, row in data.iterrows():
            for j, value in enumerate(row):
                self.entityList.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

    def clear_table(self):
            """Clear the table data but keep the original CSV data in memory."""
            reply = QtWidgets.QMessageBox.question(self, 'Clear Data', 
                "Do you want to remove the imported file or just reload the data?\n"
                "Remove the file\n" ,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                try:
                    import os
                    # os.remove(self.csv_file_path)
                    self.entityList.setRowCount(0)
                    QtWidgets.QMessageBox.information(self, "Cleared", "Imported file has been removed and table data has been cleared.")
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to remove the file: {str(e)}")
            else:
                try:
                    data = pd.read_csv(self.csv_file_path)
                except Exception as e:
                    data = pd.read_csv("D:\\BSCS\\3rd Semester\\DSA\\MINI Project\\live_scrap_freelancer_data.csv")
                
                # Update the table with the reloaded data
                self.entityList.setRowCount(len(data))
                for row_idx, row_data in data.iterrows():
                    for col_idx, value in enumerate(row_data):
                        self.entityList.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def retranslateUi(self):
        self.setWindowTitle("Data Scraper")
        self.menubar.setAccessibleName("Menu Bar")
        

    def get_data_from_table(self):
        """Retrieve data from the table for sorting and searching."""
        data = []
        for row in range(self.entityList.rowCount()):
            row_data = []
            for column in range(self.entityList.columnCount()):
                item = self.entityList.item(row, column)
                row_data.append(item.text() if item else "")
            data.append(row_data)
        return pd.DataFrame(data, columns=["Name", "Profile Link", "Title", "Location", "Rate per Hour", "Job Success Score", "Total Earnings" , "Location"])
    def sort_data(self):
        # Identify which columns have been selected via checkboxes
        selected_columns = [col for col, checkbox in self.sortingCheckboxes.items() if checkbox.isChecked()]

        if not selected_columns:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select at least one column to sort.")
            return
        selected_column_indices = [
            index for index, checkbox in enumerate(self.sortingCheckboxes.values()) if checkbox.isChecked()
        ]
       
        sorting_algorithm = self.sortingAlgoComboBox.currentText()

        # Get data from the table
        data = self.get_data_from_table()

        start_time = time.time()

        # Update the progress bar to show sorting has started
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(100)

        # Create a copy of the original DataFrame to keep rows intact
        original_data = data.copy()
        print("outside " , selected_column_indices )# Pass the Series directly
        # Sort each selected column independently
        for col_index in selected_column_indices:
            column_data = original_data.iloc[:, col_index]  # Get the column as a Series
            print("for" , selected_column_indices )# Pass the Series directly

            if sorting_algorithm == "Insertion Sort":
                print("up the inset" , selected_column_indices )# Pass the Series directly
                sorted_column = insertion_sort(column_data , col_index) 
                print("dowm the inset" , selected_column_indices )# Pass the Series directly
            elif sorting_algorithm == "Merge Sort":
                sorted_column = merge_sort(column_data)
            elif sorting_algorithm == "Bubble Sort":
                sorted_column = bubble_sort(column_data)
            elif sorting_algorithm == "Selection Sort":
                sorted_column = selection_sort(column_data)
            elif sorting_algorithm == "Counting Sort":
                sorted_column = counting_sort(column_data)
            elif sorting_algorithm == "Radix Sort":
                sorted_column = radix_sort(column_data)
            elif sorting_algorithm == "Bucket Sort":
                sorted_column = bucket_sort(column_data)
            elif sorting_algorithm == "Shell Sort":
                sorted_column = shell_sort(column_data)
            elif sorting_algorithm == "Heap Sort":
                sorted_column = heap_sort(column_data)
            elif sorting_algorithm == "Quick Sort":
                sorted_column = quick_sort(column_data)
            elif sorting_algorithm == "Comb Sort":
                sorted_column = comb_sort(column_data)

            # Update the original data with the sorted column while maintaining the original rows
            print("sorted Column " , sorted_column)
            original_data.iloc[:, col_index] = sorted_column

            # Update the progress bar incrementally
            self.progressBar.setValue(int((col_index + 1) / len(selected_column_indices) * 100))

        end_time = time.time()
        time_taken = end_time - start_time
        self.progressBar.setValue(100)
        self.timeTakenLabel.setText(f"Time Taken: {time_taken:.4f} seconds")

        # Populate the table with the sorted data
        self.populate_table(original_data)


    def search_data(self):
        """Search data based on the user input and the selected search method."""
        search_query = self.searchInput.text()
        if not search_query:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter a search query.")
            return
        
        data = self.get_data_from_table().copy()
        column_indices = [
            index for index, checkbox in enumerate(self.searchCheckboxes.values()) if checkbox.isChecked()
        ]
        selected_filter = self.filterOptionGroup.checkedButton().text()

        if not column_indices:
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select column to search.")
            return
        if selected_filter in ["AND", "OR", "NOT"] and len(column_indices) < 2:
            QtWidgets.QMessageBox.warning(self, "Selection Error", "For AND, OR, and NOT filters, at least two columns must be selected.")
            return
        result = search_by_filter(data, column_indices, search_query, selected_filter)
        if not result.empty:
            self.populate_table(result)
        else:
            QtWidgets.QMessageBox.information(self, "No Results", "No matches found for your query.")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = Ui_MainWindow()  # Create the main window instance
    sys.exit(app.exec_()) 
    
    # app = QtWidgets.QApplication(sys.argv)
    # window = Ui_MainWindow()
    # window.show()
    # sys.exit(app.exec_())