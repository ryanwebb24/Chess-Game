import pygame as pg
import ChessEngine

WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
PIECES = ['bp', 'br', 'bn', 'bb', 'bq', 'bk', 'wp', 'wr', 'wn', 'wb', 'wq', 'wk']

def load_images():
    for piece in PIECES:
        IMAGES[piece] = pg.transform.scale(pg.image.load('./Chess-Game/images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))
        

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color('white'))
    gs = ChessEngine.Game()
    valid_moves = gs.getValidMoves()
    move_made = False
    load_images()
    running = True
    sq_selected = ()
    player_click = [] 
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = ()
                    player_click = []
                else:
                    sq_selected = (row, col)
                    player_click.append(sq_selected)
                if len(player_click) == 2:
                    move = ChessEngine.Move(player_click[0],player_click[1], gs.board)
                    print(move.getChessNotation())
                    if move in valid_moves:
                        gs.makeMove(move)
                        move_made = True
                        sq_selected = ()
                        player_click = []
                    else:
                        player_click = [sq_selected]
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    gs.undoMove()
                    move_made = True
                elif event.key == pg.K_r:
                    gs.Reset()
                    move_made = False

        if move_made:
            valid_moves = gs.getValidMoves()
            move_made = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        pg.display.flip()

def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen,gs.board)

def draw_board(screen):
    colors = [pg.Color('white'),pg.Color('grey')]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col)%2)]
            pg.draw.rect(screen, color, pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != '--':
                screen.blit(IMAGES[piece], pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == '__main__':
    main()
