from pydbus import SessionBus
import time

bus = SessionBus()

proxy = bus.get("io.github.laubersheini.mobileAudio",'/io/github/laubersheini/mobileAudio')


print(proxy.Enabled)
#event_managers[0].PlayPause()

def toggleMobileLikeSound():
    state = proxy.Enabled
    proxy.Enabled = not proxy.Enabled

toggleMobileLikeSound()