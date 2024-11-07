import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Enhanced Paint")
    clock = pygame.time.Clock()

    color = (0, 0, 255)
    tool = 'brush'  
    brush_radius = 10
    radius = 15  
    mode = 'blue'

    shapes = []  
    points = []  
    start_pos = None

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    color = (255, 0, 0) 
                    mode = 'red'
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                    mode = 'green'
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                    mode = 'blue'
                
                # Change tool
                if event.key == pygame.K_s:
                    tool = 'rectangle'  # Rectangle
                elif event.key == pygame.K_c:
                    tool = 'circle'  # Circle
                elif event.key == pygame.K_l:
                    tool = 'brush'  # Brush
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tool == 'brush':
                    points.append(event.pos)
                    points = points[-256:]
                else:
                    start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP and start_pos:
                end_pos = event.pos
                if tool == 'rectangle':
                    # Create a rectangle
                    rect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]),
                                       abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    shapes.append(('rectangle', color, rect))
                elif tool == 'circle':
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    shapes.append(('circle', color, start_pos, radius))
                start_pos = None

            if event.type == pygame.MOUSEMOTION and tool == 'brush':
                position = event.pos
                points.append(position)
                points = points[-256:]

        # Clear screen
        screen.fill((255, 255, 255))

        # Draw shapes (rectangles, circles)
        for shape in shapes:
            if shape[0] == 'rectangle':
                pygame.draw.rect(screen, shape[1], shape[2])
            elif shape[0] == 'circle':
                pygame.draw.circle(screen, shape[1], shape[2], shape[3])

        # Draw lines between points for the brush tool
        for i in range(len(points) - 1):
            drawLineBetween(screen, i, points[i], points[i + 1], brush_radius, mode)
        pygame.display.flip()
        clock.tick(60)

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    # Set color based on mode
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    # Draw smooth gradient line between start and end points
    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()
