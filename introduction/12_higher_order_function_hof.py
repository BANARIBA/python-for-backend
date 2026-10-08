# Funcion que recibe otra funcion

def required_authentication(function_how_argument):
    def wrapper(user):
        if user == "admin":
            return function_how_argument(user)
        else:
            return "401-Unauthorized!"
    return wrapper

# esta es la que vamos a pasar como function_how_argument
def admin_dashboard(user):
    return f"Bienvenido, {user}"

auth_view_dashboard = required_authentication(admin_dashboard)

print(auth_view_dashboard("sales"))
print(auth_view_dashboard("admin"))

