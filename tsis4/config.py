
SCREEN_W   = 640
SCREEN_H   = 680
CELL_SIZE  = 20
COLS       = (SCREEN_W - 40) // CELL_SIZE  
ROWS       = (SCREEN_H - 100) // CELL_SIZE  
GRID_X     = 20  
GRID_Y     = 80  

FOODS_PER_LEVEL = 5 
BASE_SPEED      = 8   


C_BG          = (15,  15,  20)
C_GRID        = (30,  30,  40)
C_BORDER      = (60,  60,  80)
C_SNAKE_HEAD  = (80,  220,  80)
C_SNAKE_BODY  = (50,  170,  50)
C_FOOD_NORMAL = (255, 80,   80)
C_FOOD_BONUS  = (255, 200,   0)
C_FOOD_RARE   = (100, 180, 255)
C_FOOD_POISON = (120,  20,  20)
C_OBSTACLE    = (100,  60,  20)
C_PU_SPEED    = (255, 140,   0)
C_PU_SLOW     = (80,  140, 255)
C_PU_SHIELD   = (180, 100, 255)
C_HUD         = (220, 220, 220)
C_TITLE       = (255, 200,  60)
C_WHITE       = (240, 240, 240)
C_GRAY        = (140, 140, 140)
C_GREEN       = (80,  200,  80)
C_RED         = (220,  60,  60)
C_BTN         = (40,   40,  70)
C_BTN_H       = (70,   70, 120)

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "snake_game",
    "user":     "postgres",
    "password": "postgres",   
}
