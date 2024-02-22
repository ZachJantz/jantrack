# Jantrack v01
# Zach Jantz
# 12/19/2023
# Jantrack json model 

import json
import os 



# Absolute path tp project manifest
MANIFEST_PATH = os.path.expanduser("~") + "/mount/CollaborativeSpace/rider-project/jantrack/riders_manifest.json"



class Manifest():
    """
    Jantrack works by storing asset information and association in a json manifest file.
    This data allows for more efficent project collaboration by preventing artists from missing
    dependencies, preserving project structure and naming conventions, and managing file transfers.
    """

    def __init__(self):

        self.manifest_path = MANIFEST_PATH
        self.manifest_data = ""
        self.load_manifest()


    def load_manifest(self):
        """
        Load manifest json file to 'manifest_data'
        """
        try:
            with open(self.manifest_path, "r") as manifest_file:
                self.manifest_data = json.load(manifest_file) 
                manifest_file.close()

        except:

            print("Error: Unable to load jantrack manifest")

    def update_manifest(self):
        """
        Write manifest to disk
        """
        try:
            with open(self.manifest_path,"w") as manifest_file:

                json.dump(self.manifest_data, manifest_file, indent=2)
                manifest_file.close()
        
        except:

            print("Error: Unable to update jantrack manifest")





        