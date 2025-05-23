#!/usr/bin/env python3
import time
import re
import pyperclip
import pystray
from PIL import Image, ImageDraw
import threading
import sys
import os

# Hiding the icon from the dock
if sys.platform == 'darwin':
    import AppKit
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info["LSUIElement"] = "1"
# Hide the icon from the taskbar
elif sys.platform == 'win32':
    import ctypes
    from ctypes import wintypes
    
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
        
        self.eth_pattern = re.compile(r'0x[a-fA-F0-9]{40}')
        
    def create_tray_icon(self):
        image = Image.new('RGB', (64, 64), color='black')
        draw = ImageDraw.Draw(image)
        
        draw.ellipse([16, 16, 48, 48], fill='blue', outline='white', width=2)
        
        return image

    def is_ethereum_address(self, text):
        return bool(self.eth_pattern.fullmatch(text.strip()))
    
    def normalize_ethereum_address(self, address):
        return address.lower()
    
    def monitor_clipboard(self):
        print("For exiting the program, use Ctrl+C or click the tray icon.")
        
        while self.monitoring:
            try:
                current_clipboard = pyperclip.paste()
                
                if current_clipboard != self.last_clipboard:
                    self.last_clipboard = current_clipboard
                    
                    if self.is_ethereum_address(current_clipboard):
                        normalized_address = self.normalize_ethereum_address(current_clipboard)
                        
                        if normalized_address != current_clipboard:
                            pyperclip.copy(normalized_address)
                            print(f"Found address:")
                            print(f"Before: {current_clipboard}")
                            print(f"After: {normalized_address}")
                            print("-" * 50)
                        else:
                            print(f"Eth address already in lowercase: {current_clipboard}")
                    
                time.sleep(0.5) 
                
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(1)
    
    def toggle_monitoring(self, icon, item):
        self.monitoring = not self.monitoring
        if self.monitoring:
            monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
            monitor_thread.start()
        else:
            print("Paused monitoring.")
        
        self.update_menu()
    
    def update_menu(self):
        menu_items = [
            pystray.MenuItem(
                "Stop" if self.monitoring else "Start",
                self.toggle_monitoring,
                checked=lambda item: self.monitoring
            ),
            pystray.MenuItem("Show latest", self.show_last_clipboard),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Close", self.quit_app)
        ]
        
        self.tray_icon.menu = pystray.Menu(*menu_items)
    
    def show_last_clipboard(self, icon, item):
        current = pyperclip.paste()
        print(f"Current: {current}")
    
    def quit_app(self, icon, item):
        print("Exiting...")
        self.monitoring = False
        icon.stop()
        sys.exit(0)
    
    def run(self):
        image = self.create_tray_icon()
        
        menu_items = [
            pystray.MenuItem(
                "Stop",
                self.toggle_monitoring,
                checked=lambda item: self.monitoring
            ),
            pystray.MenuItem("Show latest", self.show_last_clipboard),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self.quit_app)
        ]
        
        self.tray_icon = pystray.Icon(
            "ethereum_monitor",
            image,
            "Ethereum Address Monitor",
            pystray.Menu(*menu_items)
        )
        
        monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        monitor_thread.start()
        
        try:
            self.tray_icon.run()
        except KeyboardInterrupt:
            print("\nExiting...")
            self.monitoring = False
            sys.exit(0)

if __name__ == "__main__":
    monitor = EthereumClipboardMonitor()
    monitor.run()