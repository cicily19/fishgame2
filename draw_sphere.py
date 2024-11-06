import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Initialize Pygame, OpenGL, and mixer for audio
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Sphere Split Animation")

# Load background music for the animation
music_path = "C:\\Users\\saleh\\Downloads\\deck-the-halls-background-christmas-music-for-video-40-second-253222.mp3"
pygame.mixer.music.load(music_path)

# Set up OpenGL settings, enabling depth testing and setting background color to white
glEnable(GL_DEPTH_TEST)
glClearColor(1, 1, 1, 1)  # White background

# Set up the camera perspective
gluPerspective(45, (800 / 600), 0.1, 50.0)
glTranslatef(0.0, 0.0, -4)  # Initial zoom to place sphere in view

# Initialize split distance and toggle for sphere halves
split_distance = 0
split = False

# Initialize rotation and zoom values
rotation_x, rotation_y = 0, 0
zoom = -4

# Initialize the angle for rotating the tree
tree_rotation_angle = 0


# Function to create sphere vertices and colors
def create_sphere(radius, segments, rings, top_half=True):
    vertices = []
    colors = []

    # Generate vertices and colors for the sphere
    for i in range(rings // 2) if top_half else range(rings // 2, rings):
        theta1 = i * np.pi / rings
        theta2 = (i + 1) * np.pi / rings

        for j in range(segments):
            phi1 = j * 2 * np.pi / segments
            phi2 = (j + 1) * 2 * np.pi / segments

            # Calculate vertices for sphere triangles
            x1, y1, z1 = radius * np.sin(theta1) * np.cos(phi1), radius * np.cos(theta1), radius * np.sin(
                theta1) * np.sin(phi1)
            x2, y2, z2 = radius * np.sin(theta2) * np.cos(phi1), radius * np.cos(theta2), radius * np.sin(
                theta2) * np.sin(phi1)
            x3, y3, z3 = radius * np.sin(theta2) * np.cos(phi2), radius * np.cos(theta2), radius * np.sin(
                theta2) * np.sin(phi2)
            vertices.extend([x1, y1, z1, x2, y2, z2, x3, y3, z3])
            colors.extend([0.0, 0.6, 0.8] * 3)  # Sphere color (blue-green)
            x4, y4, z4 = radius * np.sin(theta1) * np.cos(phi2), radius * np.cos(theta1), radius * np.sin(
                theta1) * np.sin(phi2)
            vertices.extend([x1, y1, z1, x3, y3, z3, x4, y4, z4])
            colors.extend([0.0, 0.6, 0.8] * 3)

    return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32)


# Load vertices and colors for the top and bottom halves of the sphere
top_vertices, top_colors = create_sphere(1, 32, 16, top_half=True)
bottom_vertices, bottom_colors = create_sphere(1, 32, 16, top_half=False)


# Function to draw each half of the sphere
def draw_sphere_half(vertices, colors):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glDrawArrays(GL_TRIANGLES, 0, len(vertices) // 3)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)


# Function to draw a low-poly tree between the sphere halves
def draw_low_poly_tree():
    global tree_rotation_angle
    tree_rotation_angle += 1  # Increment tree rotation angle

    # Define tree layers (base radius, height, and y-offset for each layer)
    tree_layers = [
        (0.5, 0.2, 0.0),
        (0.4, 0.2, 0.2),
        (0.3, 0.2, 0.4),
        (0.2, 0.2, 0.6)
    ]

    # Draw tree layers
    for radius, height, y_offset in tree_layers:
        glPushMatrix()
        glRotatef(tree_rotation_angle, 0, 1, 0)
        glColor3f(0.0, 0.8, 0.0)  # Green color for tree
        glTranslatef(0, y_offset, 0)
        draw_pyramid(radius, height)
        glPopMatrix()

    # Draw tree trunk
    glPushMatrix()
    glColor3f(0.55, 0.27, 0.07)  # Brown color for trunk
    glTranslatef(0, -0.1, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 0.1, 0.07, 0.8, 20, 20)
    glPopMatrix()

    # Draw star on top of tree
    glPushMatrix()
    glTranslatef(0, 0.75, 0)
    draw_star(0.1)
    glPopMatrix()


# Function to draw a pyramid layer of the tree
def draw_pyramid(radius, height):
    glBegin(GL_TRIANGLES)
    for i in range(4):
        angle = np.pi / 2 * i
        next_angle = np.pi / 2 * (i + 1)
        glVertex3f(0, height, 0)
        glVertex3f(radius * np.cos(angle), 0, radius * np.sin(angle))
        glVertex3f(radius * np.cos(next_angle), 0, radius * np.sin(next_angle))
    glEnd()


# Function to draw a star at the top of the tree
def draw_star(size):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.84, 0.0)  # Yellow color for star
    for angle in range(0, 360, 72):
        angle_rad = np.radians(angle)
        next_angle_rad = np.radians(angle + 144)
        glVertex3f(0, size, 0)
        glVertex3f(size * np.cos(angle_rad), 0, size * np.sin(angle_rad))
        glVertex3f(size * np.cos(next_angle_rad), 0, size * np.sin(next_angle_rad))
    glEnd()


# Main loop for running the animation
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            split = not split  # Toggle split
            if split:
                pygame.mixer.music.play(-1)  # Play music in loop
            else:
                pygame.mixer.music.stop()  # Stop music
                split_distance = 0  # Reset split distance
        elif event.type == MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:  # If left mouse held, rotate sphere
                rotation_x += event.rel[1]
                rotation_y += event.rel[0]
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up to zoom in
                zoom += 0.2
            elif event.button == 5:  # Scroll down to zoom out
                zoom -= 0.2

    # Clear screen for new frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Reset view and apply camera perspective and transformations
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glTranslatef(0.0, 0.0, zoom)
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)

    # Adjust split distance if sphere is split
    if split:
        if split_distance < 1.5:
            split_distance += 0.05
    else:
        if split_distance > 0:
            split_distance -= 0.05

    # Draw the top half of the sphere
    glPushMatrix()
    glTranslatef(0, split_distance / 2, 0)  # Move top half up
    draw_sphere_half(top_vertices, top_colors)
    glPopMatrix()

    # Draw the bottom half of the sphere
    glPushMatrix()
    glTranslatef(0, -split_distance / 2, 0)  # Move bottom half down
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
