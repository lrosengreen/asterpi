import os, sys, shutil

filesToMove = []
rootDir = sys.argv[1]
dstDir = sys.argv[2]
counter = 0
for root, subFolders, files in os.walk(rootDir):
	for f in [i for i in files if os.path.splitext(i)[-1].lower() == ".jpg"]:
		srcFn = os.path.join(root, f)
		dstFn = os.path.join(dstDir, "{0:07d}.jpg".format(counter))
		shutil.copy2(srcFn, dstFn)
		counter = counter + 1
		print("{} ==> {}".format(srcFn,dstFn))



