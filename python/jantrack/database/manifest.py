# Jantrack v01
# Zach Jantz
# 12/19/2023
# Jantrack json model 

import json
import os 



# Absolute path tp project manifest
MANIFEST_PATH = os.environ.get("JANTRACK_MANIFEST_PATH")

"""
Jantrack works by storing asset information and association in a json manifest file.
This data allows for more efficent project collaboration by preventing artists from missing
dependencies, preserving project structure and naming conventions, and managing file transfers.
"""

def load_disk_manifest():
    """
    Return the on disk json data dictionary
    """
    try:
        with open(MANIFEST_PATH, "r") as manifest_file:
            manifest_data = json.load(manifest_file) 
            manifest_file.close()
        return manifest_data
    except:

        print("Error: Unable to load jantrack manifest")

def update_disk_manifest(data_tree):
    """
    Write manifest to disk
    """
    try:
        with open(MANIFEST_PATH,"w") as manifest_file:

            json.dump(data_tree, manifest_file, indent=2)
            manifest_file.close()
    
    except:

        print("Error: Unable to update jantrack manifest")





        