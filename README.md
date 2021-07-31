# android_like_sound
This python script uses mpris2 to emulate a simmilar soundbehavior to Android/Apple devices on Linux.
This means that only one source of sound is allowed at any time.
## Example
Rythmbox is playing music, you open up youtube and start a video, the script detects that a new source started playing and pauses Rythmbox.

## Usage
The script only requires dbus-python

pip install dbus-python

to run the script simply execute it

python3 android_like_sound.py

## Why?
In case you want one of the more annoing Features of Mobile Operating systems the choice is yours.
