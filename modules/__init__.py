# modules/__init__.py

# This makes the classes available directly from the 'modules' package.
# It allows you to do: "from modules import Config, ScreenEyes"
# instead of: "from modules.config import Config"

from .config import Config
from .eyes import ScreenEyes
from .brain import AcademicBrain
from .enforcer import PoliceOfficer
from .resource_manager import ResourceManager