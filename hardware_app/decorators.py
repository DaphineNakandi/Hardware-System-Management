# hardware_app/decorators.py
from django.core.exceptions import PermissionDenied

def role_required(role_check_func):
    
    #Decorator to check if user passes a specific role check function
    
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if role_check_func(request.user):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("You don't have permission to access this page.")
        return wrapper
    return decorator