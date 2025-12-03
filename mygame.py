import random

BOARD_WIDTH = 800
BOARD_HEIGHT = 800
NUM_GRID = 4
GRID_SIZE = BOARD_WIDTH // NUM_GRID  # // 정수값 반환?
TILE_MARGIN = 3
TILE_COLOR = {
    0: (205, 193, 180), 
    2: (238, 228, 218), 
    4: (237, 224, 200), 
    8: (242, 177, 121), 
    16: (245, 149, 99), 
    32: (246, 124, 95), 
    64: (246, 94, 59), 
    128: (237, 207, 114), 
    256: (237, 204, 97), 
    512: (237, 200, 80), 
    1024: (237, 197, 63), 
    2048: (237, 194, 46)
}
DEFAULT_COLOR = TILE_COLOR[0]

BG_COLOR = (187, 155, 160)


def rotate(is_cw,board_map):
    new_map = None

    if is_cw:
        new_map = [list(row) for row in zip(*board_map[::-1])]
                   
    else :
        # is_ccw:
        new_map = [list(row) for row in zip(*board_map)][::-1]
    return new_map

##### 숫자 머지
def merge_row(row):
    new_row =[]
    skip_merge = False

    for i in range(NUM_GRID):
        if skip_merge is True:
            skip_merge = False
            continue

        if row[i] == 0 :
            continue
        elif i + 1 < len(row) and row[i] == row[i+1]:
            new_row.append(row[i]*2)
            skip_merge = True
             ##이해 안됨
        elif i < len(row):
            new_row.append(row[i])
    while len(new_row) < NUM_GRID:
        new_row.append(0)

    return new_row


def push_and_merge(rotate_times, board_map):
    rotated_map = board_map
    
    #rotate cw 90 * rotate times
    for _ in range(rotate_times):
        rotated_map = rotate(True, rotated_map)

    #merge row
    new_board = []
    for row in rotated_map:
        new_row = merge_row(row)
        new_board.append(new_row)


    #rotate ccw 90 * rotate times
    for _ in range(rotate_times):
        new_board = rotate(False, new_board)
    return new_board

    # return rotated_map



def draw_cell(screen, row, column, font, value):
    rect = pygame.Rect(column * GRID_SIZE + TILE_MARGIN,
                       row * GRID_SIZE + TILE_MARGIN,
                       GRID_SIZE - TILE_MARGIN*2, GRID_SIZE - TILE_MARGIN*2)

    color = TILE_COLOR.get(value, DEFAULT_COLOR)
    pygame.draw.rect(screen, color, rect)
    #Display number
    if value != 0:
        text_area = font.render(str(value),True, (0,0,0) )
        cell_x = rect.centerx - (text_area.get_width() //2)
        cell_y = rect.centery - (text_area.get_height() //2)
        screen.blit(text_area, (cell_x, cell_y))

def render_board(screen, board_map, font):
    screen.fill(BG_COLOR)

    for row in range(NUM_GRID):
        for column in range(NUM_GRID):
            draw_cell(screen, row, column, font, board_map[row][column])


def spawn_tile(board_map):
    empty_cells = [(r,c)
                   for r in range(NUM_GRID)
                   for c in range(NUM_GRID) if board_map[r][c] == 0]
    if empty_cells:
        new_value = random.choices([2,4], weights = [0.9, 0.1])[0] #choice 복수형
        spawn_r, spawn_c = random.choice(empty_cells) #choice 단수형
        print (spawn_r)
        print (spawn_c)
        board_map[spawn_r][spawn_c] = new_value
        return True
    # no empty cells left
    return False



if __name__ == "__main__":

    # Example file showing a basic pygame "game loop"
    import pygame

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
    pygame.display.set_caption("2048Game")
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("Arial", 50, bold = True)
    board_map = [[0 for _ in range(NUM_GRID)] for _ in range(NUM_GRID)]

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        rotate_time = 0
                        # push_and_merge(0, board_map)
                    case pygame.K_RIGHT:
                        rotate_time = 2
                        # push_and_merge(2, board_map)
                    case pygame.K_UP:
                        rotate_time = 3
                        # push_and_merge(3, board_map)
                    case pygame.K_DOWN: 
                        rotate_time = 1
                        # push_and_merge(0, board_map)
                    case _:
                        pass
                if rotate_time != -1:
                    board_map = push_and_merge(rotate_time, board_map)
                    spawn_tile(board_map)
                


        # fill the screen with a color to wipe away anything from last frame
        # screen.fill(BG_COLOR)
        render_board(screen, board_map, font)
        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()























