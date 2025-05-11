#!/home/jack/matrixenv/bin/python

import os
import random
import curses
import wcwidth

def get_characters():
    ranges = [
        (0x0021, 0x007E),
        (0x00A1, 0x00FF),
        (0x2580, 0x259F),
        (0x25A0, 0x25FF),
        (0x2200, 0x22FF),
        (0x2300, 0x23FF),
    ]
    start, end = random.choice(ranges)
    return chr(random.randint(start, end))

def get_safe_character():
    while True:
        c = get_characters()
        if c.isprintable() and not c.isspace() and wcwidth.wcwidth(c) == 1:
            return c

def maybe_glitch(char):
    return get_safe_character() if random.random() < 0.005 else char

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(40)

    height, width = stdscr.getmaxyx()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)

    # Initialize columns, speeds, and counters
    columns = []
    column_speeds = []
    column_counters = []

    # Initialize columns with random starting positions and trails
    for x in range(width):
        trail_length = random.randint(6, 12)
        y = random.randint(0, height // 2)
        trail = [get_safe_character() for _ in range(trail_length)]
        columns.append([y, trail, trail_length])
        column_speeds.append(random.randint(1, 3))
        column_counters.append(0)

    while True:
        # Get the new terminal size
        new_height, new_width = stdscr.getmaxyx()

        # If the size has changed, update the columns
        if new_height != height or new_width != width:
            height, width = new_height, new_width
            columns = []
            column_speeds = []
            column_counters = []

            # Reinitialize columns based on new width and height
            for x in range(width):
                trail_length = random.randint(6, 12)
                y = random.randint(0, height // 2)
                trail = [get_safe_character() for _ in range(trail_length)]
                columns.append([y, trail, trail_length])
                column_speeds.append(random.randint(1, 3))
                column_counters.append(0)

            # Clear the screen for the new layout
            stdscr.clear()

        stdscr.erase()

        # Render each column
        for x, (y, trail, trail_length) in enumerate(columns):
            for i, char in enumerate(trail):
                pos_y = (y - i) % height
                char = maybe_glitch(char)
                if i == 0:
                    color = curses.color_pair(1) | curses.A_BOLD
                elif i < 3:
                    color = curses.color_pair(2)
                elif i < len(trail) - 1:
                    color = curses.color_pair(3) | curses.A_DIM
                else:
                    color = curses.color_pair(4)
                try:
                    stdscr.addstr(pos_y, x, char, color)
                except curses.error:
                    pass

            # Update column counters and move the trail
            column_counters[x] += 1
            if column_counters[x] >= column_speeds[x]:
                column_counters[x] = 0
                trail.insert(0, get_safe_character())
                if len(trail) > trail_length:
                    trail.pop()
                columns[x][0] = (columns[x][0] + 1) % height
                if random.random() < 0.005:
                    columns[x][0] = 0
                    trail_length = random.randint(6, 12)
                    columns[x][1] = [get_safe_character() for _ in range(trail_length)]
                    columns[x][2] = trail_length

        # Refresh the screen
        stdscr.refresh()

        # Exit if 'q' is pressed
        _ = getch()
            break

curses.wrapper(main)
