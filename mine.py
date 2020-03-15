import Foundation
import threading
import rumps

from AppKit import *
from PyObjCTools import AppHelper

class MenuBarApp(rumps.App):
    def __init__(self, name, *args, **kwargs):
        super(MenuBarApp, self).__init__(name, *args, **kwargs)
        self.icon = 'icon.png'
        self.template = True
        self.quit_button = None
        
    @rumps.clicked('Start at Login')
    def boxStartAtLogin(self, event):
        event.state = not event.state
    
    @rumps.clicked('Quit')
    def quit(self, event):
        rumps.quit_application()
        
menuApp = MenuBarApp('')

class AppleMusic(NSObject):
    def getPlayingSong_(self, song):
        details = {}
        ui = song.userInfo()
        for x in ui:
            details[x] = ui.objectForKey_(x)
    
        if ('Artist' in details.keys() or 'Album Artist' in details.keys()) and 'Name' in details.keys():
            if 'Artist' in details.keys():
                artist = details['Artist']
            elif 'Album Artist' in details.keys():
                artist = details['Album Artist']
            name = details['Name']
            
            if details['Player State'] == 'Paused':
                menuApp.icon = 'icon.png'
                menuApp.title = None
            else:
                menuApp.icon = None
                menuApp.title = '%s - %s' % (artist, name)

if __name__ == "__main__":
    AppleMusic = AppleMusic.new()
    NC = Foundation.NSDistributedNotificationCenter.defaultCenter()
    NC.addObserver_selector_name_object_(AppleMusic, 'getPlayingSong:', 'com.apple.iTunes.playerInfo', None)
    threading.Thread(target=AppHelper.runConsoleEventLoop, args=()).start()
    menuApp.run()
