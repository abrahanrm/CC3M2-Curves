import numpy as np
import pygame

from b_spline_utils import get_b_spline_points

# Frames per second
FPS = 170

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

order = 3


def get_tricked_points(points):
    _points = points.copy()

    if len(points) > 0:
        _points.insert(0, points[0])

        if len(points) >= 2:
            _points.insert(len(points), points[-1])

    return _points


def get_collided_point_index(points_rect_list, pos):
    for point in points_rect_list:
        if point.collidepoint(pos):
            return points_rect_list.index(point)

    return -1


def add_new_control_point(points):
    pos = pygame.mouse.get_pos()
    points.append(np.array([pos[0], pos[1]]))
    get_tricked_points(points)


def edit_main_point(points, index):
    pos = pygame.mouse.get_pos()
    points[index] = np.array([pos[0], pos[1]])
    return points


def draw_main_points(surface, points):
    rect_list = []

    for point in points:
        rect_list.append(pygame.draw.circle(surface, RED, (point[0], point[1]), 10))

    return rect_list


def draw_b_spline_curve(surface, main_points, b_spline_points):
    if len(b_spline_points) >= 2:
        prev = (main_points[0][0], main_points[0][1])
        last = (main_points[len(main_points) - 1][0], main_points[len(main_points) - 1][1])

        count = 0
        for point in b_spline_points:
            pygame.draw.aaline(surface, GREEN, prev, (point[0], point[1]), 1)
            prev = (point[0], point[1])
            count = count + 1

        pygame.draw.aaline(surface, GREEN, prev, last, 1)


def main():
    pygame.init()

    screen = pygame.display.set_mode((1280, 900))
    clock = pygame.time.Clock()

    points = []
    points_rect_list = []
    b_spline_points = get_b_spline_points(order, get_tricked_points(points))

    drag = False
    dragged_point_index = -1

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragged_point_index = get_collided_point_index(points_rect_list, pygame.mouse.get_pos())
                    if dragged_point_index == -1:
                        add_new_control_point(points)
                    else:
                        drag = True
                elif event.button == 3:
                    dragged_point_index = get_collided_point_index(points_rect_list, pygame.mouse.get_pos())
                    if dragged_point_index != -1:
                        points.pop(get_collided_point_index(points_rect_list, pygame.mouse.get_pos()))
            elif event.type == pygame.MOUSEBUTTONUP:
                drag = False
            elif event.type == pygame.MOUSEMOTION:
                if drag:
                    edit_main_point(points, dragged_point_index)

        screen.fill(BLACK)

        draw_b_spline_curve(screen, points, b_spline_points)
        points_rect_list = draw_main_points(screen, points)

        b_spline_points = get_b_spline_points(order, get_tricked_points(points))
        pygame.display.update()


if __name__ == '__main__':
    main()
