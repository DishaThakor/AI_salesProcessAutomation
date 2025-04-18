from PIL import Image

img = Image.new('RGBA', (1, 1), (255, 255, 255, 0))  # transparent 1x1
img.save('transparent.gif', 'GIF')
