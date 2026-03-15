is_new_dev: bool = False
knows_python: bool = False
interested_python: bool = True

if is_new_dev:
  print('Te recomiendo saber python')
elif interested_python:
  print('Aprende en el curso x')
else:
  print('Inicia en este mundo de la programacion')
  
if knows_python:
  print('Te recomiendo aprender Django')