import os, re, time, pyautogui
import tkinter as tk
from tkinter import messagebox


def waitToRun(delay):
    print("Executing Picolog Backup in {0} seconds...".format(delay))
    time.sleep(delay)


def moveClick(x,y, delay = .25):
    pyautogui.moveTo(x, y)
    time.sleep(.25)
    pyautogui.click(x, y)
    time.sleep(.25)


def get_sequence():
    with open('mouse_recording.txt', 'r') as file:
        lines = file.read().strip().splitlines()
    sequence = [
        tuple(map(int, line.split(','))) if re.match(r'\d+,\d+', line) else line
        for line in lines
    ]
    return sequence


def show_message(title, message):
    messagebox.showinfo(title, message)


def main():
    waitToRun(10)
    try:
        sequence = get_sequence()
    except FileNotFoundError:
        root = tk.Tk()
        root.withdraw()  # Hides the main window
        # Show the message box
        show_message("Error", "Must run setup_mouse_clicks.py before auto backup can function")
        root.mainloop()

    for entry in sequence:
        if type(entry) == tuple:
            x, y = entry
            moveClick(x, y, delay=.5)
            time.sleep(1)
        elif type(entry) == str:
            if entry == 'filename':
                pyautogui.typewrite('BACKUP')
    return

if __name__ == '__main__':
    main()