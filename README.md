# README #

This is an alternative client downloader for Elite: Dangerous.  Although the official launcher is still required to log in and play, this script allows players to bypass the launcher's tendency to be unresponsive or stall out for very long periods while downloading and therefore get the game much faster with less frustration.

### Requirements ###

* Python 2.x (made with 2.7, but should work with earlier versions)

### Usage ###

1. Set manifestURL to the URL of the latest patch manifest.
2. Set downloadDir to the installation directory for Elite: Dangerous (e.g., "E:\\Program Files (x86)\\Frontier\\EDLaunch\\Products\\FORC-FDEV-D-1002").  Note the use of \\ versus \ because Python and Windows.
3. Run the script and enjoy your launcherless download!

### Troubleshooting ###
#### Is there any way to verify the files were downloaded correctly? ####
Log into the official launcher, then click your account name (top) > Validate Game Files.