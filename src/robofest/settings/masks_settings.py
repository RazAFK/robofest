from robofest.classes.color_class import Color, Mask

card_red_start = Mask(Color.red, (0, 10), (50, 255), (70, 255))
card_red_end = Mask(Color.red, (160, 180), (50, 255), (70, 255))
card_blue = Mask(Color.blue, (90, 128), (50, 255), (70, 255))
card_yellow = Mask(Color.yellow, (20, 35), (100, 255), (100, 255))

# cube_red_start = Mask(Color.red, (0, 50), (80, 255), (40, 255))
# cube_red_end = Mask(Color.red, (160, 180), (50, 255), (70, 255))
# cube_blue = Mask(Color.blue, (60, 179), (50, 255), (40, 255))
# cube_yellow = Mask(Color.yellow, (50, 100), (35, 255), (130, 255))
# cube_white = Mask(Color.white, (0, 50), (60, 100), (170, 255))

cube_red_start = Mask(Color.red, (0, 50), (100, 255), (40, 255))
cube_red_end = Mask(Color.red, (160, 180), (50, 255), (70, 255))
cube_blue = Mask(Color.blue, (101, 159), (50, 255), (40, 255))
cube_yellow = Mask(Color.yellow, (52, 100), (35, 255), (130, 255))
cube_white = Mask(Color.white, (0, 50), (60, 99), (170, 255))

background = Mask(Color.white, (25, 179), (0, 32), (100, 255))
line = Mask(Color.white, (0, 179), (0, 30), (200, 255))