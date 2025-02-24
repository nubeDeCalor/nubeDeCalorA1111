import flet as ft
import threading
import time
from pyobjus import autoclass


class AccelerometerVisualizer(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.motionManager = None
        self.update_thread = None

    def build(self):
        # Componentes para mostrar los datos de aceleración
        self.label_x = ft.Text("Aceleración en X: --")
        self.label_y = ft.Text("Aceleración en Y: --")
        self.label_z = ft.Text("Aceleración en Z: --")
        # Botón para iniciar/detener la lectura
        self.start_button = ft.ElevatedButton("Start", on_click=self.toggle_start)
        return ft.Column(
            controls=[
                self.label_x,
                self.label_y,
                self.label_z,
                self.start_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    def toggle_start(self, event):
        if not self.is_running:
            # Comenzar la lectura de acelerómetro
            self.start_button.text = "Stop"
            self.is_running = True

            # Inicializar el CMMotionManager a través de pyobjus
            CMMotionManager = autoclass("CMMotionManager")
            self.motionManager = CMMotionManager.alloc().init()

            if self.motionManager.isAccelerometerAvailable():
                self.motionManager.startAccelerometerUpdates()
                # Iniciar un hilo para actualizar los datos en la UI
                self.update_thread = threading.Thread(
                    target=self.update_loop, daemon=True
                )
                self.update_thread.start()
            else:
                self.label_x.value = "Acelerómetro no disponible."
                self.is_running = False
                self.start_button.text = "Start"
        else:
            # Detener la lectura de acelerómetro
            self.is_running = False
            self.start_button.text = "Start"
            if self.motionManager:
                self.motionManager.stopAccelerometerUpdates()

        self.update()  # Actualiza la UI inmediatamente para reflejar el cambio de estado

    def update_loop(self):
        while self.is_running:
            # Obtener datos del acelerómetro
            accelData = self.motionManager.accelerometerData()
            if accelData:
                # Se asume que accelData.acceleration() devuelve un objeto con propiedades x, y, z
                acceleration = accelData.acceleration()
                self.label_x.value = f"Aceleración en X: {acceleration.x:.2f}"
                self.label_y.value = f"Aceleración en Y: {acceleration.y:.2f}"
                self.label_z.value = f"Aceleración en Z: {acceleration.z:.2f}"
            else:
                self.label_x.value = "No se reciben datos."
                self.label_y.value = ""
                self.label_z.value = ""
            # Actualizar la interfaz; este método es thread-safe en flet
            self.update()
            time.sleep(0.1)  # Actualiza cada 0.1 segundos


def main(page: ft.Page):
    page.title = "Visualizador del Acelerómetro"
    # Se centra el contenido
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(AccelerometerVisualizer())


ft.app(target=main)
