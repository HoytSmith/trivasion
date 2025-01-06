#imports
import pygame
from src.validate import Validate

class Input():
    def __init__(self):
        #Mouse codes
        self.__mouse_codes = {
            "left" : 1
        }
        #Mouse states (records frames of activity, i.e. 1 == first frame of activity)
        self.__mouse_states = {
            "left" : 0
        }
        #Key codes
        self.__keycodes = {
            "pause" : [
                pygame.K_p, 
                pygame.K_ESCAPE
            ],
            "left" : [
                pygame.K_a,
                pygame.K_LEFT
            ],
            "up" : [
                pygame.K_w,
                pygame.K_UP
            ],
            "right" : [
                pygame.K_d,
                pygame.K_RIGHT
            ],
            "down" : [
                pygame.K_s,
                pygame.K_DOWN
            ]
        }
        #Key states (True if key pressed, False if not)
        self.__keystates = {
            "pause" : False,
            "left" : False,
            "up" : False,
            "right" : False,
            "down" : False
        }
    
    #SETTERS AND GETTERS:
    #MOUSE:
    def get_mouse_button_name(self, mouse_event_button_code):
        for mouse_button_name, mouse_button_code in self.__mouse_codes.items():
            if mouse_event_button_code == mouse_button_code:
                return mouse_button_name
        return "MOUSE_ERROR"

    def set_mouse_state(self, mouse_button, state):
        self.__mouse_states[mouse_button] = state
    
    def get_mouse_state(self, mouse_button):
        return self.__mouse_states[mouse_button]
    
    def press_mouse_button(self, mouse_button):
        self.set_mouse_state(mouse_button, self.get_mouse_state(mouse_button)+1)
    
    def reset_mouse_button(self, mouse_button):
        self.set_mouse_state(mouse_button, 0)
    
    #INPUT
    def get_key_name(self, key_event_code):
        for key_name, key_codes in self.__keycodes.items():
            if key_event_code in key_codes:
                return key_name
        return "KEY_ERROR"
    
    def set_key_state(self, key, state):
        self.__keystates[key] = state
    
    def press_key(self, key):
        self.set_key_state(key, True)

    def release_key(self, key):
        self.set_key_state(key, False)

    #GENERAL INPUT CHECKING METHODS:
    def mouse_button_click(self, mouse_code):
        return self.__mouse_states[mouse_code] == 1
    
    def mouse_button_down(self, mouse_code):
        return self.__mouse_states[mouse_code] > 0
    
    def is_key_pressed(self, key_name):
        return self.__keystates[key_name]
    
    #MOUSE INPUT CHECKING METHODS:
    def left_mouse_click(self):
        return self.mouse_button_click("left")
    
    def left_mouse_down(self):
        return self.mouse_button_down("left")

    #KEY INPUT CHECKING METHODS:
    def pause_pressed(self):
        return self.is_key_pressed("pause")
    
    def left_pressed(self):
        return self.is_key_pressed("left")
    
    def up_pressed(self):
        return self.is_key_pressed("up")
    
    def right_pressed(self):
        return self.is_key_pressed("right")
    
    def down_pressed(self):
        return self.is_key_pressed("down")

    #THE FOLLOWING ARE ALL EVENT HANDLING AND PROCESSING METHODS:
    def handle_event(self, event):
        if self.is_mouse_event(event.type):
            self.handle_mouse(event)
        if self.is_key_event(event.type):
            self.handle_key(event)
    
    def handle_mouse(self, mouse_event):
        mouse_button = self.get_mouse_button_name(mouse_event.button)
        if mouse_button != "MOUSE_ERROR":
            if mouse_event.type == pygame.MOUSEBUTTONDOWN:
                self.press_mouse_button(mouse_button)
            if mouse_event.type == pygame.MOUSEBUTTONUP:
                self.reset_mouse_button(mouse_button)

    def handle_key(self, key_event):
        key_name = self.get_key_name(key_event.key)
        if key_name != "KEY_ERROR":
            if key_event.type == pygame.KEYDOWN:
                self.press_key(key_name)
            if key_event.type == pygame.KEYUP:
                self.release_key(key_name)
    
    def is_mouse_event(self, event_type):
        return (event_type == pygame.MOUSEBUTTONDOWN or event_type == pygame.MOUSEBUTTONUP)
    
    def is_key_event(self, event_type):
        return (event_type == pygame.KEYUP or event_type == pygame.KEYDOWN)
