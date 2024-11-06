import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Initialize Pygame and OpenGL
pygame.init()
window = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Sphere Split Animation")

# Set up the OpenGL environment
glEnable(GL_DEPTH_TEST)
glClearColor(1, 1, 1, 1)  # White background

# Set up camera (basically the position of the sphere)
gluPerspective(45, (800 / 600), 0.1, 50.0)
glTranslatef(0.0, 0.0, -4)

# Split distance and toggle
split_distance = 0
split = False

# Rotation and zoom controls
rotation_x, rotation_y = 0, 0
zoom = -4

# Tree rotation angle
tree_rotation_angle = 0

# Function to create sphere vertices and colors
def create_sphere(radius, segments, rings, top_half=True):
    vertices = []
    colors = []

    # Only render either the top or the bottom half based on top_half argument
    for i in range(rings // 2) if top_half else range(rings // 2, rings):
        theta1 = i * np.pi / rings
        theta2 = (i + 1) * np.pi / rings

        for j in range(segments):
            phi1 = j * 2 * np.pi / segments
            phi2 = (j + 1) * 2 * np.pi / segments

            # First triangle
            x1, y1, z1 = radius * np.sin(theta1) * np.cos(phi1), radius * np.cos(theta1), radius * np.sin(theta1) * np.sin(phi1)
            x2, y2, z2 = radius * np.sin(theta2) * np.cos(phi1), radius * np.cos(theta2), radius * np.sin(theta2) * np.sin(phi1)
            x3, y3, z3 = radius * np.sin(theta2) * np.cos(phi2), radius * np.cos(theta2), radius * np.sin(theta2) * np.sin(phi2)

            vertices.extend([x1, y1, z1, x2, y2, z2, x3, y3, z3])
            colors.extend([0.0, 0.6, 0.8] * 3)

            # Second triangle
            x4, y4, z4 = radius * np.sin(theta1) * np.cos(phi2), radius * np.cos(theta1), radius * np.sin(theta1) * np.sin(phi2)
            vertices.extend([x1, y1, z1, x3, y3, z3, x4, y4, z4])
            colors.extend([0.0, 0.6, 0.8] * 3)

    return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32)

# Load the vertices for each half
top_vertices, top_colors = create_sphere(1, 32, 16, top_half=True)
bottom_vertices, bottom_colors = create_sphere(1, 32, 16, top_half=False)

# Function to draw a sphere half
def draw_sphere_half(vertices, colors):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 3)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)

# Function to draw a low-poly, layered tree
def draw_low_poly_tree():
    global tree_rotation_angle
    tree_rotation_angle += 1  # Rotate the tree slowly

    # Define layers of the tree with decreasing size as they go up
    tree_layers = [
        (0.5, 0.2, 0.0),  # Bottom layer (radius, height, y_offset)
        (0.4, 0.2, 0.2),
        (0.3, 0.2, 0.4),
        (0.2, 0.2, 0.6)
    ]

    # Rotate and draw each layer
    for radius, height, y_offset in tree_layers:
        glPushMatrix()
        glRotatef(tree_rotation_angle, 0, 1, 0)  # Rotate each layer
        glColor3f(0.0, 0.8, 0.0)  # Green color for the tree
        glTranslatef(0, y_offset, 0)
        draw_pyramid(radius, height)
        glPopMatrix()

    # Draw the trunk
    glPushMatrix()
    glColor3f(0.55, 0.27, 0.07)  # Brown color for the trunk
    glTranslatef(0, -0.1, 0)
    glRotatef(-90, 1, 0, 0)  # Align cylinder vertically
    gluCylinder(gluNewQuadric(), 0.1, 0.07, 0.8, 20, 20)
    glPopMatrix()

    # Draw the star on top of the tree
    glPushMatrix()
    glTranslatef(0, 0.75, 0)  # Position the star above the top layer
    draw_star(0.1)  # Draw a small star
    glPopMatrix()

# Function to draw a pyramid (used for each tree layer)
def draw_pyramid(radius, height):
    glBegin(GL_TRIANGLES)
    for i in range(4):
        angle = np.pi / 2 * i
        next_angle = np.pi / 2 * (i + 1)

        # Apex
        glVertex3f(0, height, 0)

        # Base corners
        glVertex3f(radius * np.cos(angle), 0, radius * np.sin(angle))
        glVertex3f(radius * np.cos(next_angle), 0, radius * np.sin(next_angle))
    glEnd()

# Function to draw a small 3D star on top of the tree
def draw_star(size):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.84, 0.0)  # Gold color for the star

    # Define vertices for a simple 3D star shape
    for angle in range(0, 360, 72):  # Five points of the star
        angle_rad = np.radians(angle)
        next_angle_rad = np.radians(angle + 144)  # Skip to create star effect

        # Center point
        glVertex3f(0, size, 0)

        # Two outer points
        glVertex3f(size * np.cos(angle_rad), 0, size * np.sin(angle_rad))
        glVertex3f(size * np.cos(next_angle_rad), 0, size * np.sin(next_angle_rad))
    glEnd()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            split = not split
            if not split:
                split_distance = 0  # Reset split distance if we are merging back
        elif event.type == MOUSEMOTION:
            # Rotate the sphere based on mouse movement
            if pygame.mouse.get_pressed()[0]:
                rotation_x += event.rel[1]  # Rotate along x-axis
                rotation_y += event.rel[0]  # Rotate along y-axis
        elif event.type == MOUSEBUTTONDOWN:
            # Zoom in/out with scroll wheel
            if event.button == 4:  # Scroll up
                zoom += 0.2
            elif event.button == 5:  # Scroll down
                zoom -= 0.2

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Apply the camera transformations
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glTranslatef(0.0, 0.0, zoom)  # Zoom control
    glRotatef(rotation_x, 1, 0, 0)  # Rotate x
    glRotatef(rotation_y, 0, 1, 0)  # Rotate y

    # Apply the split animation
    if split:
        if split_distance < 1.5:  # Max split distance
            split_distance += 0.05
    else:
        if split_distance > 0:  # Merging animation
            split_distance -= 0.05

    # Draw the top half
    glPushMatrix()
    glTranslatef(0, split_distance / 2, 0)  # Move up
    draw_sphere_half(top_vertices, top_colors)
    glPopMatrix()

    # Draw the bottom half
    glPushMatrix()
    glTranslatef(0, -split_distance / 2, 0)  # Move down
    draw_sphere_half(bottom_vertices, bottom_colors)
    glPopMatrix()

    # Draw the tree in between the two halves
    if split:
        glPushMatrix()
        glTranslatef(0, -0.25, 0)  # Position tree
        draw_low_poly_tree()
        glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()