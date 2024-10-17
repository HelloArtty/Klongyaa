import threading

from pygame import mixer

mixer.init()
sound_notification = mixer.Sound("../Klongyaa/screen/homeScreen/sound_notification.wav")

sound_cooldown = False

def releaseCooldown():
    global sound_cooldown
    sound_cooldown = False

def playSound():
    global sound_cooldown
    if not sound_cooldown:
        sound_notification.play()
        sound_cooldown = True
        threading.Timer(2, releaseCooldown).start()

def stopSound():
    sound_notification.stop()