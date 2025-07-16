from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
import os

# Estos solo funcionan en Android
from android.permissions import request_permissions, Permission
from android.storage import app_storage_path, primary_external_storage_path

class MiInterfaz(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        self.label = Label(text="Introduce un texto para guardar:")
        self.add_widget(self.label)
        
        self.entrada = TextInput(hint_text="Escribe aquí...", multiline=False)
        self.add_widget(self.entrada)
        
        self.boton_guardar = Button(text="Guardar en archivo")
        self.boton_guardar.bind(on_press=self.guardar_texto)
        self.add_widget(self.boton_guardar)
        
        self.resultado = Label(text="")
        self.add_widget(self.resultado)

    def guardar_texto(self, instance):
        texto = self.entrada.text
        if not texto.strip():
            self.resultado.text = "No se puede guardar texto vacío."
            return

        try:
            carpeta = os.path.join(primary_external_storage_path(), "MiAppKivy")
            os.makedirs(carpeta, exist_ok=True)

            ruta_archivo = os.path.join(carpeta, "datos.txt")
            with open(ruta_archivo, "a") as archivo:
                archivo.write(texto + "\n")

            self.resultado.text = f"Texto guardado en:\n{ruta_archivo}"
            self.entrada.text = ""

        except Exception as e:
            self.resultado.text = f"Error al guardar: {str(e)}"

class MiApp(App):
    def build(self):
        # Solicitar permisos en Android
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        return MiInterfaz()

if __name__ == "__main__":
    MiApp().run()