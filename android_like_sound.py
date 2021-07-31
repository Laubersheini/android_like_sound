import dbus
import time

bus = dbus.SessionBus()
#proxy = bus.get_object('org.mpris.MediaPlayer2.spotify','/org/mpris/MediaPlayer2')
#properties_manager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
#event_manager = dbus.Interface(proxy, 'org.mpris.MediaPlayer2.Player')
#curr_volume = properties_manager.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
#print(curr_volume)

#event_manager = dbus.Interface(proxy, 'org.mpris.MediaPlayer2.Player')
#event_manager.PlayPause()

#print(properties_manager.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus'))

players = []
playStates = []
proxies = []
property_managers = []
event_managers = []


for names in bus.list_names():
    if "mpris" in names:
        print(names)
        players.append(names)
        proxy = bus.get_object(names,'/org/mpris/MediaPlayer2')
        proxies.append( proxy)
        property_manager =  dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
        property_managers.append( property_manager)
        event_managers.append(dbus.Interface(proxy, 'org.mpris.MediaPlayer2.Player'))
        playStates.append(property_manager.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus'))

#event_managers[0].PlayPause()


while True:
    time.sleep(0.5)
    #update the players
    bus_names = bus.list_names()
    print("checking for new players:")
    for names in bus_names :
        if "mpris" in names:
            print(names)
            if not names in players:
                print("adding: " + names)
                players.append(names)
                proxy = bus.get_object(names,'/org/mpris/MediaPlayer2')
                proxies.append( proxy) 
                property_managers.append( dbus.Interface(proxy, 'org.freedesktop.DBus.Properties'))
                event_managers.append(dbus.Interface(proxy, 'org.mpris.MediaPlayer2.Player'))
                playStates.append("Paused")

    print("cheking for recently closed players:") 
    for i in range(len(players)-1,-1,-1):
        if not (players[i] in bus_names):
           print("deleting player: " + players[i])
           del players[i]
           del proxies[i]
           del property_managers[i]
           del event_managers[i]
           del playStates[i]



    #check if any player changed to playing
 
    playerToNotPause = -1
    newPlayStates = []
    print(players)
    if len(players)>0:
        for i in range(len(players)):
            try:
                newPlayStates.append(property_managers[i].Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus'))
            except:
                pass
            print(newPlayStates[i] + " " + playStates[i])
            if newPlayStates[i] == "Playing" and playStates[i] != "Playing":
                print(players[i])
                playerToNotPause = i
        print(playerToNotPause)

    #pause everything exept the thing that just started playing
        if playerToNotPause != -1 :
            for i in range(len(event_managers)):
                if(i != playerToNotPause):
                    event_managers[i].Pause()
        playStates = newPlayStates;
