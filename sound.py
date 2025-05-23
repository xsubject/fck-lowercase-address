import sys
import threading


def play_sound( mode):
    sound_thread = threading.Thread(target=_play_sound_threaded, args=(mode,))
    sound_thread.daemon = True
    sound_thread.start()


def _play_sound_threaded(mode):
    """Play different sounds for different modes"""
    try:
        if sys.platform == 'darwin':
            play_macos_sound(mode)
        elif sys.platform == 'win32':
            play_windows_sound(mode)
        else:
            play_linux_sound(mode)
    except Exception as e:
        print(f"Sound error: {e}")

def play_macos_sound(mode):
    """Play macOS system sounds"""
    import subprocess
    if mode == 'lowercase':
        subprocess.run(['afplay', '-t', '1', '-v', '0.35', '-r', '1.5', '/System/Library/Sounds/Purr.aiff'], check=False, timeout=1.5)
        pass
    else:
        subprocess.run(['afplay', '-t', '1', '-v', '0.35', '-r', '1.5', '/System/Library/Sounds/Blow.aiff'], check=False, timeout=1.5)

def play_windows_sound(mode):
    """Play Windows system sounds"""
    import winsound
    if mode == 'lowercase':
        winsound.Beep(400, 200)
    else:
        winsound.Beep(800, 200)

def play_linux_sound(mode):
    """Play Linux sounds using pactl or beep"""
    import subprocess
    try:
        if mode == 'lowercase':
            subprocess.run(['pactl', 'upload-sample', '/usr/share/sounds/alsa/Front_Left.wav'], check=False, capture_output=True)
        else:
            subprocess.run(['pactl', 'upload-sample', '/usr/share/sounds/alsa/Front_Right.wav'], check=False, capture_output=True)
    except:
        try:
            if mode == 'lowercase':
                subprocess.run(['beep', '-f', '400', '-l', '200'], check=False)
            else:
                subprocess.run(['beep', '-f', '800', '-l', '200'], check=False)
        except:
            print(f"🔊 Sound: {mode}")
    
