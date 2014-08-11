import Tkinter as tk
import tkFileDialog as filedialog

import AnimationEditor, LineEditor, VertexEditor

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

def makeButton(window, text, row, handler):
	btn = tk.Button(window, text=text)
	btn.grid(row=row, sticky=tk.W+tk.N+tk.E+tk.S)
	btn.bind("<ButtonRelease-1>", handler)
	return btn

def mainMenu(window):
	window.title("Main menu")

	btnNewFile = makeButton(window, "New", 0, btnNewFileClick)
	btnEditVertices = makeButton(window, "Edit vertices", 1, btnEditVerticesClick)
	btnEditLines = makeButton(window, "Edit lines", 2, btnEditLinesClick)
	btnEditAnimations = makeButton(window, "Edit animations", 3, btnEditAnimationsClick)

	window.mainloop()

if __name__ == "__main__":
	mainMenu(tk.Tk())
