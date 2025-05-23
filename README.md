# Ethereum Address Converter

A simple clipboard monitor that automatically converts Ethereum addresses to lowercase or checksum format when you copy them.

## What does it do?

🔍 Monitors your clipboard  
🔄 Converts Ethereum addresses (0x...) to lowercase OR checksum format  
🖱️ Runs quietly in system tray  
🔊 Audio feedback with different sounds for each mode  
⚡ Switch between modes on the fly with hotkeys  
✨ That's it. Simple as that.

## Why?

If you don't know why you need this, then enjoy your life outside of this repository 🌻

For the rest of us who deal with the eternal struggle of mixed-case Ethereum addresses... you know the pain.

## Quick Start

### Requirements
- Python 3.7+
- A computer (surprisingly important)
- The will to live with crypto addresses

### Installation

```bash
# Clone or download this repo
git clone <this-repo>
cd ethereum-address-converter

# Install dependencies
pip3 install -r requirements.txt

# Run it
python3 clipboard_monitor.py
```

### Dependencies
```
pyperclip
pystray
pillow
pynput
```

For Windows:
```
winsound (built-in)
```

For macOS:
```
pyobjc-framework-Cocoa
pyobjc-framework-Foundation
```

## How to use

1. Run the script
2. Copy any Ethereum address like `0xA0b86a33E6441e843CE5a5E1f8b2e2F7B5B3F4f8`
3. **Lowercase mode**: It becomes `0xa0b86a33e6441e843ce5a5e1f8b2e2f7b5b3f4f8` 🔉 *low beep*
4. **Checksum mode**: It becomes `0xA0B86a33E6441E843cE5a5E1F8B2e2f7b5B3F4F8` (EIP-55 format) 🔊 *high beep*
5. Profit??? 

## Controls

### Hotkey
- **Ctrl+Shift+0** (Windows/Linux) or **Cmd+Shift+0** (macOS): Toggle between modes

### System Tray
Right-click the tray icon to:
- Stop/Start monitoring
- **Switch between Lowercase/Checksum modes**
- Show current clipboard content  
- Exit (if you've had enough)

## Audio Feedback

Different sounds play for different modes:

**Windows:**
- Lowercase: 400Hz beep
- Checksum: 800Hz beep

**macOS:**
- Lowercase: "Tink" system sound
- Checksum: "Glass" system sound

**Linux:**
- Lowercase: 400Hz beep (via `beep` command)
- Checksum: 800Hz beep (via `beep` command)

## Modes

**Lowercase Mode** (default): Converts everything to lowercase  
**Checksum Mode**: Converts to EIP-55 checksum format (mixed case for validation)

The app remembers your last selected mode between sessions.

## Platform Support

✅ **Windows**: Full support with native sounds  
✅ **macOS**: Full support with system sounds and hidden dock icon  
✅ **Linux**: Basic support (may require `beep` package for audio)

## Troubleshooting

**"It's not working!"**
- Did you install the dependencies?
- Are you copying actual Ethereum addresses?
- Did you try turning it off and on again?

**"I don't see the tray icon!"**
- Look harder
- Check if your system tray is hidden
- On some Linux distributions, system tray support might be limited

**"No sound is playing!"**
- On Linux: Install `beep` package (`sudo apt install beep`)
- Check your system volume
- Audio might be muted or routed to wrong device

**"This is stupid!"**
- You're probably right
- But here we are

## What it recognizes

Valid Ethereum addresses:
- Starts with `0x`
- Followed by exactly 40 hexadecimal characters (0-9, a-f, A-F)
- Like `0xdeadbeefcafebabe...` (but with more characters)

Examples:
- `0x742d35Cc6644C9532C5A3aF4F6dA6e6Db4A6d5F0` ✅
- `0x742D35CC6644C9532C5A3AF4F6DA6E6DB4A6D5F0` ✅
- `0x742d35cc6644c9532c5a3af4f6da6e6db4a6d5f0` ✅
- `742d35Cc6644C9532C5A3aF4F6dA6e6Db4A6d5F0` ❌ (no 0x)
- `0x742d35Cc6644C9532C` ❌ (too short)

## Privacy

- Only touches your clipboard
- Doesn't save anything to disk
- Doesn't send data anywhere
- Runs completely offline
- Your secrets are safe (from this script at least)

## Background Operation

The app runs quietly in the background:
- **Windows**: Console window is hidden automatically
- **macOS**: App doesn't appear in dock (LSUIElement = 1)
- **Linux**: Run with `nohup` for background operation

## License

Do whatever you want with this code. If it breaks your computer, that's on you.

MIT License or whatever makes lawyers happy.

---

*Made with ❤️ and mild frustration by someone who got tired of manually converting addresses*