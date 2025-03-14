import requests
import functools

TAP_IP="172.16.0.1"

def in_ai_dev():
    """
    A decorator that replaces the function it decorates with code fetched from a URL.
    If no URL is provided, it uses http://tapip:8000/{filename}/{functionname}

    Args:
        url (str, optional): The URL to fetch the replacement function code from.
                            Defaults to None, which uses the dynamic URL pattern.

    Returns:
        function: The decorator function.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Simple pause to allow for manual forking.
                input("Press Enter to continue...")

                # Get the filename and function name
                import inspect
                filename = inspect.getmodule(func).__file__
                if filename:
                    filename = filename.split('/')[-1]
                else:
                    raise ValueError("Could not get the filename of the function")
                function_name = func.__name__

                # Use the provided URL or build the dynamic URL
                endpoint_url = f"http://{TAP_IP}:8000/{filename}/{function_name}"

                response = requests.get(endpoint_url)
                response.raise_for_status()

                # Get the code from the response
                code = response.json()["code"]

                # Create a new local namespace
                local_namespace = { }

                # Execute the remote code in the local namespace, this will define the function.
                exec(code, func.__globals__, local_namespace)

                # Get the function with the same name from the local namespace
                if func.__name__ in local_namespace:
                    remote_func = local_namespace[func.__name__]
                    return remote_func(*args, **kwargs)
                else:
                    # If no function with the same name exists, execute the first function defined
                    for name, obj in local_namespace.items():
                        if callable(obj) and not name.startswith('__'):
                            return obj(*args, **kwargs)

                    # If no function is found, fall back to the original function
                    raise ValueError("No function found in the remote code")
            except Exception as e:
                print(f"Error fetching or executing remote code: {e}")
                raise
                # Fall back to the original function in case of error
                # return func(*args, **kwargs)
        return wrapper
    return decorator
