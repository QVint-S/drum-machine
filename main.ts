let playing = false
let selectedLoop = 0
let radioGroup = 3
radio.setGroup(radioGroup)
music.setBuiltInSpeakerEnabled(true)
music.setVolume(255)
music.setTempo(120)
led.plot(0, 2)
music.play(music.stringPlayable("A C5", 500), music.PlaybackMode.UntilDone)
let Kick = music.createSoundExpression(WaveShape.Square, 523, 1, 255, 0, 100, SoundExpressionEffect.Tremolo, InterpolationCurve.Logarithmic)
let Snare = music.createSoundExpression(WaveShape.Square, 400, 100, 255, 255, 100, SoundExpressionEffect.None, InterpolationCurve.Curve)
let Hihat = music.createSoundExpression(WaveShape.Noise, 3189, 3154, 255, 76, 30, SoundExpressionEffect.None, InterpolationCurve.Linear)
let loopList = [["p", "", "", "", "k", "", "", "p", "p", "", "p", "", "k", "", "", ""], ["p", "", "t", "", "k", "", "p", "", "t", "", "p", "", "k", "", "t", ""], ["p", "", "t", "p", "k", "", "p", "", "t", "k", "p", "", "k", "", "t", "k"], ["p", "t", "t", "p", "k", "t", "p", "t", "t", "p", "p", "t", "k", "t", "t", "p"], ["p", "t", "t", "k", "", "", "p", "", "t", "k", "p", "", "k", "", "t", "t"], ["p", "", "t", "", "k", "", "t", "", "t", "", "p", "t", "p", "k", "t", ""], ["p", "", "t", "", "k", "", "t", "", "p", "", "t", "", "k", "", "t"]]
radio.onReceivedString(function on_received_string(receivedString: string) {
    
    if (receivedString == "TogglePlay") {
        if (playing) {
            playing = false
            led.unplot(2, 0)
        } else {
            playing = true
            led.plot(2, 0)
        }
        
    } else if (receivedString == "Previous" && selectedLoop > 0) {
        selectedLoop -= 1
        basic.clearScreen()
        led.plot(Math.min(selectedLoop, 4), 2)
    } else if (receivedString == "Next" && selectedLoop < loopList.length - 1) {
        selectedLoop += 1
        basic.clearScreen()
        led.plot(Math.min(selectedLoop, 4), 2)
    }
    
})
radio.onReceivedNumber(function on_received_number(receivedNumber: number) {
    let soundToPlay: SoundExpression;
    
    if (playing) {
        for (let sound of loopList[selectedLoop]) {
            if (sound) {
                if (sound == "p") {
                    soundToPlay = Kick
                } else if (sound == "k") {
                    soundToPlay = Snare
                } else if (sound == "t") {
                    soundToPlay = Hihat
                }
                
                music.play(soundToPlay, music.PlaybackMode.InBackground)
            }
            
            music.rest(music.beat(BeatFraction.Whole) + 2)
        }
    }
    
})
