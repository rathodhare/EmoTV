from os import walk,path
import os
ext = 'png'

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


curr_folder = path.dirname(path.realpath(__file__))
for (dirpath, dirnames, filenames) in walk(curr_folder):
	i=1
	for name in filenames:
		if (name.endswith(ext)):
			ori_dir=(dirpath+'/'+name)
			destination=(dirpath+'/'+str(i)+'.tiff')
			i+=1
			ensure_dir(destination)	
			print(ori_dir)			
			os.rename(ori_dir, destination)

	for (dirpath2, dirnames, filenames) in walk(dirpath+'/a'):
		for name in filenames:
			if (name.endswith(ext)):
				ori_dir=(dirpath2+'/'+name)
				destination=(dirpath+'/'+name)
				ensure_dir(destination)
				os.rename(ori_dir, destination)
		os.rmdir(dirpath2)
	break
