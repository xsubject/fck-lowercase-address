from typing import Callable
from PIL import Image, ImageDraw
import pystray


class Tray:

    def __init__(self, on_toggle_monitoring: Callable[[], None], on_toggle_checksum_mode: Callable[[], None], on_quit: Callable[[], None]):
        self.image = self.make()
        menu_items = []
        self.tray_icon = pystray.Icon(
            "ethereum_monitor",
            self.image,
            "Ethereum Address Monitor",
            pystray.Menu(*menu_items)
        )

        self.on_toggle_monitoring = on_toggle_monitoring
        self.on_toggle_checksum_mode = on_toggle_checksum_mode
        self.on_quit = on_quit

        self.monitoring = True
        self.checksum_mode = False

    def update_tray_icon(self):
        if self.tray_icon:
            new_image = self.make(self.checksum_mode, self.monitoring)
            self.tray_icon.icon = new_image

    def run(self):
        if self.tray_icon:
            self.tray_icon.run()
        else:
            print("Tray icon not initialized.")

    def stop(self):
        if self.tray_icon:
            self.tray_icon.stop()
        else:
            print("Tray icon not initialized.")


    def update_menu(self):

        menu_items = [
            pystray.MenuItem(
                "Enable",
                self.on_toggle_monitoring,
                checked=lambda item: self.monitoring
            ),
            pystray.MenuItem(
                "Mode: Checksum" if self.checksum_mode else "Mode: Lowercase",
                self.on_toggle_checksum_mode,
                checked=lambda item: self.checksum_mode
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.on_quit)
        ]
        
        self.tray_icon.menu = pystray.Menu(*menu_items)
    

    def update(self):
        if self.tray_icon:
            self.update_menu()
            self.update_tray_icon()
            
        else:
            print("Tray icon not initialized.")

    def make(self, is_checksum=False, enabled=True):
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
