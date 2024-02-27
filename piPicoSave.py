import os, re, time, pyautogui
import platform

correct_mode_platform = None

def waitToRun(delay):
    print("Executing Picolog Backup in {0} seconds...".format(delay))
    time.sleep(delay)

def determine_environment():
    uname_results = platform.uname()
    string = f'{uname_results.node} is {uname_results.system} {uname_results.release} on {uname_results.machine}'
    print(string)

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

def load_button_images(supplied_button_directory=None):
    # Determine the directory where button images are stored.
    button_image_directory = (
        os.path.join(os.getcwd(), 'on_screen_buttons')  # Use default directory if none supplied.
        if supplied_button_directory is None
        else supplied_button_directory  # Use supplied directory if provided.
    )

    # Load button images from the directory, extracting their names and mode/platform information.
    button_images = [
        (
            filename[:filename.rfind('_')],  # Button name (before the last underscore).
            os.path.join(button_image_directory, filename),  # Full path to the image file.
            filename[filename.rfind('_')+1:filename.index('.')]  # Mode/platform information (between the last underscore and the file extension).
        )
        for filename in os.listdir(button_image_directory)  # Iterate over all files in the directory.
        if filename.endswith('.png')  # Only consider PNG files.
    ]

    # Organize button images into a dictionary for easier access.
    button_dict = {}
    for button_name, button_path, button_mode_platform in button_images:
        if button_name not in button_dict:
            button_dict[button_name] = []
        button_dict[button_name].append((button_path, button_mode_platform))

    return button_dict

def handle_sequence_item(sequence_item, button_dictionary):
    global correct_mode_platform  # A global variable to store the current mode/platform.

    main_action, fallback_action = sequence_item
    action_type, action_required, action_input = main_action
    action_optional = False if action_required == 'required' else True

    if action_type == 'button':
        # Get all image paths for the specified button.
        button_image_paths = [
            button_image_path[0]   # index 0 is a path, index 1 is the mode information
            for button_image_path
            in button_dictionary[action_input]
        ]

        # Filter image paths based on the correct mode/platform, if known.
        if correct_mode_platform is not None:
            button_image_paths = [
                path
                for path in button_image_paths
                if path.endswith(f'{correct_mode_platform}.png')
            ]
        button_image_path = None

        # Find the first image that *is* on screen and use it.
        path_on_screen_checks = [
            (find_on_screen(path) is not None)
            for path in button_image_paths
        ]
        if True in path_on_screen_checks:
            button_image_path = button_image_paths[path_on_screen_checks.index(True)]
            # Set the correct mode/platform based on the found image, if not already set.
            if correct_mode_platform is None:
                correct_mode_platform = button_dictionary[action_input][button_image_paths.index(button_image_path)][1]
                print(f'mode_platform set to {correct_mode_platform}')

        # Find the location of the button image on the screen and click it, if found.
        button_location = (
            find_on_screen(button_image_path)
            if button_image_path is not None
            else None
        )
        if button_location is not None:
            pyautogui.click(button_location)
            return True
        # If the button is not found, handle the fallback action or raise an exception if it's required.
        elif button_location is None and not action_optional and fallback_action is not None:
            handle_sequence_item((fallback_action, None), button_dictionary)
        elif button_location is None and not action_optional and fallback_action is None:
            raise ButtonNotFoundException(action_input)

    # Handle text typing
    elif action_type == 'text':
        pyautogui.typewrite(str(action_input))
        return True


def run_sequence(sequence, button_dictionary, delay_after_action = 1):
    for sequence_item in sequence:
        action_done = handle_sequence_item(sequence_item, button_dictionary)
        if action_done:
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