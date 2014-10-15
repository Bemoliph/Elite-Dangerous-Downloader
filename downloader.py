import gzip
import hashlib
import StringIO
import os
import urllib

from xml.etree import ElementTree

def generateDirectories(path):
	dir = os.path.dirname(path)
	
	if not os.path.isdir(dir):
		os.makedirs(dir)

def getPatchManifest(manifestURL):
	compressedManifest = StringIO.StringIO(urllib.urlopen(manifestURL).read())
	decompressedManifest = gzip.GzipFile(fileobj=compressedManifest)
	parsedManifest = ElementTree.fromstring(decompressedManifest.read())
	
	return parsedManifest

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

def downloadAssets(manifest, downloadDir):
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

if __name__ == "__main__":
	# TODO: Automatically determine manifest URL
	manifestURL = "http://cdn.zaonce.net/elitedangerous/win/manifests/Beta2.06_Final+%282014.10.14.45307%29.xml.gz"
	# TODO: Automatically determine download directory
	downloadDir = "C:\\Program Files (x86)\\Frontier\\EDLaunch\\Products\\FORC-FDEV-D-1002"
	
	generateDirectories(downloadDir)
	manifest = getPatchManifest(manifestURL)
	downloadAssets(manifest, downloadDir)
