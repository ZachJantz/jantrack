# Jantrack v01
# Zach Jantz
# 12/19/2023
# Jantrack data management fucntions for managing the active project db

import os
from datetime import datetime
import copy
from glob import glob

from database.manifest import load_disk_manifest, update_disk_manifest
from database.jantrack_ftp import copy_shot_assets, transfer_hip, transfer_asset_files
from database.commit_tracking import Commits

 

class Jantrack_Management():
    """
    Jantrack_Management is a class structure designed to manage a working copy of 
    a projects asset database as well as functionality that assists artist in managing the 
    files and dependencies of a large project over a collaborative network.
    """
    def __init__(self):

        # Load the manifest file and store the data in a dictionary
        self.jantrack_data = copy.deepcopy(load_disk_manifest())

        # Absolute path to the network farm directory
        self.FARM_PATH = os.environ.get("JANTRACK_FARM_PATH")
        # Absolute path to the project folder
        self.NETWORK_PROJECT_PATH = os.environ.get("JANTRACK_NETWORK_PATH")
        # Local project path set by users
        self.LOCAL_PATH = ""

        self.commit_record = Commits()



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
        self.commit_record.record_shot_addition(new_shot)
        print(self.commit_record.shot_additions)


    def delete_shot(self, shot):
        """
        Remove a given shot from the jantrack database
        Input: string shot
        """
        del self.jantrack_data[shot]
        self.commit_record.record_shot_deletion(shot)


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
        if new_asset not in shot_assets.keys():
            shot_assets[new_asset] = {
                "path":asset_path,
                "user":active_user,
                "updated":update_time
            }

            self.commit_record.record_asset_addition(shot,new_asset)

    
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

        self.commit_record.record_asset_addition(destination_shot, asset_key)


    def delete_asset(self, shot, asset):
        """
        Remove an asset from a shot in the jantrack database
        Input: string shot, string asset
        """
        shot_assets = self.jantrack_data[shot]
        del shot_assets[asset]
        self.commit_record.record_asset_deletion(shot, asset)
    
    
    def get_network_hip(self, shot):
        """
        Get the latest network houdini file path for a shot from the network drive
        Input: string shot
        Output: string shot_hip_path
        """
        
        path = os.path.join(self.NETWORK_PROJECT_PATH, shot) + "*"
        hips = sorted(glob(path))
        if len(hips)>=1:
            shot_hip_path = hips[-1]

            return shot_hip_path

        else:
            return None

            
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

            # Loop stored asset commits
            for key_path in self.commit_record.asset_additions:
                transfer_asset_files(self.jantrack_data[key_path[0]][key_path[1]], self.LOCAL_PATH, self.NETWORK_PROJECT_PATH)

        # Memory database -> disk database
                
        disk_data = load_disk_manifest()

        for shot_key in self.commit_record.shot_additions:
            disk_data[shot_key] = {}

        for shot_key in self.commit_record.shot_deletions:
            del disk_data[shot_key]

        for asset_record in self.commit_record.asset_additions:
            disk_data[asset_record[0]][asset_record[1]] = self.jantrack_data[asset_record[0]][asset_record[1]]

        for asset_record in self.commit_record.asset_deletions:
            del disk_data[asset_record[0]][asset_record[1]]
        
        update_disk_manifest(disk_data)
        self.commit_record.clear_record()

        
    def refresh_jantrack(self):
        """
        Function for inporting any changes made by other jantrack users
        """
        disk_data = load_disk_manifest()
        # Append added data
        for shot, shot_data in disk_data.items():
            if shot not in self.jantrack_data.keys() and shot not in self.commit_record.shot_deletions:
                self.jantrack_data[shot] = shot_data

            else:
                for asset, asset_data in shot_data.items():
                    if asset not in self.jantrack_data[shot].keys() and [shot,asset] not in self.commit_record.asset_deletions:
                        self.jantrack_data[shot][asset] = asset_data

        # Append on disk deletions
        current_memory_data = copy.deepcopy(self.jantrack_data)
        for shot, shot_data in current_memory_data.items():
            if shot not in disk_data.keys() and shot not in self.commit_record.shot_additions:
                del self.jantrack_data[shot]

            else:
                for asset, asset_data in shot_data.items():
                    if asset not in disk_data[shot].keys() and [shot, asset] not in self.commit_record.asset_additions:
                        del self.jantrack_data[shot][asset]
        
            




    






