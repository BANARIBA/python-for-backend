age: float = 25
licensed: bool = False

if age >= 18 and licensed:
  print('You can drive in downtown')

is_student: bool = False
membership: bool = True
if is_student or membership:
  print('Get special price')
  
is_admin: bool = False
if not is_admin:
  print('You does not have privileges for this')
