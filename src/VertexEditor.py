import glob
import json
import Tkinter as tk
import tkFileDialog as filedialog
import Utils

Vertices = None
FileName = None
Lines = None
Frames = None

CurrentVertex = 0
ImageGlob = None
VertexName = None

lblVertex = None
canvas = None

def fillEditorWindow(window):
	global ImageGlob, VertexName, lblVertex, canvas

	window.title("Vertex Editor")

	canvas = tk.Canvas(window)
	canvas.grid(row=0, column=0, columnspan=7)
	canvas.bind("<ButtonPress-1>", canvasDown)
	canvas.config(width=700, height=700)

	tk.Entry(window, textvariable=ImageGlob).grid(row=1, column=0, columnspan=3)

	btnSetImage = tk.Button(window, text="Update image")
	btnSetImage.grid(row=1, column=3)
	btnSetImage.bind("<ButtonRelease-1>", btnSetImageClick)

	tk.Entry(window, textvariable=VertexName).grid(row=2, column=0, columnspan=3)

	btnSetVertexName = tk.Button(window, text="Set vertex name")
	btnSetVertexName.grid(row=2, column=3)
	btnSetVertexName.bind("<ButtonRelease-1>", btnSetVertexNameClick)

	lblVertex = Utils.MakeArrowButtons(window, 3, 0, btnPrevVertexClick, btnNextVertexClick)

	if len(Lines) == 0 and len(Frames) == 0:
		btnRemoveVertex = tk.Button(window, text="Remove vertex")
		btnRemoveVertex.grid(row=4, column=0, columnspan=3)
		btnRemoveVertex.bind("<ButtonRelease-1>", btnRemoveVertexClick)

	btnAddVertex = tk.Button(window, text="Add vertex")
	btnAddVertex.grid(row=5, column=0, columnspan=3)
	btnAddVertex.bind("<ButtonRelease-1>", btnAddVertexClick)

	btnSave = tk.Button(window, text="Save")
	btnSave.grid(row=6, column=3, columnspan=3)
	btnSave.bind("<ButtonRelease-1>", btnSaveClick)

	updateVertexData()
	updateImage()

	window.mainloop()

def canvasDown(event):
	global CurrentVertex, Vertices
	Vertices[CurrentVertex]["x"] = event.x
	Vertices[CurrentVertex]["y"] = event.y
	updateImage()

def btnSetImageClick(event):
	updateImage()

def btnSetVertexNameClick(event):
	global CurrentVertex, Vertices, VertexName
	Vertices[CurrentVertex]["name"] = VertexName.get()

def updateVertexData():
	global CurrentVertex, Vertices, lblVertex
	lblVertex["text"] = str(CurrentVertex)
	VertexName.set(Vertices[CurrentVertex]["name"])

def btnPrevVertexClick(event):
	global CurrentVertex
	if CurrentVertex > 0:
		CurrentVertex -= 1
		updateVertexData()
		updateImage()

def btnNextVertexClick(event):
	global CurrentVertex, Vertices
	if CurrentVertex < len(Vertices) - 1:
		CurrentVertex += 1
		updateVertexData()
		updateImage()

def btnRemoveVertexClick(event):
	global Vertices, CurrentVertex
	if len(Vertices) > 1:
		del Vertices[CurrentVertex]
		if CurrentVertex >= len(Vertices):
			CurrentVertex -= 1
	updateVertexData()
	updateImage()


def btnAddVertexClick(event):
	global Vertices, CurrentVertex
	Vertices.append(Utils.NewVertex())
	CurrentVertex = len(Vertices) - 1
	updateVertexData()
	updateImage()

def btnSaveClick(event):
	global ImageGlob, Vertices, FileName, Lines, Frames
	Utils.Save(FileName, ImageGlob.get(), Vertices, Lines, Frames)

def updateImage():
	global canvas, Vertices, ImageGlob, Lines

	currentImage = None
	if ImageGlob != None:
		images = glob.glob(ImageGlob.get())
		images.sort()
		if len(images) > 0:
			currentImage = images[0]

	CurrentLine = -1

	Utils.UpdateImage(canvas, 0, 0, Vertices, Lines, currentImage, CurrentVertex, CurrentLine)


def OpenFromFile(window, filename, newFile):
	global ImageGlob, Vertices, FileName, CurrentVertex, VertexName, Lines, Frames

	FileName = filename
	CurrentVertex = 0

	if newFile:
		vertices = [Utils.NewVertex()]
		data = {
			"imageGlob" : "",
			"vertices" : vertices,
			"lines" : [],
			"frames" : []
		}
	else:
		f = open(filename)
		data = json.load(f)
		f.close()	

	VertexName = tk.StringVar()
	ImageGlob = tk.StringVar()
	ImageGlob.set(data["imageGlob"])
	Vertices = data["vertices"]
	Lines = data["lines"]
	Frames = data["frames"]

	fillEditorWindow(tk.Toplevel())


if __name__ == "__main__":
	OpenFromFile(tk.Tk(), "data/testfile.json", newFile=True)

