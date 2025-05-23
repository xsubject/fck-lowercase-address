#!/usr/bin/env python3
import time
import re
import pyperclip
import pystray
from PIL import Image, ImageDraw
import threading
import sys
from pynput import keyboard
from eth_utils import to_checksum_address

from sound import play_sound
from tray_icon import Tray

if sys.platform == 'darwin':
    import AppKit
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info["LSUIElement"] = "1"
elif sys.platform == 'win32':
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_HIDE = 0
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, SW_HIDE)

class EthereumClipboardMonitor:
    def __init__(self):
        self.last_clipboard = ""
        self.monitoring = True
        self.tray_icon = None
        self.checksum_mode = False
        self.eth_pattern = re.compile(r'0x[a-fA-F0-9]{40}')
        self.setup_hotkey()
        
    def setup_hotkey(self):
        """Setup Ctrl/Cmd + Shift + 0 hotkey"""
        def on_hotkey():
            self.toggle_checksum_mode(None, None)
        
        if sys.platform == 'darwin':
            hotkey = keyboard.HotKey(keyboard.HotKey.parse('<cmd>+<shift>+0'), on_hotkey)
        else:
            hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+<shift>+0'), on_hotkey)
        
        def for_canonical(f):
            return lambda k: f(listener.canonical(k))
        
        listener = keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)
        )
        listener.start()
    

    def is_ethereum_address(self, text):
        return bool(self.eth_pattern.fullmatch(text.strip()))

    
    def normalize_ethereum_address(self, address):
        if self.checksum_mode:
            return to_checksum_address(address)
        else:
            return address.lower()
    
    def monitor_clipboard(self):
        print("Ethereum clipboard monitor started...")
        hotkey_text = "Cmd+Shift+0" if sys.platform == 'darwin' else "Ctrl+Shift+0"
        print(f"Press {hotkey_text} to toggle between lowercase/checksum modes")
        last_mode = "lowercase" if not self.checksum_mode else "checksum"


        while self.monitoring:
            try:
                current_clipboard = pyperclip.paste()
                
                if current_clipboard != self.last_clipboard or last_mode != self.checksum_mode:
                    last_mode = self.checksum_mode
                    
                    self.last_clipboard = current_clipboard
                    
                    if self.is_ethereum_address(current_clipboard):
                        normalized_address = self.normalize_ethereum_address(current_clipboard)
                        
                        if normalized_address != current_clipboard:
                            pyperclip.copy(normalized_address)
                            self.last_clipboard = normalized_address

                            mode_text = "checksum" if self.checksum_mode else "lowercase"
                            print(f"Address converted to {mode_text}:")
                            print(f"  {current_clipboard} → {normalized_address}")
                    
                time.sleep(0.5) 
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(1)
    
    def toggle_checksum_mode(self, icon, item):
        self.checksum_mode = not self.checksum_mode
        mode_text = "checksum" if self.checksum_mode else "lowercase"
        print(f"Mode switched to: {mode_text}")
        
        play_sound(mode_text)
        
        self.tray.checksum_mode = self.checksum_mode
        self.tray.update()
    
    def toggle_monitoring(self):
        self.monitoring = not self.monitoring
        if self.monitoring:
            print("Monitoring resumed")
            monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
            monitor_thread.start()
        else:
            print("Monitoring paused")
        
        self.tray.monitoring = self.monitoring
        self.tray.update()
    
    
    def quit_app(self):
        print("Shutting down...")
        self.monitoring = False
        self.tray.stop()
        sys.exit(0)
    
    def run(self):
        self.tray = Tray(
            on_toggle_monitoring= self.toggle_monitoring,
            on_toggle_checksum_mode=self.toggle_checksum_mode,
            on_quit=self.quit_app
        )
        self.tray.update()
        
        monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        monitor_thread.start()
        
        try:
            self.tray.run()
        except KeyboardInterrupt:
            print("\nReceived interrupt signal, shutting down...")
            self.monitoring = False
            sys.exit(0)

if __name__ == "__main__":
    monitor = EthereumClipboardMonitor()
    monitor.run()