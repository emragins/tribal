import ika
#Portions of the code originally created by Hatchet.

def loadFrames(x,y,img, width, height, span,xdist,ydist, numtiles):    
	"""
	This is a simple function that takes any image that's formatted like a tileset and rips the tiles into a
	list which is then returned. 
	img: image to rip from
	width/height: width and height of a single tile
	span: how many tiles per row
	numtiles: number of tiles to rip
	"""
	tiles=[]
	bigImage = ika.Canvas(img)
	i2 = 0
	i3 = 0
	
	for i in range(numtiles):
		tile = ika.Canvas(width, height)
		bigImage.Clip((x+((i2*width)+(i2*xdist))),(y+((i3*height)+(i3*ydist))),width,height)
		#bigImage.Blit(tile, -1-((width+1)*(i%span)), -1-((height+1)*(i%span)), ika.Opaque)
		bigImage.Blit(tile, 0, 0, ika.Opaque)
		tiles.append(ika.Image(tile))
		
		i2+=1
		if i2 >= span:
			i3+=1
			i2=0
	#ika.Exit(str(tiles))
	return tiles