# Jantrack_v01
# Zach Jantz
# 2/22/2024
# Jantrack file transfer protocol 


import subprocess
import os 


def copy_shot_assets(shot_assets, source, destination):
	"""
	Copy a shot's assets to a destination
	Inputs:
		shot_assets -  dictionary containing a shots assets
		source - source project file path string
		destination - string destination project directory path
	"""

	for asset, asset_data in shot_assets.items():
		transfer_asset_files(asset_data, source, destination)


def transfer_asset_files(asset_data, source, destination):
	"""
	Transfer an asset from one project directory to another
	Inputs:
		asset_data - diectionary containing an assets metadata
		source - source project file path string
		destination - string destination project directory path
	"""

	asset_relpath = asset_data["path"]

	asset_relparent = os.path.split(asset_relpath)[0]
	destination_parent = os.path.join(destination,asset_relparent)

	# If parent directories do not exist create them
	if os.path.isdir(destination_parent) is False:
		os.makedirs(destination_parent)

	destination_path = os.path.join(destination, asset_relpath)
	source_path = os.path.join(source, asset_relpath)

	if os.path.exists(source_path) and os.path.exists(destination_path) is False:

		if os.path.isdir(source_path):
			system_copy_directory(source_path, destination_path)
		
		else:
			system_copy_file(source_path, destination_path)


def transfer_hip(hip_network_path, destination):
	"""
	Transfer the latest hip from the network
	Inputs:
		hip_network_path - string network path of hip file
		destination - string destination project directory path
	"""

	if hip_network_path != None:

		hip_destination_path = os.path.join(destination, os.path.split(hip_network_path)[1])
		system_copy_file(hip_network_path, hip_destination_path)


def system_copy_directory(s,d):
	"""
	Transfer a directory asset using subprocess to avoid network blocks
	"""
	subprocess.run(["cp","-rT",s,d])


def system_copy_file(s,d):
	"""
	Transfer a file asset using subprocess to avoid netowrk blocks
	"""
	subprocess.run(["cp",s,d])


		










	


	






