import os, re, time, pyautogui
import platform

def waitToRun(delay):
    print("Executing Picolog Backup in {0} seconds...".format(delay))
    time.sleep(delay)


def moveClick(x,y, delay = .25):
    pyautogui.moveTo(x, y)
    time.sleep(.25)
    pyautogui.click(x, y)
    time.sleep(.25)
    
def load_button_images(supplied_button_directory=None):
    button_image_directory = os.path.join(os.getcwd(), 'on_screen_buttons') if supplied_button_directory is None else supplied_button_directory
    button_images = [
        (filename[:filename.index('.')], os.path.join(button_image_directory, filename)) 
        for filename in os.listdir(button_image_directory) 
        if filename.endswith('.png')]
    button_dict = {}
    for button_name, button_path in button_images:
        button_dict[button_name] = button_path
    return button_dict

class ButtonNotFoundException(Exception):
    def __init__(self, button_name):
        self.button_name = button_name
        super().__init__(f"Button '{button_name}' not found on screen.")


def handle_sequence_item(sequence_item, button_dictionary):
    main_action, fallback_action = sequence_item
    action_type, action_required, action_input = main_action
    action_optional = False if action_required == 'required' else True
    if action_type == 'button':
        button_image_path = button_dictionary[action_input]
        try:
            button_location = pyautogui.locateCenterOnScreen(button_image_path)
        except Exception as e:
            print(f'{action_input}: {e}')
            button_location = None

        if button_location is not None:
            pyautogui.click(button_location)
        elif button_location is None and not action_optional and fallback_action is not None:
            handle_sequence_item((fallback_action, None), button_dictionary)
        elif button_location is None and not action_optional and fallback_action is None:
            raise ButtonNotFoundException(action_input)
    elif action_type == 'text':
        pyautogui.typewrite(str(action_input))


def run_sequence(sequence, button_dictionary, delay_after_action = 1):
    for sequence_item in sequence:
        handle_sequence_item(sequence_item, button_dictionary)
        time.sleep(delay_after_action)

def main():
    print(os.uname())
    print(platform.system(), platform.release(), platform.version())
    #waitToRun(10)
    button_dictionary = load_button_images()
    color_mode = 'darkmode'
    sequence = [
        (('button', 'required', f'save_icon_{color_mode}'),      None),
        (('button', 'required', f'save_data_text_{color_mode}'), None),
        (('button', 'optional', f'continue_{color_mode}'),       None),
        (('text',    None,      'BACKUP'),                       None),
        (('button', 'required', f'final_save_{color_mode}'),     ('button', 'required', f'save_and_overwrite_{color_mode}')),
    ]    
    run_sequence(sequence, button_dictionary)    


if __name__ == '__main__':
    main()