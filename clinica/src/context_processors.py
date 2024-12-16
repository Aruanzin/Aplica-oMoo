
def user_type(request):
    user_type = None
    user = request.user
    if user.is_authenticated:
        if hasattr(user, 'clinicowner'):
            user_type = 'clinic_owner'
        elif hasattr(user, 'secretary'):
            user_type = 'secretary'
        elif hasattr(user, 'dentist'):
            user_type = 'dentist'
        elif hasattr(user, 'client'):
            user_type = 'client'
    return {'user_type': user_type}