from win32api import GetAsyncKeyState

from . import logitech_km
from . import mobox_km
from . import msdk
import win32gui
from win32con import SPI_SETMOUSE, SPI_GETMOUSE, SPI_GETMOUSESPEED, SPI_SETMOUSESPEED

if logitech_km.STATE:
    from .logitech_km import mouse_move_relative, mouse_left_press
elif msdk.STATE:
    from msdk import mouse_move_relative, mouse_left_press
elif mobox_km.STATE:
    from mobox_km import mouse_move_relative, mouse_left_press

VK_CODE = {
    "A": 0x41, "B": 0x42, "C": 0x43, "D": 0x44, "E": 0x45, "F": 0x46, "G": 0x47, "H": 0x48, "I": 0x49, "J": 0x4A,
    "K": 0x4B, "L": 0x4C, "M": 0x4D, "N": 0x4E, "O": 0x4F, "P": 0x50, "Q": 0x51, "R": 0x52, "S": 0x53, "T": 0x54,
    "U": 0x55, "V": 0x56, "W": 0x57, "X": 0x58, "Y": 0x59, "Z": 0x5A, "1": 0x31, "2": 0x32, "3": 0x33, "4": 0x34,
    "5": 0x35, "6": 0x36, "7": 0x37, "8": 0x38, "9": 0x39, "0": 0x30, "Enter": 0x0D, "Esc": 0x1B, "BackSpace": 0x08,
    "Tab": 0x09, " ": 0x20, "-": 0xBD, "=": 0xBB, "[": 0xDB, "]": 0xDD, "\\": 0xDC, ";": 0xBA, "'": 0xDE, "`": 0xC0,
    ",": 0xBC, ".": 0xBE, "/": 0xBF, "CapsLock": 0x14, "F1": 0x70, "F2": 0x71, "F3": 0x72, "F4": 0x73, "F5": 0x74,
    "F6": 0x75, "F7": 0x76, "F8": 0x77, "F9": 0x78, "F10": 0x79, "F11": 0x7A, "F12": 0x7B, "PrintScreen": 0x2C,
    "ScrollLock": 0x91, "Pause": 0x13, "Break": 0x13, "Insert": 0x2D, "Home": 0x24, "Pageup": 0x21, "Delete": 0x2E,
    "End": 0x23, "Pagedown": 0x22, "Right": 0x27, "Left": 0x25, "Down": 0x28, "Up": 0x26, "NumLock": 0x90,
    "keypad./": 0x6F, "keypad.*": 0x60, "keypad.-": 0x6D, "keypad.+": 0x6B, "keypad.enter": 0x6C, "keypad.1": 0x61,
    "keypad.2": 0x62, "keypad.3": 0x63, "keypad.4": 0x64, "keypad.5": 0x65, "keypad.6": 0x66, "keypad.7": 0x67,
    "keypad.8": 0x68, "keypad.9": 0x69, "keypad.0": 0x60, "keypad..": 0x6E, "Menu": 0x5D, "keypad.=": 0x92, "静音": 0xAD,
    "音量加": 0xAF, "音量减": 0xAE, "left_Ctrl": 0xA2, "left_Shift": 0xA0, "left_Alt": 0xA4, "left_Win": 0x5B,
    "right_Ctrl": 0xA3, "right_Shift": 0xA1, "right_Alt": 0xA5, "right_Win": 0x5C, "Ctrl": 0x11, "Shift": 0x10,
    "Alt": 0x12, "l_button": 1, "r_button": 2, "cancel": 3, "m_button": 4, }
VK_CODE.update({_k.lower(): _v for _k, _v in VK_CODE.items()})
VK_CODE.update({_k.upper(): _v for _k, _v in VK_CODE.items()})


def move_relative(dx, dy):
    enhanced_holdback = win32gui.SystemParametersInfo(SPI_GETMOUSE)
    if enhanced_holdback[1]:
        win32gui.SystemParametersInfo(SPI_SETMOUSE, [0, 0, 0], 0)
    mouse_speed = win32gui.SystemParametersInfo(SPI_GETMOUSESPEED)
    if mouse_speed != 10:
        win32gui.SystemParametersInfo(SPI_SETMOUSESPEED, 10, 0)

    mouse_move_relative(round(dx), round(dy))

    if enhanced_holdback[1]:
        win32gui.SystemParametersInfo(SPI_SETMOUSE, enhanced_holdback, 0)
    if mouse_speed != 10:
        win32gui.SystemParametersInfo(SPI_SETMOUSESPEED, mouse_speed, 0)


get_key_state = lambda key: GetAsyncKeyState(key) & 0x8000
