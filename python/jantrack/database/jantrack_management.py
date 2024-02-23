# Jantrack v01
# Zach Jantz
# 12/19/2023
# Jantrack data management fucntions for managing the active project db

import os
from datetime import datetime
import copy
import subprocess
from glob import glob

from database.manifest import Manifest
from database.jantrack_ftp import copy_shot_assets, transfer_hip

 

class Jantrack_Management():
    """
    Jantrack_Management is a class structure designed to manage a working copy of 
    a projects asset database as well as functionality that assists artist in managing the 
    files and dependencies of a large project over a collaborative network.
    """
    def __init__(self):

        # Load the manifest file and store the data in a dictionary
        self.manifest_import = Manifest()
        self.jantrack_data = copy.deepcopy(self.manifest_import.manifest_data)

        # Absolute path to the network farm directory
        self.FARM_PATH = os.environ.get("JANTRACK_FARM_PATH")
        # Absolute path to the project folder
        self.NETWORK_PROJECT_PATH = os.environ.get("JANTRACK_NETWORK_PATH")
        # Local project path set by users
        self.LOCAL_PATH = ""

        self.uncommitted_additions = []
        self.uncommitted_deletions = []


    def query_assets(self,shot):
        """
        Return all assets from a shot
        Input: string shot
        Output: list asset_names
        """
        asset_names = self.jantrack_data[shot].keys()

        return asset_names
    

    def query_asset_data(self,shot, asset, data_tag):
        """
        Return asset data correlating to the given tag
        Input: string shot, string asset,
        """
        asset = self.jantrack_data[shot][asset]

        queried_data = asset[data_tag]        

        return queried_data
    

    def add_shot(self, new_shot):
        """
        Add a new shot to the jantrack database
        Input: string new_shot
        """
        self.jantrack_data[new_shot] = {}


    def delete_shot(self, shot):
        """
        Remove a given shot from the jantrack database
        Input: string shot
        """
        del self.jantrack_data[shot]


    def add_asset(self,shot, new_asset_path):
        """
        Add a new asset to a shot in the jantrack database
        Input: string shot, string new_asset_path
        """
        shot_assets = self.jantrack_data[shot]

        # Get asset data
        if os.path.isdir(new_asset_path):
            new_asset = os.path.basename(os.path.normpath(new_asset_path))
        else:
            new_asset = os.path.basename(new_asset_path)
        active_user = os.getlogin()
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        asset_path = os.path.relpath(new_asset_path, self.LOCAL_PATH)

        # New asset and asset data is added to shot assets
        shot_assets[new_asset] = {
            "path":asset_path,
            "user":active_user,
            "updated":update_time
        }

    
    def paste_asset(self,source_shot, asset_key, destination_shot):
        """
        Add a copied asset to a new shot
        Inputs: string source_shot, string asset_key, string destination_shot
        """

        destination_assets = self.jantrack_data[destination_shot]
        pasted_asset_data = self.jantrack_data[source_shot][asset_key]

        active_user = os.getlogin()
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        destination_assets[asset_key] = {
            "path":pasted_asset_data["path"],
            "user":active_user,
            "updated":update_time
        }


    def delete_asset(self, shot, asset):
        """
        Remove an asset from a shot in the jantrack database
        Input: string shot, string asset
        """
        shot_assets = self.jantrack_data[shot]
        del shot_assets[asset]
            

    def clone_shot_locally(self,shot):
        """
        Pull the selected shot's assets to the local drive from the
        network drive
        Input: string shot
        """
        if os.path.isdir(self.LOCAL_PATH):

            copy_shot_assets(self.jantrack_data[shot], self.NETWORK_PROJECT_PATH, self.LOCAL_PATH)
            transfer_hip(self.get_network_hip(shot), self.LOCAL_PATH) 


    def push_to_farm(self, shot):
        """
        Copy a shots assets to the render farm drive from the network drive
        Input: string shot
        """
        copy_shot_assets(self.jantrack_data[shot], self.NETWORK_PROJECT_PATH, self.FARM_PATH)
        transfer_hip(self.get_network_hip(shot), self.FARM_PATH)


    def commit_local_jantrack_changes(self, merge_files_check):
        """
        Function to commit the changes made in jantrack to the project manifest.
        Copies required files to the network
        Input: bool merge_files_check
        """

        if merge_files_check:

            # Loop through shots
            for shot, shot_data in self.jantrack_data.items():

                # Loop through assets
                for asset, asset_data in shot_data.items():

                    file_rel_path = asset_data["path"]

                    local_file_path = os.path.join(self.LOCAL_PATH, file_rel_path)
                    network_file_path = os.path.join(self.RIDER_PROJECT_PATH, file_rel_path)

                    if os.path.isdir(local_file_path):
                        if os.path.exists(local_file_path) is True:
                            subprocess.run(["cp", "-rT", local_file_path, network_file_path])
                    else:
                        if os.path.exists(local_file_path) is True and os.path.exists(network_file_path) is False:
                        # Files are moved with subprocess to get around annoying network blocks
                            subprocess.run(["cp",local_file_path, network_file_path])
                            
        self.manifest_import.manifest_data = self.jantrack_data
        self.manifest_import.update_manifest()


    def refresh_jantrack(self):
        """
        Function for inporting any changes made by other jantrack users
        """
        self.manifest_import.load_manifest()
        self.jantrack_data = copy.deepcopy(self.manifest_import.manifest_data)

        
    def get_network_hip(self, shot):
        """
        Get the latest network houdini file path for a shot from the network drive
        Input: string shot
        Output: string shot_hip_path
        """
        path = os.path.join(self.NETWORK_PROJECT_PATH, shot) + "*"
        hips = sorted(glob(path))
        if len(hips)>1:
            shot_hip_path = hips[-1]

            return shot_hip_path

        else:
            return None






