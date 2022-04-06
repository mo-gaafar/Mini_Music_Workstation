# https://namingconvention.org/python/ use the pythonic naming convention here (friendly reminder)

from PyQt5 import QtGui, QtWidgets, uic, QtCore 
from PyQt5.QtWidgets import QTabWidget
from modules import interface, resource
from modules.instruments import *
from modules.emphasizer import *
import numpy as np
from modules.utility import print_debug
import sys

from modules.spectrogram import create_spectrogram_figure


class MainWindow(QtWidgets.QMainWindow):
    ''' This is the PyQt5 GUI Main Window'''

    def __init__(self, *args, **kwargs):
        ''' Main window constructor'''

        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('./resources/music_ws_mainwindow.ui', self)

        # set the title and icon
        self.setWindowIcon(QtGui.QIcon('./resources/icons/icon.png'))
        self.setWindowTitle("Music Workstation")

        print_debug("Connectors Initialized")

        # initialize arrays and variables
        pygame.mixer.pre_init(
            channels=1, allowedchanges=0, buffer=512, frequency=44100)
        pygame.mixer.init()
       
        self.music_signal = MusicSignal()
        self.piano_instrument = Piano()
        self.drums_instrument = Drums()
        self.guitar_instrument = Guitar()
        self.toggle_play = 0
        self.toggle_apply = 0
        self.pressed_key =''
        self.current_tab_index = 0
        # initialize points to app
        self.pointsToAppend = 0
        interface.create_piano_layout(self)
        interface.init_connectors(self)
        create_spectrogram_figure(self)
   ############################################ test keyboard_pressed
    def keyPressEvent(self, event):
            #  print(event.text())
            print_debug('1         ' + self.pressed_key)
            self.pressed_key = event.text()  
            print_debug('2         ' + self.pressed_key)   
            if (self.current_tab_index == 0):
                self.piano_instrument.key_piano(self.pressed_key)  
            elif (self.current_tab_index == 0):
                pass
            elif (self.current_tab_index == 2):
                 self.drums_instrument.key_drums(self.pressed_key)
                
def main():

    app = QtWidgets.QApplication(sys.argv)
    # qt_material.apply_stylesheet(app, theme='light_blue.xml')
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
