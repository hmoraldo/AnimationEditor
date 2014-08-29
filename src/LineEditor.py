import glob
import json
import Tkinter as tk
import Utils
from PIL import Image, ImageTk

FileName = None
ImageGlob = None
Vertices = None
CurrentLine = None
Lines = None
Frames = None

canvas = None
lblLine = None
lblVertex1 = None
lblVertex2 = None
color = None

def fillEditorWindow(window):
	global canvas, lblLine, lblVertex1, lblVertex2, color

	window.title("Line Editor")

	canvas = tk.Canvas(window)
	canvas.grid(row=0, column=0, columnspan=7)
	canvas.config(width=700, height=700)

	tk.Label(window, text="Line #:").grid(row=1, column=0)
	lblLine = Utils.MakeArrowButtons(window, 1, 1, btnPrevLineClick, btnNextLineClick)

	btnAddLine = tk.Button(window, text="Add line")
	btnAddLine.grid(row=2, column=0)
	btnAddLine.bind("<ButtonRelease-1>", btnAddLineClick)
	btnRemoveLine = tk.Button(window, text="Remove line")
	btnRemoveLine.grid(row=2, column=1, columnspan=3)
	btnRemoveLine.bind("<ButtonRelease-1>", btnRemoveLineClick)

	tk.Label(window, text="Vertex 1:").grid(row=3, column=0)
	lblVertex1 = Utils.MakeArrowButtons(window, 3, 1, btnPrevVertex1Click, btnNextVertex1Click)

	tk.Label(window, text="Vertex 2:").grid(row=4, column=0)
	lblVertex2 = Utils.MakeArrowButtons(window, 4, 1, btnPrevVertex2Click, btnNextVertex2Click)

	tk.Label(window, text="Color:").grid(row=5, column=0)
	color = tk.StringVar()
	color.set("black")
	color.trace("w", optColorChanged)
	optColor = tk.OptionMenu(window, color, "black", "white", "red", "blue", "green")
	optColor.grid(row=5, column=1, columnspan=3)

	btnSave = tk.Button(window, text="Save")
	btnSave.grid(row=6, column=4)
	btnSave.bind("<ButtonRelease-1>", btnSaveClick)

	updateData()
	updateImage()

	window.mainloop()

def btnPrevLineClick(event):
	global CurrentLine
	if CurrentLine > 0:
		CurrentLine -= 1
	updateData()
	updateImage()

def btnNextLineClick(event):
	global CurrentLine, Lines
	if CurrentLine < len(Lines) - 1:
		CurrentLine += 1
	updateData()
	updateImage()

def btnAddLineClick(event):
	global Lines, CurrentLine
	Lines.append(Utils.NewLine(Vertices))
	CurrentLine = len(Lines) - 1
	updateData()
	updateImage()

def btnRemoveLineClick(event):
	global Lines, CurrentLines
	if len(Lines) > 1:
		del Lines[Line]
		if CurrentLine >= len(Lines):
			CurrentLine -= 1
	updateData()
	updateImage()


def optColorChanged(*args):
	global Lines, CurrentLine, color
	Lines[CurrentLine]["color"] = color.get()
	updateImage()

def btnPrevVertex1Click(event):
	global Lines, CurrentLine
	fromV = Lines[CurrentLine]["from"]
	if fromV > 0:
		fromV -= 1
	Lines[CurrentLine]["from"] = fromV
	updateData()
	updateImage()

def btnNextVertex1Click(event):
	global Lines, CurrentLine
	fromV = Lines[CurrentLine]["from"]
	if fromV < len(Vertices) - 1:
		fromV += 1
	Lines[CurrentLine]["from"] = fromV
	updateData()
	updateImage()

def btnPrevVertex2Click(event):
	global Lines, CurrentLine
	toV = Lines[CurrentLine]["to"]
	if toV > 0:
		toV -= 1
	Lines[CurrentLine]["to"] = toV
	updateData()
	updateImage()

def btnNextVertex2Click(event):
	global Lines, CurrentLine
	toV = Lines[CurrentLine]["to"]
	if toV < len(Vertices) - 1:
		toV += 1
	Lines[CurrentLine]["to"] = toV
	updateData()
	updateImage()

def btnSaveClick(event):
	global ImageGlob, Vertices, FileName, Lines, Frames
	Utils.Save(FileName, ImageGlob, Vertices, Lines, Frames)

def updateData():
	global lblLine, lblVertex1, lblVertex2
	global Lines, CurrentLine
	lblLine["text"] = str(CurrentLine)
	lblVertex1["text"] = str(Lines[CurrentLine]["from"]) + " (" + str(Vertices[Lines[CurrentLine]["from"]]["name"]) + ")"
	lblVertex2["text"] = str(Lines[CurrentLine]["to"]) + " (" + str(Vertices[Lines[CurrentLine]["to"]]["name"]) + ")"

def updateImage():
	global canvas, Vertices, ImageGlob, Lines, CurrentLine

	noVertex = -1
	currentImage = None
	if ImageGlob != None:
		images = glob.glob(ImageGlob)
		images.sort()
		if len(images) > 0:
			currentImage = images[0]

	Utils.UpdateImage(canvas, 0, 0, Vertices, Lines, currentImage, noVertex, CurrentLine)

def OpenFromFile(window, filename):
	global FileName, CurrentLine, ImageGlob, Vertices, Lines, CurrentLine, Frames

	FileName = filename
	CurrentLine = 0

	f = open(filename)
	data = json.load(f)
	f.close()	

	ImageGlob = data["imageGlob"]
	Vertices = data["vertices"]
	Lines = data["lines"]
	Frames = data["frames"]

	if len(Lines) == 0:
		Lines = [Utils.NewLine(Vertices)]

	fillEditorWindow(window)


if __name__ == "__main__":
	OpenFromFile(tk.Tk(), "data/testfile.json")


