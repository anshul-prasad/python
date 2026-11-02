from playsound3 import playsound
import time

CLEAR = "\033[2J"
CLEAR_AND_RETURN = "\033[H"

def alarm(seconds):
    time_elapsed = 0
    print(CLEAR)
    while time_elapsed < seconds:
        time.sleep(1)
        time_elapsed += 1
        time_left = seconds - time_elapsed
        minutes_left, seconds_left = divmod(time_left, 60)
        print(f"{CLEAR_AND_RETURN}Alarm will sound in: {minutes_left:02d}:{seconds_left:02d}")
    playsound("utility/alarm_sound.mp3")

minutes = int(input("How many minutes to wait: "))
seconds = int(input("How many seconds to wait: "))

alarm(minutes * 60 + seconds)