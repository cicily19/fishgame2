Features
3D Sphere Split Animation: An Earth-like sphere splits horizontally with two halves moving aside.
Interactive Tree Model: A rotating low-poly tree appears in between the sphere halves.
Background Music: Christmas-themed background music plays while the sphere is split.
User Interaction: Toggle sphere split, rotate view, and zoom in/out using mouse interactions.

Requirements:
Python 3.x,
Pygame,
PyOpenGL,
NumPy,

Installation
Clone the Repository
Command: git clone https://github.com/your-username/3d-sphere-split-animation.git

Install Dependencies
Command:pip install pygame pyopengl numpy

Add Background Music
Download from:https://pixabay.com/music/christmas-deck-the-halls-background-christmas-music-for-video-40-second-253222/

Usage
Run the script to start the animation:

Command: python draw_sphere.py

Controls
Left Mouse Click: Toggle sphere split / play or stop background music.
Mouse Drag: Rotate the sphere.
Mouse Scroll: Zoom in (scroll up) or zoom out (scroll down).

Code Structure
Sphere Creation: create_sphere() generates the vertices and colors for both halves of the sphere.

Drawing Functions:
draw_sphere_half() renders each sphere half.
draw_low_poly_tree(), draw_pyramid(), and draw_star() create a rotating low-poly tree model with a star on top.

Main Loop: Handles events, updates transformations, and renders frames continuously.
