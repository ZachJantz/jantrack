# Jantrack v01
# Zach Jantz
# 12/19/2023
# Jantrack app interface

from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import time
import os

from database.jantrack_management import Jantrack_Management


class Jantrack(QtWidgets.QMainWindow):
    """
    Jantrack UI set up consisting of list view widgets that display the project data
    and a interface that allows artists to speed up their workflows in a network based
    collaborative project.
    """
    def __init__(self):

        super().__init__()

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.setFixedHeight(800)
        self.setFixedWidth(1000)

        self.setWindowTitle("Jantrack")

        self.central_hlayout1 = QtWidgets.QHBoxLayout()
        self.central_widget.setLayout(self.central_hlayout1)

        # Data Management Utility
        self.jtm = Jantrack_Management()

        # User home directory
        self.home_dir_path = QtCore.QDir().homePath()

        # --------------------Shot utility group-----------------------------------

        self.shot_context = QtWidgets.QGroupBox()
        self.shot_context.setTitle("Shots")
        self.central_hlayout1.addWidget(self.shot_context)
        self.shot_context_vlayout1 = QtWidgets.QVBoxLayout()
        self.shot_context.setLayout(self.shot_context_vlayout1)

        # Shot list view
        self.shot_list_view = QtWidgets.QListWidget()
        self.shot_list_view.setSortingEnabled(True)
        self.update_shot_list_view()
        self.shot_context_vlayout1.addWidget(self.shot_list_view)
        self.active_shot = None

        # Shot list view signal actions
        self.shot_list_view.itemPressed.connect(self.update_active_shot)
        self.shot_list_view.itemPressed.connect(self.update_asset_list_view)

        # Shot utilities
        shot_context_hlayout1 = QtWidgets.QHBoxLayout()
        self.shot_context_vlayout1.addLayout(shot_context_hlayout1)

        self.add_shot_button = QtWidgets.QPushButton("Add Shot")
        shot_context_hlayout1.addWidget(self.add_shot_button)
        self.add_shot_button.clicked.connect(self.new_shot)

        self.delete_shot_button = QtWidgets.QPushButton("Delete Shot")
        shot_context_hlayout1.addWidget(self.delete_shot_button)
        self.delete_shot_button.clicked.connect(self.delete_selected_shot)

        shot_context_hlayout2 = QtWidgets.QHBoxLayout()
        self.shot_context_vlayout1.addLayout(shot_context_hlayout2)

        self.farm_shot_button = QtWidgets.QPushButton("Farm Shot")
        shot_context_hlayout2.addWidget(self.farm_shot_button)
        self.farm_shot_button.clicked.connect(self.farm_shot)

        self.clone_shot_button = QtWidgets.QPushButton("Clone Shot")
        shot_context_hlayout2.addWidget(self.clone_shot_button)
        self.clone_shot_button.clicked.connect(self.clone_shot)

        
        # ------------------Asset utility group------------------------------------

        self.asset_context = QtWidgets.QGroupBox()
        self.asset_context.setTitle("Shot Assets")
        self.central_hlayout1.addWidget(self.asset_context)
        self.asset_context_vlayout1 = QtWidgets.QVBoxLayout()
        self.asset_context.setLayout(self.asset_context_vlayout1)

        # Asset lsit view
        self.asset_list_view = QtWidgets.QListWidget()
        self.asset_context_vlayout1.addWidget(self.asset_list_view)
        self.asset_list_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.asset_list_view.setSortingEnabled(True)
        self.active_assets = None

        # Asset list view signal actions
        self.asset_list_view.itemSelectionChanged.connect(self.update_active_asset)
        self.asset_list_view.itemPressed.connect(self.update_data_view)

        # Asset utilities 
        asset_context_hlayout1 = QtWidgets.QHBoxLayout()
        self.asset_context_vlayout1.addLayout(asset_context_hlayout1)

        self.add_asset_button = QtWidgets.QPushButton("Add Assets")
        asset_context_hlayout1.addWidget(self.add_asset_button)
        self.add_asset_button.clicked.connect(self.new_assets)

        self.delete_asset_button = QtWidgets.QPushButton("Delete Assets")
        asset_context_hlayout1.addWidget(self.delete_asset_button)
        self.delete_asset_button.clicked.connect(self.delete_selected_asset)

        self.add_asset_directory_button = QtWidgets.QPushButton("Add Multi-Component Folder")
        self.asset_context_vlayout1.addWidget(self.add_asset_directory_button)
        self.add_asset_directory_button.clicked.connect(self.new_asset_directory)


        # Left side split layout
        self.central_vlayout1 = QtWidgets.QVBoxLayout()
        self.central_hlayout1.addLayout(self.central_vlayout1)


        # ------------------Data utility group--------------------------------

        self.data_context = QtWidgets.QGroupBox()
        self.data_context.setTitle("Asset Data")
        self.central_vlayout1.addWidget(self.data_context)
        self.data_context_vlayout1 = QtWidgets.QVBoxLayout()
        self.data_context_vlayout1.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)
        self.data_context.setLayout(self.data_context_vlayout1)
    
        # Asset Path Display
        self.data_hlayout1 = QtWidgets.QHBoxLayout()
        self.data_context_vlayout1.addLayout(self.data_hlayout1)

        self.asset_path_label = QtWidgets.QLabel("Asset Path: ")
        self.data_hlayout1.addWidget(self.asset_path_label)

        self.asset_path_data = QtWidgets.QLabel("")
        self.data_hlayout1.addWidget(self.asset_path_data)

        # Asset User Display
        self.data_hlayout2 = QtWidgets.QHBoxLayout()
        self.data_context_vlayout1.addLayout(self.data_hlayout2)

        self.user_label = QtWidgets.QLabel("Last Edit By: ")
        self.data_hlayout2.addWidget(self.user_label)

        self.user_data = QtWidgets.QLabel("")
        self.data_hlayout2.addWidget(self.user_data)

        # Update Time Display
        self.data_hlayout3 = QtWidgets.QHBoxLayout()
        self.data_context_vlayout1.addLayout(self.data_hlayout3)

        self.update_time_label = QtWidgets.QLabel("Last Updated: ")
        self.data_hlayout3.addWidget(self.update_time_label)

        self.update_time_data = QtWidgets.QLabel("")
        self.data_hlayout3.addWidget(self.update_time_data)


        # --------------------------Merge Utility Group------------------------------
        
        self.merge_context = QtWidgets.QGroupBox()
        self.merge_context.setTitle("Jantrack Updates")
        self.central_vlayout1.addWidget(self.merge_context)
        merge_context_vlayout1 = QtWidgets.QVBoxLayout()
        merge_context_vlayout1.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)
        self.merge_context.setLayout(merge_context_vlayout1)

        merge_context_hlayout1 = QtWidgets.QHBoxLayout()
        merge_context_vlayout1.addLayout(merge_context_hlayout1)

        local_directory = QtWidgets.QLabel("Local Directory")
        merge_context_hlayout1.addWidget(local_directory)

        # Display local project path
        self.local_directory_path_display = QtWidgets.QLineEdit("")
        merge_context_hlayout1.addWidget(self.local_directory_path_display)

        self.get_local_directory = QtWidgets.QPushButton("Set")
        merge_context_hlayout1.addWidget(self.get_local_directory)

        # Prompt project setting
        self.select_local_project_path()
        self.get_local_directory.clicked.connect(self.select_local_project_path)

        self.commit_progress_button = QtWidgets.QPushButton("Commit")
        merge_context_vlayout1.addWidget(self.commit_progress_button)
        self.commit_progress_button.clicked.connect(self.commit_changes)

        self.merge_files_box = QtWidgets.QCheckBox("Include Asset Files")
        merge_context_vlayout1.addWidget(self.merge_files_box)
        self.merge_files_box.setChecked(True)

        self.reload_button = QtWidgets.QPushButton("Reload Jantrack")
        merge_context_vlayout1.addWidget(self.reload_button)
        self.reload_button.clicked.connect(self.reload_jantrack)


        # -------------------------Keyboard Shortcuts-----------------------------

        self.copy_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_C),self)
        self.copy_shortcut.activated.connect(self.copy_assets)
        self.copied_assets = []

        self.paste_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_V),self)
        self.paste_shortcut.activated.connect(self.paste_assets)
        


    # ------------------------Update View Functions-------------------------------

    def update_shot_list_view(self):
        """
        Update the shot list view to display existing shots
        """
        self.shot_list_view.clear()
        shots = list(self.jtm.jantrack_data.keys())
        self.shot_list_view.addItems(shots)


    def update_active_shot(self,item):
        """
        Store the acitvely selected shot
        """
        self.active_shot = item.text()


    def update_active_asset(self):
        """
        Store the actively selected asset
        """
        assets = [item.text() for item in list(self.asset_list_view.selectedItems())]
        self.active_assets = assets


    def update_asset_list_view(self):
        """
        Refresh the asset list widget to correspond with the selected shot
        """
        self.asset_list_view.clear()
        
        assets = self.jtm.query_assets(self.active_shot)
        self.asset_list_view.addItems(assets)

    
    def update_data_view(self):
        """
        Refresh the asset data display to correspond with the selected asset
        """
        self.clear_asset_data_display()

        self.asset_path_data.setText(self.jtm.query_asset_data(self.active_shot, self.active_assets[-1],"path"))
        self.user_data.setText(self.jtm.query_asset_data(self.active_shot, self.active_assets[-1],"user"))
        self.update_time_data.setText(self.jtm.query_asset_data(self.active_shot, self.active_assets[-1],"updated"))


    def clear_asset_data_display(self):
        """
        Function for clearing the data view
        """
        self.asset_path_data.clear()
        self.user_data.clear()
        self.update_time_data.clear()


    # -----------------------------Shot Utility Functions-----------------------------------------
        
    def new_shot(self):
        """
        Add a new shot to the shot list
        """
        shot_name, done = QtWidgets.QInputDialog.getText(self, "Add Shot", "Enter Shot Name: ")
        if done:

            # Check if shot already exists
            if shot_name in list(self.jtm.jantrack_data.keys()):

                QtWidgets.QMessageBox.critical(self, "Warning", "Added shot already exists")
                return None

            else:
                self.jtm.add_shot(shot_name)
                self.update_shot_list_view()


    def delete_selected_shot(self):
        """
        Remove the selected shot from the shot list
        """
        # Check that a shot is selected
        if self.active_shot != None:
            button = QtWidgets.QMessageBox.question(self, "Confirm", 
                                                    "Are you sure you want to delete {}?\nThis action is not reversable".format(self.active_shot))

            # If deletion is confirmed, delete the shot from the jantrack manager
            if button == QtWidgets.QMessageBox.Yes:
                self.jtm.delete_shot(self.active_shot)

                self.update_shot_list_view()

            else:
                return None
        else:
            return None
            

    def farm_shot(self):
        """
        Push the selected shot to the SCAD RenderFarm
        """
        if self.active_shot != None:
            button = QtWidgets.QMessageBox.question(self, "Confirm",
                                                    "Confirm pushing {} to the SCAD RenderFarm".format(self.active_shot))

            if button == QtWidgets.QMessageBox.Yes:

                self.jtm.push_to_farm(self.active_shot)

        else:
            warning = QtWidgets.QMessageBox.critical(self, "Warning", "Failed to add shot to the RenderFarm")
            return None


    def clone_shot(self):
        """
        Pull the active shot to a local drive
        """
        if self.active_shot != None:
            button = QtWidgets.QMessageBox.question(self, "Confirm",
                                                    "Confirm pushing {} to your local project".format(self.active_shot))

            if button == QtWidgets.QMessageBox.Yes:
                try:
                    self.jtm.clone_shot_locally(self.active_shot)
                except:
                    fail = QtWidgets.QMessageBox.critical(self, "Fail",
                                                        "Unable to clone {} to your local project".format(self.active_shot))
        else:
            warning = QtWidgets.QMessageBox.critical(self, "Warning", "Select a shot to pull")



    # ----------------------------Asset Utility Functions-----------------------------
        
    def new_assets(self):
        """
        Add a new asset to the active shot
        """
        if self.active_shot != None:

            # Fetch a list of desired assets to add
            asset_paths = QtWidgets.QFileDialog.getOpenFileNames(self, caption="Select Assets",
                                                                 directory=self.jtm.LOCAL_PATH,
                                                                 filter="All files (*.*)")[0]
            
            # If asset_paths are selected add each asset to jantrack
            try:
                if len(asset_paths)>0:

                    for asset_path in asset_paths:
                        self.jtm.add_asset(self.active_shot, asset_path)
                    self.update_asset_list_view()
            except:
                warning1 = QtWidgets.QMessageBox.critical(self, "Warning", "Failed to add asset")

        else:
            warning2 = QtWidgets.QMessageBox.critical(self, "Warning", "Select a shot first")
        

    def delete_selected_asset(self):
        """
        Delete the selected asset from the active shot
        """
        if self.active_assets != None:
            for asset in self.active_assets:
                button = QtWidgets.QMessageBox.question(self, "Confirm", 
                                                        "Are you sure you want to delete {}?\nThis action is not reversable".format(asset))
                # If confirmed delete the asset
                if button == QtWidgets.QMessageBox.Yes:

                    self.jtm.delete_asset(self.active_shot,asset)
                    self.update_asset_list_view()
                    self.clear_asset_data_display()
                else:
                    return None
        else:
            return None

    def copy_assets(self):

        self.copied_assets = self.active_assets
        self.copied_shot = self.active_shot


    def paste_assets(self):

        if self.active_shot != None:
            for asset in self.copied_assets:
                if asset not in self.jtm.jantrack_data[self.active_shot].keys():
                    self.jtm.paste_asset(self.copied_shot, asset, self.active_shot)
            self.update_asset_list_view()
                    
        else:
            warning1 = QtWidgets.QMessageBox.critical(self, "Warning", "Select a shot first")


    def new_asset_directory(self):
        """
        Add a folder containing a sequential frame dependant asset
        """
        if self.active_shot != None:
            asset_directory_path = QtWidgets.QFileDialog.getExistingDirectory(self, caption = "Select Asset Directory",
                                                                                directory = self.jtm.LOCAL_PATH)
            try:
                if os.path.isdir(asset_directory_path):
                    self.jtm.add_asset(self.active_shot, asset_directory_path)
                self.update_asset_list_view()
            except:
                warning3 = QtWidgets.QMessageBox.critical(self, "Warning", "Failed to add asset")
        else:
            warning4 = QtWidgets.QMessageBox.critical(self, "Warning", "Select a shot first")
    

    #------------------------Commit Functions-------------------------------------

    def select_local_project_path(self):
        """
        Select the users local project folder
        """
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, caption="Set Local Directory",
                                                                 directory=self.home_dir_path)
        self.local_directory_path_display.setText(directory)
        self.jtm.LOCAL_PATH = directory                                                 


    def commit_changes(self):
        """
        Run the jantrack save functions
        """
        confirm = QtWidgets.QMessageBox.question(self, "Confirm",
                                                    "Confirm jantrack data merge")
        if confirm == QtWidgets.QMessageBox.Yes:

            self.jtm.commit_local_jantrack_changes(self.merge_files_box.isChecked())


    def reload_jantrack(self):
        """
        Allow users to get latest jantrack commits
        """    
        self.jtm.refresh_jantrack()
        self.update_shot_list_view()





    

