import json, glob
import Tkinter as tk
import Utils

RefVertex = None
canvas = None
lblImage = None
FileName = None
CurrentFrame = None
ImageGlob = None
Vertices = None
Lines = None
Frames = None
Images = None

CanvasSize = 700

def fillEditorWindow(window):
	global canvas, lblImage, CanvasSize

	window.title("Reference Vertex Editor")

	canvas = tk.Canvas(window)
	canvas.grid(row=0, column=0, columnspan=7)
	canvas.bind("<ButtonPress-1>", canvasDown)
	canvas.config(width=CanvasSize, height=CanvasSize)

	lblImage = Utils.MakeArrowButtons(window, 1, 0, btnPrevImageClick, btnNextImageClick)

	btnSave = tk.Button(window, text="Save")
	btnSave.grid(row=2, column=0)
	btnSave.bind("<ButtonRelease-1>", btnSaveClick)

	updateData()
	updateImage()

	window.mainloop()

def getOrigin():
	global Frames, CurrentFrame, RefVertex, CanvasSize
	originX = Frames[CurrentFrame]["vertices"][RefVertex]["x"] - CanvasSize / 2
	originY = Frames[CurrentFrame]["vertices"][RefVertex]["y"] - CanvasSize / 2
	return (originX, originY)

def canvasDown(event):
	global RefVertex, Vertices, CurrentFrame, Frames
	originX, originY = getOrigin()
	Frames[CurrentFrame]["vertices"][RefVertex]["x"] = event.x + originX
	Frames[CurrentFrame]["vertices"][RefVertex]["y"] = event.y + originY
	updateImage()

def btnSaveClick(event):
	global ImageGlob, Vertices, FileName, Lines, Frames
	Utils.Save(FileName, ImageGlob, Vertices, Lines, Frames)

def btnPrevImageClick(event):
	global CurrentFrame
	if CurrentFrame > 0:
		CurrentFrame -= 1
	updateData()
	updateImage()

def btnNextImageClick(event):
	global CurrentFrame, Images, Frames
	if CurrentFrame < len(Images) - 1:
		CurrentFrame += 1
	updateData()
	updateImage()

def updateData():
	global lblImage, CurrentFrame, FrameName
	lblImage["text"] = str(CurrentFrame) + " (" + str(Images[CurrentFrame]) + ")"
	if Frames[CurrentFrame]["name"] != "":
		lblImage["text"] += " - " + Frames[CurrentFrame]["name"] 

def updateImage():
	global canvas, Lines, Frames, Images, CurrentFrame, RefVertex

	noSelection = -1
	currentImage = Images[CurrentFrame]

	originX, originY = getOrigin()

	Utils.UpdateImage(canvas, originX, originY, Frames[CurrentFrame]["vertices"], Lines, currentImage, RefVertex, noSelection)

def OpenFromFile(window, filename, refVertex):
	global FileName, CurrentFrame, ImageGlob, Vertices, Lines, Frames, Images, RefVertex

	FileName = filename
	CurrentFrame = 0
	RefVertex = refVertex

	f = open(filename)
	data = json.load(f)
	f.close()	

	ImageGlob = data["imageGlob"]
	Vertices = data["vertices"]
	Lines = data["lines"]
	Frames = data["frames"]

	Images = glob.glob(ImageGlob)
	Images.sort()
	if len(Images) == 0:
		print "Error, no images found with the given glob"
		quit()

	fillEditorWindow(window)

if __name__ == "__main__":
	OpenFromFile(tk.Tk(), "data/testfile.json")



