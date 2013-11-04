import sys, getopt, os
from scipy import misc
import numpy

# create a list of all files in directory 'dir'
# having the form *.png where x is a digit.
def loadImages(fromFile):
  images = []

  for root, dirs, files in os.walk(fromFile):
    for file in files:
      if file.endswith(".png"):
        path = os.path.join(root, file)
        image = misc.imread(path)
        images.append(image)
        
  return images
  
def createCompatibleTilesetImage(images):
  return numpy.zeros(shape=(512, 1024, 4), dtype=numpy.int64)

def placeInto(tilesetImage, images):
  xst = tilesetImage.shape[0]
  yst = tilesetImage.shape[1]
  xss = images[0].shape[0]
  yss = images[0].shape[1]
  
  x = 0
  y = 0
  for image in images:
    tilesetImage[x:(x+xss),y:(y+yss)] = image
    y += yss
    if (y + yss) > yst:
      x += xss
      y = 0

def main(argv):
  try:
    opts, args = getopt.getopt(argv, "")
  except getopt.GetoptError:
    print 'tileset [tilesetFile] [fromFile] .. [fromFile]'
    sys.exit(2)

  tilesetFile = args[0]
  fromFile = args[1]
  
  print "fromFile: " + fromFile + " tilesetFile: " + tilesetFile
  
  images = loadImages(fromFile)
  tilesetImage = createCompatibleTilesetImage(images)
  placeInto(tilesetImage, images)
  
  misc.imsave(tilesetFile, tilesetImage)
  
if __name__ == "__main__":
  main(sys.argv[1:])