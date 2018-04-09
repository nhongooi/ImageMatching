
import curses
from imageRecognition.wrapper import ImageWrapper
HEADER = "Image Matching Menu"
BOTTOM_HEADER = "Press 'Q' to quit; 'E' To select an option"

IMAGING_OPTION = {'title': "Type of Imaging", 'choice': ['Matching', 'Templating']}
SEARCH_OPTION = {'title': "Search File Type", 'choice': ['archive', 'image']}
PATH_INPUT = 'PATH:'
TEMPLATE_INPUT = "TEMPLATE PATH:"
MAX_USER_LEN = 260

def start_menu():

    user_choice = None
    user_path = None

    # start curses
    stdscr = curses.initscr()
    # disable keyboard echo, break mode. and hide cursor
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)


    # check for color support
    if curses.has_colors():
        curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # set header
    stdscr.addstr(HEADER, curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)

    # print bottom menu
    stdscr.addstr(curses.LINES - 1, 0, BOTTOM_HEADER)

    # change q to green
    stdscr.chgat(curses.LINES - 1, 7, 1, curses.A_BOLD | curses.color_pair(2))
    stdscr.chgat(curses.LINES - 1, 20, 1, curses.A_BOLD | curses.color_pair(1))

    # init inner/sub window/ border
    menu_window = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0 )

    # draw a border around the menu
    menu_window.box()

    # Enable keypad

    # update the menu window data struct
    stdscr.noutrefresh()
    menu_window.noutrefresh()

    # redraw the screen
    curses.doupdate()

    #init variables
    user_search_choice = None
    user_path = None
    user_fuzzy = None
    # imaging option
    # TODO check valid paths, user_fuzzy is int or float, and template path is valid
    try:
        user_choice = option_menu(stdscr, menu_window, IMAGING_OPTION)
        user_path = input_menu(menu_window, PATH_INPUT)

        if user_choice == 0: # matching
            user_search_choice = option_menu(stdscr, menu_window, SEARCH_OPTION)
            user_fuzzy = int(input_menu(menu_window, PATH_INPUT))
        elif user_choice == 1: # templating
            user_template_choice = input_menu(menu_window, TEMPLATE_INPUT)
        else:
            exit_menu()
            return None
    except Exception:
        return None

    user_wrapper = ImageWrapper(user_choice, user_path, user_search_choice,
                                user_template_choice, user_fuzzy)
    exit_menu()
    return user_wrapper


def option_menu(main_curses, window, text_options):
    """ Generate selectable option in curses sub windows

        Paramerters
        -------------
        window - curses sub window
        test_options - array of lines, indicating options for user selection

        return
        ---------------
        Index of text_options if user select an option
        else, -1 to exit curses menu"""

    main_curses.nodelay(0)
    window.keypad(1)
    option = 0
    # get value of windows and options
    num_options = len(text_options)
    selected = [0] * num_options
    window.addstr(1, 1, text_options['title'])
    # loop through nothing is chosen
    while True:
        # highlight option
        selected[option] = curses.A_REVERSE
        # loop through list of opteions for selection
        for line, text in zip(range(num_options), text_options['choice']):
            window.addstr(line + 3, 1, text, selected[line])

        window.refresh()

        # evaluation key input
        action = window.getch()
        if action == curses.KEY_DOWN:
            selected[option] = curses.A_NORMAL
            option = (option + 1) % num_options
        elif action == curses.KEY_UP:
            selected[option] = curses.A_NORMAL
            option = (option - 1) % num_options
        elif action == ord('E') or action == ord('e'):
            break
        elif action == ord('Q') or action == ord('q'):
            option = -1
            break
        else:
            continue

    window.keypad(0)
    window.clear()
    window.refresh()
    window.box()

    return option


def input_menu(window, text_input):
    """ Generate graphics for user string input

        Parameters
        ----------
        window - curses sub windows
        text_input - indicate what is being asked for

        Return
        -----------
        String of user input lress than Max len of 260 chars

        Note
        -----------
        The max len of 260 in path is due to Windows limitation on path
        size, it would not affect Linux or OSX"""
    # allow user typing
    curses.echo()
    window.addstr(1, 1, text_input)
    # added 1 on width for space separation
    user_input = window.getstr(1, len(text_input) + 1, MAX_USER_LEN)

    curses.noecho()
    window.clear()
    window.refresh()
    window.box()
    return user_input

def exit_menu():
    # restore terminal settings
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)

    # return to terminal
    curses.endwin()
