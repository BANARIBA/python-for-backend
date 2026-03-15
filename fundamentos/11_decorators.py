def required_auth(func):
  def wrapper(user: str):
    if (user == 'admin'):
      return func(user)
    else:
      return "Acceso denegado!"
  return wrapper

@required_auth
def admin_dashboard(user):
  return f"Bienvenido al panel {user}"

print(admin_dashboard("guest"))
print(admin_dashboard("admin"))