from __future__ import annotations
from enum import IntEnum
from typing import Literal
from .exceptions import InvalidMouseButtonRequested


class KeyState(IntEnum):
    KEY_DOWN = 0x00
    KEY_UP = 0x01
    KEY_E0 = 0x02
    KEY_E1 = 0x04
    KEY_TERMSRV_SET_LED = 0x08
    KEY_TERMSRV_SHADOW = 0x10
    KEY_TERMSRV_VKPACKET = 0x20


class MouseState(IntEnum):
    MOUSE_LEFT_BUTTON_DOWN = 0x001
    MOUSE_LEFT_BUTTON_UP = 0x002
    MOUSE_RIGHT_BUTTON_DOWN = 0x004
    MOUSE_RIGHT_BUTTON_UP = 0x008
    MOUSE_MIDDLE_BUTTON_DOWN = 0x010
    MOUSE_MIDDLE_BUTTON_UP = 0x020

    MOUSE_BUTTON_4_DOWN = 0x040
    MOUSE_BUTTON_4_UP = 0x080
    MOUSE_BUTTON_5_DOWN = 0x100
    MOUSE_BUTTON_5_UP = 0x200

    MOUSE_WHEEL = 0x400
    MOUSE_HWHEEL = 0x800

    @staticmethod
    def from_string(
        button: Literal["left", "right", "middle", "mouse4", "mouse5"]
    ) -> tuple[MouseState, MouseState]:
        try:
            return _MAPPED_MOUSE_BUTTONS[button]
        except KeyError:
            raise InvalidMouseButtonRequested(button)


class MouseFlag(IntEnum):
    MOUSE_MOVE_RELATIVE = 0x000
    MOUSE_MOVE_ABSOLUTE = 0x001
    MOUSE_VIRTUAL_DESKTOP = 0x002
    MOUSE_ATTRIBUTES_CHANGED = 0x004
    MOUSE_MOVE_NOCOALESCE = 0x008
    MOUSE_TERMSRV_SRC_SHADOW = 0x100


class MouseRolling(IntEnum):
    MOUSE_WHEEL_UP = 0x78
    MOUSE_WHEEL_DOWN = 0xFF88


class FilterMouseState(IntEnum):
    FILTER_MOUSE_NONE = 0x0000
    FILTER_MOUSE_ALL = 0xFFFF

    FILTER_MOUSE_LEFT_BUTTON_DOWN = MouseState.MOUSE_LEFT_BUTTON_DOWN
    FILTER_MOUSE_LEFT_BUTTON_UP = MouseState.MOUSE_LEFT_BUTTON_UP
    FILTER_MOUSE_RIGHT_BUTTON_DOWN = MouseState.MOUSE_RIGHT_BUTTON_DOWN
    FILTER_MOUSE_RIGHT_BUTTON_UP = MouseState.MOUSE_RIGHT_BUTTON_UP
    FILTER_MOUSE_MIDDLE_BUTTON_DOWN = MouseState.MOUSE_MIDDLE_BUTTON_DOWN
    FILTER_MOUSE_MIDDLE_BUTTON_UP = MouseState.MOUSE_MIDDLE_BUTTON_UP

    FILTER_MOUSE_BUTTON_4_DOWN = MouseState.MOUSE_BUTTON_4_DOWN
    FILTER_MOUSE_BUTTON_4_UP = MouseState.MOUSE_BUTTON_4_UP
    FILTER_MOUSE_BUTTON_5_DOWN = MouseState.MOUSE_BUTTON_5_DOWN
    FILTER_MOUSE_BUTTON_5_UP = MouseState.MOUSE_BUTTON_5_UP

    FILTER_MOUSE_WHEEL = MouseState.MOUSE_WHEEL
    FILTER_MOUSE_HWHEEL = MouseState.MOUSE_HWHEEL
    FILTER_MOUSE_MOVE = 0x1000


class FilterKeyState(IntEnum):
    FILTER_KEY_NONE = 0x0000
    FILTER_KEY_ALL = 0xFFFF
    FILTER_KEY_DOWN = KeyState.KEY_UP
    FILTER_KEY_UP = KeyState.KEY_UP << 1
    FILTER_KEY_E0 = KeyState.KEY_E0 << 1
    FILTER_KEY_E1 = KeyState.KEY_E1 << 1
    FILTER_KEY_TERMSRV_SET_LED = KeyState.KEY_TERMSRV_SET_LED << 1
    FILTER_KEY_TERMSRV_SHADOW = KeyState.KEY_TERMSRV_SHADOW << 1
    FILTER_KEY_TERMSRV_VKPACKET = KeyState.KEY_TERMSRV_VKPACKET << 1


_MAPPED_MOUSE_BUTTONS = {
    "left": (MouseState.MOUSE_LEFT_BUTTON_DOWN, MouseState.MOUSE_LEFT_BUTTON_UP),
    "right": (MouseState.MOUSE_RIGHT_BUTTON_DOWN, MouseState.MOUSE_RIGHT_BUTTON_UP),
    "middle": (MouseState.MOUSE_MIDDLE_BUTTON_DOWN, MouseState.MOUSE_MIDDLE_BUTTON_UP),
    "mouse4": (MouseState.MOUSE_BUTTON_4_DOWN, MouseState.MOUSE_BUTTON_4_UP),
    "mouse5": (MouseState.MOUSE_BUTTON_5_DOWN, MouseState.MOUSE_BUTTON_5_UP),
}

UPPER_TO_LOWER = {
    "~": "`",
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
    "_": "-",
    "+": "=",
    "A": "a",
    "B": "b",
    "C": "c",
    "D": "d",
    "E": "e",
    "F": "f",   
    "G": "g",
    "H": "h",
    "I": "i",
    "J": "j",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "O": "o",
    "P": "p",
    "Q": "q",
    "R": "r",
    "S": "s",
    "T": "t",
    "U": "u",
    "V": "v",
    "W": "w",
    "X": "x",
    "Y": "y",
    "Z": "z",
    "{": "[",
    "}": "]",
    "|": "\\",
    ":": ";",
    '"': "'",
    "<": ",",
    ">": ".",
    "?": "/",
}