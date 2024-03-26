import hou
from PySide2 import QtWidgets, QtCore
import os
import subprocess
from glob import glob



class Rider_Versioning_Tool(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        usr_home = os.path.expanduser("~")

        self.setGeometry(500,300,100,110)

        #Absolute network path
        self.NETWORK_PROJECT_PATH = os.environ.get("JANTRACK_NETWORK_PATH")

        self.setWindowTitle("Save and Push New File Version")

        vbox_1 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_1)

        label1 = QtWidgets.QLabel("Confirm versioning up this file")
        vbox_1.addWidget(label1)

        hbox_1 = QtWidgets.QHBoxLayout()
        vbox_1.addLayout(hbox_1)


        cancel_button = QtWidgets.QPushButton("Cancel")
        hbox_1.addWidget(cancel_button)
        cancel_button.clicked.connect(self.close)

        confirm_button = QtWidgets.QPushButton("Confirm")
        hbox_1.addWidget(confirm_button)
        confirm_button.clicked.connect(self.save_and_increment)


    def save_and_increment(self):

        if self.active_is_current():                    
            hou.hipFile.saveAndIncrementFileName()
            new_hip_name = hou.hipFile.basename()
            NEW_HIP_PATH = hou.hipFile.path()

            NETWORK_HIP_PATH = os.path.join(self.NETWORK_PROJECT_PATH, new_hip_name)

            subprocess.run(["cp",NEW_HIP_PATH, NETWORK_HIP_PATH])

            shot_name = new_hip_name.split("_v")[0]
            local_search = os.path.join(os.path.dirname(NEW_HIP_PATH), shot_name) + "*"
            network_search = os.path.join(self.NETWORK_PROJECT_PATH, shot_name) + "*" 

            local_versions = sorted(glob(local_search))
            network_versions = sorted(glob(network_search))

            for local_version in local_versions:

                if len(local_versions)>10:

                    oldest_local_version = local_versions.pop(0)
                    os.remove(oldest_local_version)

            for network_version in network_versions:

                if len(network_versions)>10:

                    oldest_network_version = network_versions.pop(0)
                    os.remove(oldest_network_version)

            self.close()

        else:

            warning = QtWidgets.QMessageBox.critical(self, "Warning", 
                                                    "This File is not up to date \n Only version the latest file updates")

    def active_is_current(self):

        checked_shot = hou.hipFile.basename().split("_v")[0]
        check_network = os.path.join(self.NETWORK_PROJECT_PATH, checked_shot) + "*"
        shot_versions = sorted(glob(check_network))
        if len(shot_versions) > 0:
            latest_network_version = os.path.basename(shot_versions[-1])
    
            if hou.hipFile.basename() == latest_network_version:
    
                return True
    
            else:
    
                return False
        else:
            return True
        


