import curses

text = """Hello world!
This is a tiny text editor.
Edit me!"""

cursor = 0


def draw(screen):
    screen.clear()

    # ==========================================================
    # INITIALIZE THE DISPLAY
    #
    # Display the document with the cursor at the current
    # cursor position.
    #
    # Example
    #
    # text    = "Hello"
    # cursor  = 0
    #
    # display = "|Hello"
    #
    # ---------------- TODO ----------------

    display = text[:cursor] + "|" + text[cursor:]

    # ----------------------------------------

    for row, line in enumerate(display.split("\n")):
        screen.addstr(row, 0, line)

    screen.addstr(
        len(display.split("\n")) + 1,
        0,
        "← → Move   Type Insert   Backspace Delete   Enter New Line   Esc Quit"
    )

    screen.refresh()


def main(screen):
    global text, cursor

    while True:
        draw(screen)

        key = screen.getch()

        if key == 27:
            break

        # ==========================================================
        # LEFT ARROW
        #
        # Move the cursor one position to the left.
        #
        # Example
        #
        # Before
        # text    = "Hello"
        # cursor  = 3
        # display = "Hel|lo"
        #
        # After
        # text    = "Hello"
        # cursor  = 2
        # display = "He|llo"
        #
        # ---------------- ANSWER ----------------

        elif key == curses.KEY_LEFT:
            if cursor > 0:
                cursor -= 1

            display = text[:cursor] + "|" + text[cursor:]

        # ----------------------------------------

        # ==========================================================
        # RIGHT ARROW
        #
        # Move the cursor one position to the right.
        #
        # Example
        #
        # Before
        # text    = "Hello"
        # cursor  = 3
        # display = "Hel|lo"
        #
        # After
        # text    = "Hello"
        # cursor  = 4
        # display = "Hell|o"
        #
        # ---------------- ANSWER ----------------

        elif key == curses.KEY_RIGHT:

            if cursor < len(text):
                cursor += 1
            display = text[:cursor] + "|" + text[cursor:]

        # ----------------------------------------

        # ==========================================================
        # BACKSPACE
        #
        # Delete the character immediately before the cursor.
        #
        # Example
        #
        # Before
        # text    = "Hello"
        # cursor  = 3
        # display = "Hel|lo"
        #
        # After
        # text    = "Helo"
        # cursor  = 2
        # display = "He|lo"
        #
        # ---------------- ANSWER ----------------





        elif key in (8, 127, curses.KEY_BACKSPACE):

            if cursor > 0:

                text = text[:cursor-1] + text[cursor:]
                cursor -= 1

            display = text[:cursor] + "|" + text[cursor:]



        # ----------------------------------------

        # ==========================================================
        # ENTER
        #
        # Insert a newline at the cursor.
        #
        # Example
        #
        # Before
        # text    = "Hello"
        # cursor  = 3
        # display = "Hel|lo"
        #
        # After
        # text    = "Hel\nlo"
        # cursor  = 4
        # display = "Hel\n|lo"
        #
        # ---------------- ANSWER ----------------

        elif key == 10:

            
            text = text[:cursor] + "\n" + text[cursor:]
            cursor +=1

            display = text[:cursor] + "\n" + "|" + text[cursor:]

        # ----------------------------------------

        # ==========================================================
        # INSERT CHARACTER
        #
        # Insert the typed character at the cursor.
        #
        # Example
        #
        # Before
        # text    = "Hello"
        # cursor  = 3
        # display = "Hel|lo"
        #
        # Typing X
        #
        # After
        # text    = "HelXlo"
        # cursor  = 4
        # display = "HelX|lo"
        #
        # ---------------- ANSWER ----------------

        elif 32 <= key <= 126:

            text = text[:cursor] + chr(key) + text[cursor:]
            cursor +=1

            display = text[:cursor+1] + "|" + text[cursor:]

        # ----------------------------------------

        #BONUS: Can you figure out how to select one line up/down by yourself?

        elif key == curses.KEY_UP:

            lines = text.split("\n")
            position = 0
            for i in range(len(lines)):
                if position + len(lines[i]) >= cursor:
                    col = cursor - position
                    if i > 0:
                        cursor = position - len(lines[i-1]) - 1 + min(col, len(lines[i-1]))
                    break
                position += len(lines[i]) + 1
            display = text[:cursor] + "\n" + "|" + text[cursor:]




        elif key == curses.KEY_DOWN:
            lines = text.split("\n")
            position = 0
            for i in range(len(lines)):
                if position + len(lines[i]) >= cursor:
                    col = cursor - position
                    if i < len(lines)-1:
                        cursor = position + len(lines[i]) + 1 + min(col, len(lines[i-1]))
                    break
                position += len(lines[i]) + 1
            display = text[:cursor] + "\n" + "|" + text[cursor:]

curses.wrapper(main)
