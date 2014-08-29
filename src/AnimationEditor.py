import json, glob
from PIL import Image, ImageTk
import Tkinter as tk
import Utils

canvas = None
lblImage = None
lblVertex = None
FileName = None
CurrentFrame = None # current frame number
CurrentVertex = None
FrameName = None
Images = None # the image names
ImageGlob = None
Vertices = None
Lines = None
Frames = None # the actual frame information

def fillEditorWindow(window):
	global canvas, lblImage, lblVertex, FrameName

	window.title("Animation Editor")
	window.bind("<Left>", btnPrevVertexClick)
	window.bind("<Right>", btnNextVertexClick)

	canvas = tk.Canvas(window)
	canvas.grid(row=0, column=0, columnspan=7)
	canvas.bind("<ButtonPress-1>", canvasDown)
	canvas.config(width=700, height=700)

	tk.Entry(window, textvariable=FrameName).grid(row=1, column=1, columnspan=3)
	btnSetFrameName = tk.Button(window, text="Set name")
	btnSetFrameName.grid(row=1, column=4, columnspan=2)
	btnSetFrameName.bind("<ButtonRelease-1>", btnSetFrameNameClick)

	tk.Label(window, text="Image:").grid(row=2, column=0)
	lblImage = Utils.MakeArrowButtons(window, 2, 1, btnPrevImageClick, btnNextImageClick)

	tk.Label(window, text="Vertex:").grid(row=3, column=0)
	lblVertex = Utils.MakeArrowButtons(window, 3, 1, btnPrevVertexClick, btnNextVertexClick)

	btnSave = tk.Button(window, text="Save")
	btnSave.grid(row=4, column=4)
	btnSave.bind("<ButtonRelease-1>", btnSaveClick)

	updateData()
	updateImage()

	window.mainloop()

def completeFrameData(index):
	global Frames, Vertices

	for i in range(len(Frames[index]["vertices"]), len(Vertices)):
		Frames[index]["vertices"].append(Vertices[i])

def btnSetFrameNameClick(event):
	global FrameName, CurrentFrame, Frames
	Frames[CurrentFrame]["name"] = FrameName.get()

def btnPrevImageClick(event):
	global CurrentFrame
	if CurrentFrame > 0:
		CurrentFrame -= 1
	completeFrameData(CurrentFrame)

	updateData()
	updateImage()

def btnNextImageClick(event):
	global CurrentFrame, Images, Frames
	if CurrentFrame < len(Images) - 1:
		CurrentFrame += 1
	if CurrentFrame >= len(Frames):
		if CurrentFrame == len(Frames):
			Frames.append(Utils.NewFrame(Frames))
		else:
			print "Error, can't edit this frame"
			quit()

	completeFrameData(CurrentFrame)

	updateData()
	updateImage()

def btnPrevVertexClick(event):
	global CurrentVertex

	if CurrentVertex > 0:
		CurrentVertex -= 1
	updateData()
	updateImage()

def btnNextVertexClick(event):
	global CurrentVertex, Vertices

	if CurrentVertex < len(Vertices) - 1:
		CurrentVertex += 1
	updateData()
	updateImage()

def canvasDown(event):
	global CurrentVertex, Vertices, CurrentFrame, Frames
	Frames[CurrentFrame]["vertices"][CurrentVertex]["x"] = event.x
	Frames[CurrentFrame]["vertices"][CurrentVertex]["y"] = event.y
	updateImage()

def btnSaveClick(event):
	global ImageGlob, Vertices, FileName, Lines, Frames
	Utils.Save(FileName, ImageGlob, Vertices, Lines, Frames)

def updateData():
	global lblImage, lblVertex, CurrentFrame, CurrentVertex, FrameName
	lblImage["text"] = str(CurrentFrame) + " (" + str(Images[CurrentFrame]) + ")"
	lblVertex["text"] = str(CurrentVertex) + " (" + str(Vertices[CurrentVertex]["name"]) + ")"
	FrameName.set(Frames[CurrentFrame]["name"])

def updateImage():
	global canvas, Vertices, Lines, Frames, Images, CurrentFrame, CurrentVertex

	noSelection = -1
	currentImage = Images[CurrentFrame]

	Utils.UpdateImage(canvas, 0, 0, Frames[CurrentFrame]["vertices"], Lines, currentImage, CurrentVertex, noSelection)

def OpenFromFile(window, filename):
	global FrameName, FileName, CurrentFrame, CurrentVertex, Images, ImageGlob, Vertices, Lines, Frames

	FileName = filename
	CurrentVertex = 0
	CurrentFrame = 0

	f = open(filename)
	data = json.load(f)
	f.close()	

	FrameName = tk.StringVar()

	ImageGlob = data["imageGlob"]
	Vertices = data["vertices"]
	Lines = data["lines"]
	Frames = data["frames"]

	Images = glob.glob(ImageGlob)
	Images.sort()
	if len(Images) == 0:
		print "Error, no images found with the given glob"
		quit()

	if len(Frames) == 0:
		Frames = [Utils.NewFrame(Frames)]
	completeFrameData(CurrentFrame)

	fillEditorWindow(window)

if __name__ == "__main__":
	OpenFromFile(tk.Tk(), "data/testfile.json")



