import curses
import numpy as np
import sys

SYMBOLS = "`,+LT{(S1EkhO#@"
SIZE = 11
OFFSET = SIZE // 2
ROT = 10

def setup_colors():
    for i in range(1, np.rint(SIZE * 1.41).astype(np.int8) + 1):
        curses.init_color(i, int(1000 / 16) * i, 0, 0 )
        curses.init_pair(i, i, 0)
        
    
def draw_cube(stdscr, pts, center_pt):
    rounded_pts = np.rint(pts).astype(np.int8)
    
    visible_xy_pts = np.unique(rounded_pts[:,1:], axis=0)
    i = visible_xy_pts[0, 0]
    j = 0

    for pt in visible_xy_pts:
        depth = rounded_pts[np.all(rounded_pts[:,1:] == pt, axis=1), 0].max()
        depth = np.clip(depth, int (-OFFSET*1.41)+1, int(OFFSET*1.41)+1) + OFFSET + 1
        if pt[0] != j:
            j = pt[0]
            i = 0
        #stdscr.addch(pt[0] + center_pt[0], pt[1] + center_pt[1], curses.ACS_BLOCK, curses.color_pair(depth))
        y = pt[0] + center_pt[0]
        x = pt[1] * 2 + center_pt[1]

        stdscr.addch(y, x, curses.ACS_BLOCK, curses.color_pair(depth))
        stdscr.addch(y, x + 1, curses.ACS_BLOCK, curses.color_pair(depth))
        j += 1
        
        #stdscr.addch(pt[0] + center_pt[0], pt[1] + center_pt[1], SYMBOLS[depth])
    stdscr.refresh()
    
def rotate3d(pts, alfa, beta, gamma):
    sa, ca = np.sin(alfa), np.cos(alfa)
    sb, cb = np.sin(beta), np.cos(beta)
    sc, cc = np.sin(gamma), np.cos(gamma)
    # extrinsic rotation matrix
    rot_matrix = np.array([[cb*cc,
                            sa*sb*cc - ca*sc,
                            ca*sb*cc + sa*sc],
                            [cb*sc,
                            sa*sb*sc + ca*cc,
                            ca*sb*sc - sa*cc],
                            [-sb,
                            sa*cb,
                            ca*cb]], 
                            dtype=np.float32)
    for i, pt in enumerate(pts):
        pts[i] = rot_matrix @ pt
           
def main(stdscr):
    curses.curs_set(0)
    
    setup_colors()
    heigth, width = stdscr.getmaxyx()    
    center_pt = [heigth // 2, width // 2]
    cube = (np.argwhere(np.ones(shape=(SIZE, SIZE, SIZE))) - OFFSET).astype(np.float32)
    #select only surface points
    mask = (cube[:,0] == -OFFSET) | (cube[:,0] == OFFSET) \
    | (cube[:,1] == -OFFSET) | (cube[:,1] == OFFSET) \
    | (cube[:,2] == -OFFSET) | (cube[:,2] == OFFSET)
    cube = cube[mask]
    alfa, beta, gamma = 0, 0, 0 # ROT: Z Y X
    rot_step = np.radians(ROT)
    i = 0
    draw_cube(stdscr, cube, center_pt)
    while True:
        i += 1
        pts = cube.copy()
        pressed_key = stdscr.getch()
        if pressed_key == ord("q"):
            break
        elif pressed_key == ord("z"):
            alfa += rot_step
        elif pressed_key == ord("c"):
            beta += rot_step
        elif pressed_key == ord("x"):
            gamma += rot_step
            
        rotate3d(pts, alfa, beta, gamma)    
        stdscr.clear()
        draw_cube(stdscr, pts, center_pt)
        stdscr.addstr(heigth-1, 0, f"ROT: {i}, ALFA: {int(np.degrees(alfa))% 360}, BETA: {int(np.degrees(beta))% 360}, GAMMA: {int(np.degrees(gamma))% 360}")
curses.wrapper(main)
