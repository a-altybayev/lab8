import pygame
import sys
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Drawing Tool")
screen.fill((255, 255, 255))

current_tool = "rectangle"  # Options: rectangle, square, circle, right_triangle, equilateral_triangle, rhombus, eraser, brush
draw_color = (0, 0, 0)
brush_size = 5
start_pos = None

print("Press R for Rectangle, S for Square, C for Circle, T for Right Triangle, E for Equilateral Triangle, D for Rhombus, B for Brush, Z for Eraser")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_tool = "rectangle"
                print("Selected tool: Rectangle")
            elif event.key == pygame.K_s:
                current_tool = "square"
                print("Selected tool: Square")
            elif event.key == pygame.K_c:
                current_tool = "circle"
                print("Selected tool: Circle")
            elif event.key == pygame.K_t:
                current_tool = "right_triangle"
                print("Selected tool: Right Triangle")
            elif event.key == pygame.K_e:
                current_tool = "equilateral_triangle"
                print("Selected tool: Equilateral Triangle")
            elif event.key == pygame.K_d:
                current_tool = "rhombus"
                print("Selected tool: Rhombus")
            elif event.key == pygame.K_b:
                current_tool = "brush"
                print("Selected tool: Brush")
            elif event.key == pygame.K_z:
                current_tool = "eraser"
                print("Selected tool: Eraser")
            elif event.key == pygame.K_g:
                draw_color = (0,255,0)
                print("Selected color: Green")
            elif event.key == pygame.K_f:
                draw_color = (255,0,0)
                print("Selected color: Red")
            elif event.key == pygame.K_h:
                draw_color = (0,0,255)
                print("Selected color: Blue")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0] and current_tool == "brush":
                pygame.draw.circle(screen, draw_color, event.pos, brush_size)
            if pygame.mouse.get_pressed()[0] and current_tool == "eraser":
                pygame.draw.circle(screen, (255,255,255), event.pos, 50)
        elif event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos
            if current_tool == "rectangle":
                pygame.draw.rect(screen, draw_color, (*start_pos, end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
            elif current_tool == "square":
                side_length = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                pygame.draw.rect(screen, draw_color, (start_pos[0], start_pos[1], side_length, side_length))
            elif current_tool == "circle":
                radius = int(math.sqrt((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) / 2)
                center = ((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2)
                pygame.draw.circle(screen, draw_color, center, radius)
            elif current_tool == "right_triangle":
                pygame.draw.polygon(screen, draw_color, [start_pos, (start_pos[0], end_pos[1]), end_pos])
            elif current_tool == "equilateral_triangle":
                height = math.sqrt(3) * abs(end_pos[0] - start_pos[0])
                point1 = (start_pos[0], start_pos[1] - height // 2)
                point2 = (start_pos[0] - abs(end_pos[0] - start_pos[0]) // 2, start_pos[1] + height // 2)
                point3 = (start_pos[0] + abs(end_pos[0] - start_pos[0]) // 2, start_pos[1] + height // 2)
                pygame.draw.polygon(screen, draw_color, [point1, point2, point3])
            elif current_tool == "rhombus":
                dx = abs(end_pos[0] - start_pos[0]) // 2
                dy = abs(end_pos[1] - start_pos[1]) // 2
                center = (start_pos[0] + dx, start_pos[1] + dy)
                vertices = [
                    (center[0], start_pos[1]),
                    (end_pos[0], center[1]),
                    (center[0], start_pos[1] + 2 * dy),
                    (start_pos[0], center[1])
                ]
                pygame.draw.polygon(screen, draw_color, vertices)
                start_pos = None
    pygame.display.flip()
pygame.quit()
sys.exit()