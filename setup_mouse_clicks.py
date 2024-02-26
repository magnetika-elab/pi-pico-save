import time
from pynput import mouse

clicks = 0

def on_click(x, y, button, pressed):
    global clicks
    if pressed:
        with open('mouse_recording.txt','a') as file:
            file.write(f'{x},{y}\n')
        clicks += 1
        if clicks == 2:
            with open('mouse_recording.txt','a') as file:
                file.write('filename\n')
        elif clicks == 3:
            exit()


print('Begining recording in 3 seconds...')
time.sleep(3)
print('go')
# Collect events until released
with mouse.Listener(
        on_click=on_click) as listener:
    listener.join()