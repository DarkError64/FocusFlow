# modules/resource_manager.py
import os

class ResourceManager:
    def __init__(self):
        # Finds the 'assets' folder relative to this script
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_path = os.path.join(self.base_path, 'assets')

    def get_image_path(self, image_name):
        """
        Returns full path to an image (e.g., penalty.gif)
        """
        return os.path.join(self.assets_path, 'images', image_name)