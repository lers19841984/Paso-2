from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import os

# Módulos de Android
from android.permissions import request_permissions, Permission
from android.storage import app_storage_path

class MiInterfaz(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        self.label = Label(text="Introduce un texto para guardar:")
        self.add_widget(self.label)
        
        self.entrada = TextInput(hint_text="Escribe aquí...", multiline=False)
        self.add_widget(self.entrada)
        
        self.boton_guardar = Button(text="Guardar texto")
        self.boton_guardar.bind(on_press=self.guardar_texto)
        self.add_widget(self.boton_guardar)

        self.boton_leer = Button(text="Leer texto guardado")
        self.boton_leer.bind(on_press=self.leer_texto)
        self.add_widget(self.boton_leer)
        
        self.resultado = Label(text="")
        self.add_widget(self.resultado)

        # Ruta de almacenamiento
        self.carpeta = os.path.join(app_storage_path(), "MiAppKivy")
        os.makedirs(self.carpeta, exist_ok=True)
        self.ruta_archivo = os.path.join(self.carpeta, "datos.txt")

    def guardar_texto(self, instance):
        texto = self.entrada.text.strip()
        if not texto:
            self.resultado.text = "⚠️ No se puede guardar texto vacío."
            return

        try:
            with open(self.ruta_archivo, "a") as archivo:
                archivo.write(texto + "\n")
            self.resultado.text = "✅ Texto guardado correctamente."
            self.entrada.text = ""
        except Exception as e:
            self.resultado.text = f"❌ Error al guardar: {str(e)}"

    def leer_texto(self, instance):
        try:
            if not os.path.exists(self.ruta_archivo):
                self.resultado.text = "⚠️ El archivo aún no existe."
                return

            with open(self.ruta_archivo, "r") as archivo:
                contenido = archivo.read()
            self.resultado.text = f"📄 Contenido:\n{contenido}"
        except Exception as e:
            self.resultado.text = f"❌ Error al leer: {str(e)}"

class MiApp(App):
    def build(self):
        # Pedir permisos de almacenamiento
        request_permissions([
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE
        ])
        return MiInterfaz()

if __name__ == "__main__":
    MiApp().run()
