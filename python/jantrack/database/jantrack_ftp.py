# Jantrack_v01
# Zach Jantz
# 2/22/2024
# Jantrack file transfer protocol 


import subprocess
import os 



def transfer_asset_files(asset, source, destination):


	asset_relpath = asset["path"]

	asset_relparent = os.path.split(asset_relpath)[0]
	destination_parent = os.path.join(destination,asset_relparent)

	# If parent directories do not exist create them
	if os.path.isdir(destination_parent) is False:
		os.makedirs(destination_parent)

	destination_path = os.path.join(destination, asset_relpath)
	source_path = os.path.join(destination, asset_relpath)

	if os.path.isdir(source_path):
		










	


	






