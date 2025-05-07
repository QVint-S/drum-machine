playing = False
selectedLoop = 0
radioGroup = 3
radio.set_group(radioGroup)
music.set_built_in_speaker_enabled(True)
music.set_volume(255)
music.set_tempo(120)
led.plot(0, 2)
music.play(music.string_playable("E G A C5 - - - - ", 500),
    music.PlaybackMode.UNTIL_DONE)

Kick = music.create_sound_expression(WaveShape.SQUARE,
    523,
    1,
    255,
    0,
    100,
    SoundExpressionEffect.TREMOLO,
    InterpolationCurve.LOGARITHMIC)

Snare = music.create_sound_expression(WaveShape.SQUARE,
    400,
    100,
    255,
    255,
    100,
    SoundExpressionEffect.NONE,
    InterpolationCurve.CURVE)

Hihat = music.create_sound_expression(WaveShape.NOISE,
    3189,
    3154,
    255,
    76,
    30,
    SoundExpressionEffect.NONE,
    InterpolationCurve.LINEAR)

loopList = [
["p", "", "", "", "k", "", "", "p", "p", "", "p", "", "k", "", "", ""],
["p", "", "t", "", "k", "", "p", "", "t", "", "p", "", "k", "", "t", ""],
["p", "", "t", "p", "k", "", "p", "", "t", "k", "p", "", "k", "", "t", "k"],
["p", "t", "t", "p", "k", "t", "p", "t", "t", "p", "p", "t", "k", "t", "t", "p"],
["p", "t", "t", "k", "", "", "p", "", "t", "k", "p", "", "k", "", "t", "t"],
["p", "", "t", "", "k", "", "t", "", "t", "", "p", "t", "p", "k", "t", ""],
["p", "", "t", "", "k", "", "t", "", "p", "", "t", "", "k", "", "t"]
]

def on_received_string(receivedString):
    global playing, selectedLoop, loopList

    if receivedString == "TogglePlay":
            if playing:
                playing = False
                led.unplot(2, 0)
            else:
                playing = True
                led.plot(2, 0)

    elif receivedString == "Previous" and selectedLoop > 0:
        selectedLoop -= 1
        basic.clear_screen()
        led.plot(min(selectedLoop, 4), 2)
    elif receivedString == "Next" and selectedLoop < len(loopList) - 1:
        selectedLoop += 1
        basic.clear_screen()
        led.plot(min(selectedLoop, 4), 2)
radio.on_received_string(on_received_string)

def on_received_number(receivedNumber):
    global playing, selectedLoop, loopList
    if playing:
        for sound in loopList[selectedLoop]:
            if sound:
                if sound == "p":
                    soundToPlay = Kick
                elif sound == "k":
                    soundToPlay = Snare
                elif sound == "t":
                    soundToPlay = Hihat
                else:
                    basic.pause(10)
                music.play(soundToPlay, music.PlaybackMode.IN_BACKGROUND)
            music.rest(music.beat(BeatFraction.WHOLE) + 2)
radio.on_received_number(on_received_number)