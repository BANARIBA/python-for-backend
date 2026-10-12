def required_authentication(function_how_argument):
    def wrapper(user):
        if user == "admin":
            return function_how_argument(user)
        else:
            return "401-Unauthorized!"
    return wrapper

@required_authentication
def admin_dashboard(user):
    return f"Bienvenido, {user}"

print(admin_dashboard("sales"))
print(admin_dashboard("admin"))

