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

def determine_environment():
    uname_results = platform.uname()
    string = f'{uname_results.node} is {uname_results.system} {uname_results.release} on {uname_results.machine}'
    print(string)



def load_button_images(supplied_button_directory=None):
    button_image_directory = (
        os.path.join(os.getcwd(), 'on_screen_buttons')
        if supplied_button_directory is None
        else supplied_button_directory
    )
    button_images = [
        (filename[:filename.rfind('_')], os.path.join(button_image_directory, filename)) 
        for filename in os.listdir(button_image_directory) 
        if filename.endswith('.png')]
    button_dict = {}
    for button_name, button_path in button_images:
        if button_name not in button_dict:
            button_dict[button_name] = []
        button_dict[button_name].append(button_path)
    return button_dict

class ButtonNotFoundException(Exception):
    def __init__(self, button_name):
        self.button_name = button_name
        super().__init__(f"Button '{button_name}' not found on screen.")

def find_on_screen(button_image_path):
    try:
        button_location = pyautogui.locateCenterOnScreen(button_image_path)
    except Exception as e:
        button_location = None
    return button_location


def handle_sequence_item(sequence_item, button_dictionary):
    main_action, fallback_action = sequence_item
    action_type, action_required, action_input = main_action
    action_optional = False if action_required == 'required' else True
    if action_type == 'button':
        button_image_paths = button_dictionary[action_input]
        button_image_path = None
        if True in list(map(lambda i: i is not None, list(map(find_on_screen, button_image_paths)))):
            button_image_path = button_image_paths[list(map(lambda i: i is not None, list(map(find_on_screen, button_image_paths)))).index(True)]
        button_location = find_on_screen(button_image_path) if button_image_path is not None else None
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
    determine_environment()
    waitToRun(10)
    button_dictionary = load_button_images()
    sequence = [
        (('button', 'required', f'save_icon'),      None),
        (('button', 'required', f'save_data_text'), None),
        (('button', 'optional', f'continue'),       None),
        (('text',    None,      'BACKUP'),                       None),
        (('button', 'required', f'final_save'),     ('button', 'required', f'save_and_overwrite')),
    ]
    run_sequence(sequence, button_dictionary)


if __name__ == '__main__':
    main()