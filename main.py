import time
import json

import pyperclip
import pyautogui


def timestamp():
    mt = time.localtime()
    return f'{mt.tm_hour}:{mt.tm_min}'


def cmd_info_prefix(msg):
    print(f'[{timestamp()}] - {str(msg)}')


def load_commands_json(filename=r"commands.json"):
    trys = 10
    while True:
        try:
            with open(filename, "r", encoding="UTF8") as file:
                return json.load(file)

        except FileNotFoundError:

            if trys == 0:
                cmd_info_prefix(f"{trys} trys left.")
                cmd_info_prefix(f"script has been shut down")
                exit()
            else:
                trys -= 1
                cmd_info_prefix(f"next try in 30 seconds. {trys} left before script shutdown.")
                time.sleep(30)


def convert_command(execution_method=None, command=None):
    if execution_method != None and command != None:
        if type(command) != list:
            command = [command]

        # just overwrites the marked command with the assigned value
        if execution_method == "#":
            for value in command:
                pyperclip.copy(value)
                pyautogui.hotkey("ctrl", "v")

        # overwrites the marked command triggers tab+enter to write another value
        # userd for multiple values holded in one command i.e #MAMAPAPA3
        # which holds 3 values
        elif execution_method == "+":
            for value in command:
                pyperclip.copy(value)
                pyautogui.hotkey("ctrl", "v")
                pyautogui.press("tab")
                pyautogui.press("enter")

        # '!' is used to display text, infos or instruction in the CMD
        # maybe later also used to switch to cmd instructions and easy .json
        # commands updates
        elif execution_method == "!":
            for value in command:
                cmd_info_prefix(value)
                pyperclip.copy("reset")


def main_loop(tick_rate=1):
    pyperclip.copy("reset")

    while True:

        commands_dict = load_commands_json()
        cb = pyperclip.paste().upper()

        if len(cb) > 2 and commands_dict != None:
            for exe_instr, command_key in commands_dict.items():
                if cb[0] in exe_instr and cb[1::] in command_key:
                    convert_command(exe_instr, command_key.get(cb[1::], None))

        time.sleep(tick_rate)


if __name__ == '__main__':
    cmd_info_prefix(f"script is being started - listening to commands in clipboard")
    main_loop()
