def required_auth(func):
  def wrapper(user: str):
    if (user == 'admin'):
      return func(user)
    else:
      return "Acceso denegado!"
  return wrapper

def admin_dashboard(user):
  return f"Bienvenido al panel {user}"

admin_view_dasboard = required_auth(admin_dashboard)
print(admin_view_dasboard("guest"))
print(admin_view_dasboard("admin"))