#Experimental Function

import pygame
import tkinter as tk

class Controller:
    def __init__(self, app):
        self.app = app
        
        pygame.init()
        pygame.joystick.init()

        self.joy = None

        if pygame.joystick.get_count():
            self.joy = pygame.joystick.Joystick(0)
            self.joy.init()
        
        self.poll()
    
    def poll(self):
        pygame.event.pump()

        if self.joy:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        widget = self.app.root.focus_get()

                        if isinstance(widget, tk.Entry):
                            self.shKey()
                        elif widget and hasattr(widget, "invoke"):
                            widget.invoke()
                    elif event.button == 1:
                        self.app.root.event_generate("<Escape>")
                    elif event.button == 4:
                        widget = self.app.root.focus_get()

                        if widget:
                            widget.tk_focusPrev().focus_set()
                    elif event.button == 5:
                        widget = self.app.root.focus_get()

                        if widget:
                            widget.tk_focusNext().focus_set()
                elif event.type == pygame.JOYHATMOTION:
                    if event.value == (0, 1):
                        self.app.root.event_generate("<Up>")
                    elif event.value == (0, -1):
                        self.app.root.event_generate("<Down>")
                    elif event.value == (-1, 0):
                        self.app.root.event_generate("<Left>")
                    elif event.value == (1, 0):
                        self.app.root.event_generate("<Right>")
            
        self.app.root.after(20, self.poll)