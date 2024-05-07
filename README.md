import math
import pygame
import numpy as np

WHITE = 255, 255, 255
RED = 255, 0, 0
BLACK = 0, 0, 0

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('3D')

points = []

scale = 100

angle = 0

cirle_pos = [WIDTH / 2, HEIGHT / 2]

points.append(np.matrix([[-1], [-1], [1]]))
points.append(np.matrix([[1], [-1], [1]]))
points.append(np.matrix([[1], [1], [1]]))
points.append(np.matrix([[-1], [1], [1]]))
points.append(np.matrix([[-1], [-1], [-1]]))
points.append(np.matrix([[1], [-1], [-1]]))
points.append(np.matrix([[1], [1], [-1]]))
points.append(np.matrix([[-1], [1], [-1]]))

projection_matrix = np.matrix([
   [1, 0, 0],
   [0, 1, 0]
])

rotation_z = np.matrix([
   [math.cos(angle), -math.sin(angle), 0],
   [math.sin(angle), math.cos(angle), 0],
   [0, 0, 1],
])

rotation_x = np.matrix([
   [1, 0, 0],
   [0, math.cos(angle), -math.sin(angle)],
   [0, math.sin(angle), math.cos(angle)],
])

rotation_y = np.matrix([
   [math.cos(angle), 0, -math.sin(angle)],
   [0, 1, 0],
   [-math.sin(angle), 0, math.cos(angle)],
])

projected_points = [
   [n, n] for n in range(len(points))
]

def connect_points(i, j, points):
   pygame.draw.line(screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

clock = pygame.time.Clock()

run = True
while run:
   clock.tick(60)
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           run = False
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_ESCAPE:
               run = False
   rotation_z = np.matrix([
       [math.cos(angle), -math.sin(angle), 0],
       [math.sin(angle), math.cos(angle), 0],
       [0, 0, 1],
   ])

   rotation_x = np.matrix([
       [1, 0, 0],
       [0, math.cos(angle), -math.sin(angle)],
       [0, math.sin(angle), math.cos(angle)],
   ])

   rotation_y = np.matrix([
       [math.cos(angle), 0, -math.sin(angle)],
       [0, 1, 0],
       [-math.sin(angle), 0, math.cos(angle)],
   ])
   angle += 0.01
   screen.fill(WHITE)

   i = 0
   for point in points:
       rotated_2d = np.dot(rotation_z, point.reshape((3, 1)))
       rotated_2d = np.dot(rotation_y, rotated_2d)
       projected2d = np.dot(projection_matrix, rotated_2d)
       x = int(projected2d[0][0] * scale) + cirle_pos[0]
       y = int(projected2d[1][0] * scale) + cirle_pos[1]
       projected_points[i] = [x, y]
       pygame.draw.circle(screen, RED, (x, y), 5)
       i += 1

   for p in range(4):
       connect_points(p, (p + 1) % 4, projected_points)
       connect_points(p + 4, ((p + 1) % 4) + 4, projected_points)
       connect_points(p, (p + 4), projected_points)
   pygame.display.update()

