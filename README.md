AnimationEditor
===============

Animation editor; simplifies the process of extracting vector animations from videos for machine learning

![example](img/anim-editor.png)

This project has been used by the [procedural locomotion project](https://github.com/hmoraldo/ProceduralLocomotion). For the procedural locomotion project, we built a dataset of 25 walking animations (each with multiple frames). Then we used machine learning to compute a simple algorithm for generating continous walking animations.

(the background image used for the screenshot is a public domain image from [publicdomainpictures.net](http://www.publicdomainpictures.net/view-image.php?image=11855&picture=walking-on-the-beach))

Notes
-----

To run, execute "python MainMenu.py".

The main menu shows 5 buttons:

* New: creates a new json file. The program allows you to select what are the frames from the video you want to extract vertex information from, add as many named vertices as needed, and set their default positions.

* Edit vertices: opens a json file created with the New button, and allows the user to change the animation properties (including position and number of vertices).

* Edit lines: opens a json file and allows the user to create lines between vertices, with different colors. Having lines between vertices makes the animation process easier and more intuitive.

* Edit animations: allows the user to go through all the frames of an animation, selecting the vertex positions for each.

* Edit ref vertex: press this button after selecting the right reference vertex number. The reference vertex will be used as the origin for all frames; the edit ref vertex menu lets the user edit the position of the reference vertex in a simpler way than by using the edit vertices menu.
