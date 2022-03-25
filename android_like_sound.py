from pydbus.generic import signal
import subprocess
from gi.repository import GLib
from pydbus import SessionBus
import time
import sys

bus = SessionBus()
loop = GLib.MainLoop()


#proxy = bus.get_object('org.mpris.MediaPlayer2.spotify','/org/mpris/MediaPlayer2')
#properties_manager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
#event_manager = dbus.Interface(proxy, 'org.mpris.MediaPlayer2.Player')
#curr_volume = properties_manager.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
# print(curr_volume)

#event_manager = dbus.Interface(proxy, 'org.mpris.MediaPlayer2.Player')
# event_manager.PlayPause()

#print(properties_manager.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus'))

loopEnabled = True
players = []
playStates = {}
# these are characters from fontawesome and may not get rendered in your editor
disabledCharacter = ""
#disabledCharacter = "Linux"
enabledCharacter = ""
#enabledCharacter = "Android"
# help(bus.dbus.Interfaces)
sys.stdout.write(enabledCharacter + "\n")
sys.stdout.flush()

players = list(filter(lambda x: x != "", subprocess.check_output(
    ["playerctl --list-all"], shell=True, universal_newlines=True).split("\n")))

print(players)

for name in players:
    playStates[name] = subprocess.check_output(
        ["playerctl -p " + name + " status"], shell=True, universal_newlines=True)

# event_managers[0].PlayPause()


def loop_function():
    global loopEnabled
    # print(loopEnabled)
    if loopEnabled:
        global proxies
        global players
        global playStates
        global loop_function
        time.sleep(0.5)
        # update the players

        new_players = list(filter(lambda x: x != "",subprocess.check_output(
            ["playerctl --list-all"], shell=True, universal_newlines=True).split("\n")))
        for name in new_players:
            # print(names)
            if not name in players:
                #print("adding: " + names)
                players.append(name)
                playStates[name] = "Paused"

        #print("cheking for recently closed players:")
        for i in range(len(players)-1, -1, -1):
            if not (players[i] in new_players):
                #print("deleting player: " + players[i])
                del playStates[players[i]]
                del players[i]

        # check if any player changed to playing

        playerToNotPause = -1
        newPlayStates = {}
        # print(players)
        if len(players) > 0:
            for i in range(len(players)):
                try:
                    name = players[i]
                    newPlayStates[name] = subprocess.check_output(
                        ["playerctl -p " + name + " status"], shell=True, universal_newlines=True)[:-1]

                except:
                    players[name] = "Paused"
                    pass
                #print(newPlayStates[i] + " " + playStates[i])
                if newPlayStates[name] == "Playing" and playStates[name] != "Playing":
                    # print(players[i])
                    playerToNotPause = i
                    # print(playerToNotPause)

        # pause everything exept the thing that just started playing
            if playerToNotPause != -1:
                for i in range(len(players)):
                    if(i != playerToNotPause):
                        name = players[i]
                        subprocess.check_output(
                            ["playerctl -p " + name + " pause"], shell=True, universal_newlines=True)

            playStates = newPlayStates
        print(players)
        print(playStates)
        GLib.timeout_add_seconds(0.5, loop_function)


loop_function()
'''        <method name='EchoString'>
          <arg type='s' name='a' direction='in'/>
          <arg type='s' name='response' direction='out'/>
        </method>
        '''


class Example(object):
    """
    <node>
      <interface name='io.github.laubersheini.mobileAudio'>

        <property name="Enabled" type="b" access="readwrite">
          <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
        </property>
      </interface>
    </node>
    """

    def EchoString(self, s):
        """returns whatever is passed to it"""
        return s

    def __init__(self):
        self._Enabled = True

    @property
    def Enabled(self):
        return self._Enabled

    @Enabled.setter
    def Enabled(self, value):
        global loopEnabled
        global loop_function
        loopEnabled = value
        if loopEnabled:
            sys.stdout.write(enabledCharacter + "\n")
            sys.stdout.flush()
            loop_function()
        else:
            sys.stdout.write(disabledCharacter + "\n")
            sys.stdout.flush()

        self._Enabled = value
        self.PropertiesChanged("io.github.laubersheini.mobileAudio", {
                               "Enabled": self.Enabled}, [])

    PropertiesChanged = signal()


bus.publish("io.github.laubersheini.mobileAudio", Example())
loop.run()
