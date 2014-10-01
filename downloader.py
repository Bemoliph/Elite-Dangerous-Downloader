import gzip
import hashlib
import os
import urllib

from xml.etree import ElementTree

manifestURL = "http://cdn.zaonce.net/elitedangerous/win/manifests/Beta2.0_Final_Final+%282014.10.01.43904%29.xml.gz"
downloadDir = "E:\\Program Files (x86)\\Frontier\\EDLaunch\\Products\\FORC-FDEV-D-1002"

def generateDirectories(path):
	dir = os.path.dirname(path)
	
	if not os.path.isdir(dir):
		os.makedirs(dir)

def alreadyHaveAsset(downloadPath, assetHash):
	if os.path.isfile(downloadPath):
		# Asset exists on disk, but need to check version
		sha1 = hashlib.sha1()
		sha1.update(open(downloadPath, "rb").read())
		localHash = sha1.hexdigest()
		
		return localHash == assetHash
	else:
		# Asset doesn't exist on disk
		return False

# Set up the download directory
generateDirectories(downloadDir)

# Get the patch manifest
manifestPath = urllib.urlretrieve(manifestURL, os.path.join(downloadDir, manifestURL.rsplit("/", 1)[-1]))[0]
manifest = ElementTree.fromstring(gzip.open(manifestPath, "rb").read())
assetCount = len(manifest)

# Get assets
for assetNumber, asset in enumerate(manifest.getchildren()):
	assetURL = asset.find("Download").text
	assetSize = float(asset.find("Size").text) / 1048576.0 # Bytes -> Megabytes
	assetHash = asset.find("Hash").text
	assetRelPath = asset.find("Path").text
	downloadPath = os.path.join(downloadDir, assetRelPath)
	
	generateDirectories(downloadPath)
	
	if alreadyHaveAsset(downloadPath, assetHash):
		print "Skipping file %d of %d: (%.2f MB) %s" % (assetNumber+1, assetCount, assetSize, assetRelPath)
	else:
		print "Downloading file %d of %d: (%.2f MB) %s" % (assetNumber+1, assetCount, assetSize, assetRelPath)
		urllib.urlretrieve(assetURL, downloadPath)
