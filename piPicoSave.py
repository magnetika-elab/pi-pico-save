import os, re, time, datetime, pyautogui


def waitToRun(delay):
    print("Executing Picolog Backup in {0} seconds...".format(delay))
    time.sleep(delay)
    return

def moveClick(x,y, delay = .25):
    pyautogui.moveTo(x, y)
    time.sleep(.25)
    pyautogui.click(x, y)
    time.sleep(.25)
    return

def get_sequence():
    with open('mouse_recording.txt', 'r') as file:
        lines = file.read().strip().splitlines()
    sequence = [
        tuple(map(int, line.split(','))) if re.match(r'\d+,\d+', line) else line
        for line in lines
    ]
    return sequence

def main():
    waitToRun(10)
    time_at_call = datetime.datetime.now()
    #(255, 15),
    sequence = get_sequence()
    for entry in sequence:
        if type(entry) == tuple:
            x, y = entry
            moveClick(x, y, delay=.5)
            time.sleep(1)
        elif type(entry) == str:
            if entry == 'filename':
                pyautogui.typewrite('BACKUP')#pyautogui.typewrite(time_at_call.strftime("%Y-%m-%d %H%M")) 
    return

if __name__ == '__main__':
    main()