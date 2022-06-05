# Screen dimensions
WIDTH = HEIGHT = 512

# Board dimensions
ROWS = COLS = 8
SQUARE_SIZE = HEIGHT // ROWS

# Colors
LIGHT_GREEN = (234, 235, 200)
DARK_GREEN = (119, 154, 88)
BROWN = (196, 112, 95)
L_BROWN = (240, 208, 187)
YELLOW = ( 236, 205, 35 )
L_YELLOW = (244, 212, 134)

# Color choice
COLORS = (L_BROWN, BROWN)  # [light, dark]
CHECK_COLOR = (207, 0, 0)  # red
SELECTED_COLOR = DARK_GREEN
POSSIBLE_COLOR = (154, 156, 148)  # grey-ish

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
DEPTH = 2
INIT_POS = (-1, -1)
EVAL_SIGN = {"white": 1, "black": -1}
AI_LINES = ["Beat that!", "In your face!", "You're going down...", "Didn't see that coming?",
            "It's never too late to resign", "easy", "you're so predicted",
            "who gave you a chess license?", "What's your number?", "Think you're tough?",
            "I love you, but you're gonna lose", "that's a SAHI move", "that's tough"]
