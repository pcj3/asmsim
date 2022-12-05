import pathlib
import curses

import cv2 as cv
import numpy as np


MAP = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
MAP = " .:-=+*#%@"
def img2curses(stdscr, img_path):
    curses.curs_set(0)
    img = cv.imread(str(img_path), cv.IMREAD_GRAYSCALE)
    height, width = stdscr.getmaxyx()
    height_scaled = height
    scale = height_scaled / img.shape[0] 
    width_scaled = int(scale * img.shape[1])
    img = cv.resize(img, (width_scaled, height_scaled))
    img = np.repeat(img.astype(np.int16), 2, axis=1)
    #img = (img - img.min()) / (img.max() - img.min()) * len(MAP) - 1
    #img = img.astype(np.int16)
    color_step = 1000 / 255
    for i_color in range(1, 255):
        curses.init_color(i_color,  int(i_color * color_step), int(i_color * color_step), 0)
        curses.init_pair(i_color, i_color, 0)
    #curses.init_color(101,  1000, 1000, 0)
    #curses.init_pair(101, 101, 0)    # 

    finished = False
    while True:
        c = stdscr.getch()
        if c == ord("q"):
            break
        elif finished:
            stdscr.addstr(height // 2,
             width_scaled * 2 + 2, 
             "The little birds could be preyed upon at any moment.", 
             curses.color_pair(101))
             
            stdscr.addstr(height // 2 + 1,
              width_scaled * 2 + 2, 
              "The fountain is merely a token of acquittal for the people who are destroying nature.", 
              curses.color_pair(101))
            stdscr.refresh()
            
        for y in range(height_scaled):
            for x in range(width_scaled*2):
                stdscr.addch(y, x, curses.ACS_BLOCK, curses.color_pair(img[y, x]))    
                #stdscr.addch(y, x, MAP[img[y, x]], curses.color_pair(101))    
            finished = True  
        stdscr.refresh()
    curses.use_default_colors()
if __name__ == "__main__":
    input = pathlib.Path("tomek.jpg")
    curses.wrapper(img2curses, input)
