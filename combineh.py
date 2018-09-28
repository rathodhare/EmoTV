import sys
from PIL import Image
#path='surprisedf.png'
def make(path):

	images = map(Image.open, ['1.jpg', path])
	widths, heights = zip(*(i.size for i in images))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	x_offset = 0
	for im in images:
  		new_im.paste(im, (x_offset,0))
  		x_offset += im.size[0]

	new_im.save('test.jpg')

if __name__=='__main__':
	make(path)
