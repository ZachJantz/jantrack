import hou
import os
import subprocess
from glob import glob


usr_home = os.path.expanduser("~")
#Absolute network path
RIDERS_PROJECT_PATH = os.path.join(usr_home, 
                                "mount/CollaborativeSpace/rider-project/rider")
                                
hou.hipFile.saveAndIncrementFileName()
new_hip_name = hou.hipFile.basename()
NEW_HIP_PATH = hou.hipFile.path()

NETWORK_HIP_PATH = os.path.join(RIDERS_PROJECT_PATH, new_hip_name)

subprocess.run(["cp",NEW_HIP_PATH, NETWORK_HIP_PATH])



shot_name = new_hip_name.split("_v")[0]
local_search = os.path.join(os.path.dirname(NEW_HIP_PATH), shot_name) + "*"
network_search = os.path.join(RIDERS_PROJECT_PATH, shot_name) + "*" 


local_versions = glob(local_search)
network_versions = glob(network_search)

for local_version in local_versions:

    if len(local_versions)>10:

        oldest_local_version = local_versions.pop(0)
        os.remove(oldest_local_version)

for network_version in network_versions:

    if len(network_versions)>10:

        oldest_network_version = network_versions.pop(0)
        os.remove(oldest_network_version)