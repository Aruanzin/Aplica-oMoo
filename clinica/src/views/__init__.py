from .authentication import login_view, logout_view, register_view
from .home import home_view
from .appointment import (
    request_appointment_view,
    get_available_times,
    manage_appointments_view,
    accept_appointment_view,
    reject_appointment_view,
    view_appointments
)
from .schedule import (
    manage_schedule_view,
    toggle_schedule_view
)
from .configuration import configure_user_view
from .password_reset import reset_password_view
