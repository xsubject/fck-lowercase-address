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
    
    def play_sound(self, mode):
        sound_thread = threading.Thread(target=self._play_sound_threaded, args=(mode,))
        sound_thread.daemon = True
        sound_thread.start()


    def _play_sound_threaded(self, mode):
        """Play different sounds for different modes"""
        try:
            if sys.platform == 'darwin':
                self.play_macos_sound(mode)
            elif sys.platform == 'win32':
                self.play_windows_sound(mode)
            else:
                self.play_linux_sound(mode)
        except Exception as e:
            print(f"Sound error: {e}")
    
    def play_macos_sound(self, mode):
        """Play macOS system sounds"""
        import subprocess
        if mode == 'lowercase':
            subprocess.run(['afplay', '-t', '1', '-v', '0.35', '-r', '1.5', '/System/Library/Sounds/Purr.aiff'], check=False, timeout=1.5)
            pass
        else:
            subprocess.run(['afplay', '-t', '1', '-v', '0.35', '-r', '1.5', '/System/Library/Sounds/Blow.aiff'], check=False, timeout=1.5)
    
    def play_windows_sound(self, mode):
        """Play Windows system sounds"""
        import winsound
        if mode == 'lowercase':
            winsound.Beep(400, 200)
        else:
            winsound.Beep(800, 200)
    
    def play_linux_sound(self, mode):
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
        

    
    def create_tray_icon(self, is_checksum=False, enabled=True):
        size = (64, 64)
        radius = 360

        image = Image.new('RGBA', size, (0, 0, 0, 0))

        mask = Image.new('L', size, 0)
        mask_draw = ImageDraw.Draw(mask)
        opacity = 255 if enabled else 200


        mask_draw.rounded_rectangle((0, 0, *size), radius=radius, fill=opacity)
        icon = Image.new('RGBA', size, (255, 255, 255, 220))
        draw = ImageDraw.Draw(icon)
        
        color = 'green' if is_checksum else 'red'
        
        if enabled:
            if is_checksum:
                triangle_points = [
                    (32, 20), 
                    (22, 44),
                    (42, 44)   
                ]
            else:
                triangle_points = [
                    (22, 20),  
                    (42, 20), 
                    (32, 44)  
                ]
            draw.polygon(triangle_points, fill=color, outline='white')
        else:
            draw.ellipse([20, 18, 44, 35], fill='black')
            draw.ellipse([22, 20, 42, 33], fill='white')
            draw.rectangle([30, 28, 34, 40], fill='black')
            draw.ellipse([30, 42, 34, 46], fill='black')
            image.paste(icon, (0, 0), mask)

        image.paste(icon, (0, 0), mask)

        return image

    def update_tray_icon(self):
        if self.tray_icon:
            new_image = self.create_tray_icon(self.checksum_mode, self.monitoring)
            self.tray_icon.icon = new_image

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
        
        self.play_sound(mode_text)
        
        if self.tray_icon:
            self.update_menu()
            self.update_tray_icon()
    
    def toggle_monitoring(self, icon, item):
        self.monitoring = not self.monitoring
        if self.monitoring:
            print("Monitoring resumed")
            monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
            monitor_thread.start()
        else:
            print("Monitoring paused")
        
        if self.tray_icon:
            self.update_menu()
            self.update_tray_icon()
    
    def update_menu(self):
        menu_items = [
            pystray.MenuItem(
                "Enable",
                self.toggle_monitoring,
                checked=lambda item: self.monitoring
            ),
            pystray.MenuItem(
                "Mode: Checksum" if self.checksum_mode else "Mode: Lowercase",
                self.toggle_checksum_mode,
                checked=lambda item: self.checksum_mode
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_app)
        ]
        
        self.tray_icon.menu = pystray.Menu(*menu_items)
    
    def show_last_clipboard(self, icon, item):
        current = pyperclip.paste()
        print(f"Current clipboard: {current}")
    
    def quit_app(self, icon, item):
        print("Shutting down...")
        self.monitoring = False
        icon.stop()
        sys.exit(0)
    
    def run(self):
        image = self.create_tray_icon(self.checksum_mode, self.monitoring)
        
        menu_items = []
        
        self.tray_icon = pystray.Icon(
            "ethereum_monitor",
            image,
            "Ethereum Address Monitor",
            pystray.Menu(*menu_items)
        )
        self.update_menu()
        self.update_tray_icon()
        
        monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        monitor_thread.start()
        
        try:
            self.tray_icon.run()
        except KeyboardInterrupt:
            print("\nReceived interrupt signal, shutting down...")
            self.monitoring = False
            sys.exit(0)

if __name__ == "__main__":
    monitor = EthereumClipboardMonitor()
    monitor.run()