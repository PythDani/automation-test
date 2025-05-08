from functools import wraps
import traceback

def catch_exceptions(method_name=""):

    """
    Decorator to catch exceptions and log them, re-raising the error afterwards.

    The decorator will capture the exception and log it with the given method_name
    (or the function name if not provided) and append the error message (if any)
    and the traceback.

    :param method_name: The name of the method to be used in the log message
    :type method_name: str
    :return: The decorated function
    :rtype: callable
    """
    
    def decorator(func):
        """
        Decorator to catch exceptions and log them, re-raising the error afterwards.

        The decorator will capture the exception and log it with the given method_name
        (or the function name if not provided) and append the error message (if any)
        and the traceback.

        :param func: The function to be decorated
        :type func: callable
        :return: The decorated function
        :rtype: callable
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            """
            Function that wraps the original function to catch exceptions and log them, re-raising
            the error afterwards.

            The wrapper will capture the exception and log it with the given method_name (or the
            function name if not provided) and append the error message (if any) and the traceback.

            :param self: The instance of the class where the original function is defined
            :param args: The arguments passed to the original function
            :param kwargs: The keyword arguments passed to the original function
            :return: The result of the original function if no exception is raised
            :rtype: The type of the result of the original function
            """


            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                # Capture error + traceback
                error_message = f"{type(e).__name__}: {str(e) if str(e) else traceback.format_exc()}"
                self.logger.error(f"Error in {method_name or func.__name__}: {error_message}")

                raise
        return wrapper
    return decorator
