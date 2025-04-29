from functools import wraps
import traceback

def catch_exceptions(method_name=""):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                # Capture error + traceback
                error_message = f"{type(e).__name__}: {str(e) if str(e) else traceback.format_exc()}"
                self.logger.error(f"Error en {method_name or func.__name__}: {error_message}")
                raise
        return wrapper
    return decorator
