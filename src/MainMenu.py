import Tkinter as tk
import ttk
import tkFileDialog as filedialog
import Utils

import AnimationEditor, LineEditor, RefVertexEditor, VertexEditor

lblRefVertex = None
refVertex = None

class DialogMode():
	New = 0
	Open = 1

def selectFile(mode):
	if mode == DialogMode.Open:
		return filedialog.askopenfilename()
	else:
		return filedialog.asksaveasfilename()

def btnNewFileClick(event):
	VertexEditor.OpenFromFile(tk.Toplevel(), selectFile(DialogMode.New), newFile=True)

def btnEditVerticesClick(event):
	VertexEditor.OpenFromFile(tk.Toplevel(), selectFile(DialogMode.Open), newFile=False)

def btnEditLinesClick(event):
	LineEditor.OpenFromFile(tk.Toplevel(), selectFile(DialogMode.Open))

def btnEditAnimationsClick(event):
	AnimationEditor.OpenFromFile(tk.Toplevel(), selectFile(DialogMode.Open))

def updateRefVertex():
	global refVertex, lblRefVertex
	lblRefVertex["text"] = refVertex

def btnPrefRefVertexClick(event):
	global refVertex
	if refVertex > 0:
		refVertex -= 1
	updateRefVertex()

def btnNextRefVertexClick(event):
	global refVertex
	refVertex += 1
	updateRefVertex()

def btnEditRefVertexClick(event):
	global refVertex
	RefVertexEditor.OpenFromFile(tk.Toplevel(), selectFile(DialogMode.Open), refVertex)

def makeButton(window, text, row, handler):
	btn = tk.Button(window, text=text)
	btn.grid(row=row, sticky=tk.W+tk.N+tk.E+tk.S, columnspan=3)
	btn.bind("<ButtonRelease-1>", handler)
	return btn

def mainMenu(window):
	global lblRefVertex, refVertex

	window.title("Main menu")

	makeButton(window, "New", 0, btnNewFileClick)
	makeButton(window, "Edit vertices", 1, btnEditVerticesClick)
	makeButton(window, "Edit lines", 2, btnEditLinesClick)
	makeButton(window, "Edit animations", 3, btnEditAnimationsClick)

	ttk.Separator().grid(row=4, columnspan=3)
	tk.Label(window, text="Reference vertex:").grid(row=5, columnspan=3)
	lblRefVertex = Utils.MakeArrowButtons(window, 6, 0, btnPrefRefVertexClick, btnNextRefVertexClick)
	makeButton(window, "Edit ref vertex", 7, btnEditRefVertexClick)

	refVertex = 0
	updateRefVertex()

	window.mainloop()

if __name__ == "__main__":
	mainMenu(tk.Tk())

