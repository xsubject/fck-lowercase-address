# Ethereum Address Lowercase Converter

A simple clipboard monitor that automatically converts Ethereum addresses to lowercase when you copy them.

## What does it do?

🔍 Monitors your clipboard  
🔄 Converts Ethereum addresses (0x...) to lowercase automatically  
🖱️ Runs quietly in system tray  
✨ That's it. Simple as that.

## Why?

If you don't know why you need this, then enjoy your life outside of this repository 🌻

## Quick Start

### Requirements

-   Python 3.7+
-   A computer (surprisingly important)
-   The will to live with crypto addresses

### Installation

```bash
# Clone or download this repo
git clone <this-repo>
cd ethereum-lowercase-converter

# Install dependencies
pip3 install -r requirements.txt

# Run it
python3 clipboard_monitor.py
```

## How to use

1. Run the script
2. Copy any Ethereum address like `0xA0b86a33E6441e843CE5a5E1f8b2e2F7B5B3F4f8`
3. It magically becomes `0xa0b86a33e6441e843ce5a5e1f8b2e2f7b5b3f4f8`

## System Tray

Right-click the tray icon to:

-   Stop/Start monitoring
-   Exit (if you've had enough)

## Autostart

```bash
# Install autostart
python3 autostart.py install

# Remove autostart (when you realize you don't need this anymore)
python3 autostart.py remove
```

## Troubleshooting

**"It's not working!"**

-   Did you install the dependencies?
-   Are you copying actual Ethereum addresses?
-   Did you try turning it off and on again?

**"I don't see the tray icon!"**

-   Look harder
-   Check if your system tray is hidden
-   Maybe you're on Linux (not supported, sorry)

**"This is stupid!"**

-   You're probably right
-   But here we are

## What it recognizes

Valid Ethereum addresses:

-   Starts with `0x`
-   Followed by exactly 40 hexadecimal characters
-   Like `0xdeadbeefcafebabe...` (but with more characters)

## Privacy

-   Only touches your clipboard
-   Doesn't save anything
-   Doesn't send data anywhere
-   Your secrets are safe (from this script at least)
