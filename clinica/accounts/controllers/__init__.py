from .auth_controller import AuthController
from .appointment_controller import AppointmentController

# __init__.py for the controllers package

# Importing all controllers to make them available when the package is imported

__all__ = ['AuthController', 'AppointmentController']