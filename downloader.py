import gzip
import hashlib
import os
import StringIO
import sys
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

def reportFileProgress(blockNumber, blockSize, fileSize):
	blockSize /= 1048576.0 # Bytes -> Megabytes
	fileSize /= 1048576.0 # Bytes -> Megabytes
	
	currentSize = blockNumber * blockSize
	percentComplete = min(100.0 * currentSize/fileSize, 100.00)
	
	print "\r\t%.2f MB / %.2f MB (%.2f%%)" % (currentSize, fileSize, percentComplete),

def getAsset(assetNumber, assetCount, assetRelPath, assetURL, downloadPath):
	print "Downloading file %d of %d: %s" % (assetNumber, assetCount, assetRelPath)
	
	downloaded = False
	currentTry = 1
	maxTries = 5
	
	while not downloaded and currentTry <= maxTries:
		try:
			urllib.urlretrieve(assetURL, downloadPath, reportFileProgress)
			downloaded = True
		except IOError:
			print 
			print "Failed to download, retry %d of %d" % (currentTry, maxTries)
			currentTry += 1
	
	print 

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
			print "Skipping file %d of %d: %s" % (assetNumber+1, assetCount, assetRelPath)
		else:
			getAsset(assetNumber+1, assetCount, assetRelPath, assetURL, downloadPath)

def getInstallPathFromRegistry():
	import _winreg
	
	edInstallKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{696F8871-C91D-4CB1-825D-36BE18065575}_is1")
	installDir = _winreg.QueryValueEx(edInstallKey, "InstallLocation")[0]
	
	downloadDir = os.path.join(installDir, "Products\\FORC-FDEV-D-1002")
	
	return downloadDir

if __name__ == "__main__":
	# TODO: Automatically determine manifest URL
	manifestURL = "http://cdn.zaonce.net/elitedangerous/win/manifests/Gamma1.04_Final+%282014.11.28.52088%29.xml.gz"
	
	downloadDir = "C:\\Program Files (x86)\\Frontier\\EDLaunch\\Products\\FORC-FDEV-D-1002"
	if not os.path.isdir(downloadDir) and sys.platform == "win32":
		print "downloadDir (%s) does not exist.  Trying to auto-detect via Windows registry..." % downloadDir
		downloadDir = getInstallPathFromRegistry()
	
	if os.path.isdir(downloadDir):
		print "Downloading client files to %s" % downloadDir
		manifest = getPatchManifest(manifestURL)
		downloadAssets(manifest, downloadDir)
	else:
		print "downloadDir (%s) does not exist.  Make sure downloadDir is correct and that you've started the download in the official launcher at least once." % downloadDir