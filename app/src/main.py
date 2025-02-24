import flet as ft
import threading
import time
from pyobjus import autoclass
from pyobjus.dylib_manager import load_framework, INCLUDE

load_framework(INCLUDE.Foundation)

NSProcessInfo = autoclass("NSProcessInfo")
process_info = NSProcessInfo.processInfo()
os_version = process_info.operatingSystemVersionString().UTF8String()


class SensorVisualizer(ft.Container):
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.motionManager = None
        self.update_thread = None

        # Elementos de la UI
        self.label_x = ft.Text("Aceleración en X: --")
        self.label_y = ft.Text("Aceleración en Y: --")
        self.label_z = ft.Text("Aceleración en Z: --")
        self.sensor_status = ft.Text("Estado: Detenido")
        self.start_button = ft.ElevatedButton("Iniciar", on_click=self.toggle_start)

        self.content = ft.Column(
            controls=[
                self.label_x,
                self.label_y,
                self.label_z,
                self.sensor_status,
                self.start_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    def toggle_start(self, event):
        if not self.is_running:
            self.start_sensor()
        else:
            self.stop_sensor()
        self.update()

    def start_sensor(self):
        self.start_button.text = "Detener"
        self.is_running = True

        CMMotionManager = autoclass("CMMotionManager")
        self.motionManager = CMMotionManager.alloc().init()

        # Primero probamos con el acelerómetro
        if self.motionManager.isAccelerometerAvailable():
            self.motionManager.accelerometerUpdateInterval = 0.1  # 10 Hz
            self.motionManager.startAccelerometerUpdates()
            self.sensor_status.value = "Usando acelerómetro"
            self.update_thread = threading.Thread(
                target=self.update_accelerometer, daemon=True
            )

        # Si falla, probamos con el giroscopio
        elif self.motionManager.isGyroAvailable():
            self.motionManager.gyroUpdateInterval = 0.1
            self.motionManager.startGyroUpdates()
            self.sensor_status.value = "Usando giroscopio"
            self.update_thread = threading.Thread(target=self.update_gyro, daemon=True)

        else:
            self.sensor_status.value = "No hay sensores disponibles"
            self.is_running = False
            self.start_button.text = "Iniciar"
            return

        self.update_thread.start()

    def stop_sensor(self):
        self.is_running = False
        self.start_button.text = "Iniciar"
        if self.motionManager:
            self.motionManager.stopAccelerometerUpdates()
            self.motionManager.stopGyroUpdates()
        self.sensor_status.value = "Estado: Detenido"

    def update_accelerometer(self):
        while self.is_running and self.motionManager:
            accelData = self.motionManager.accelerometerData
            if accelData:
                acceleration = accelData.acceleration
                self.label_x.value = f"Aceleración X: {acceleration.x:.2f}g"
                self.label_y.value = f"Aceleración Y: {acceleration.y:.2f}g"
                self.label_z.value = f"Aceleración Z: {acceleration.z:.2f}g"
            self.update()
            time.sleep(0.1)

    def update_gyro(self):
        while self.is_running and self.motionManager:
            gyroData = self.motionManager.gyroData
            if gyroData:
                rotation = gyroData.rotationRate
                self.label_x.value = f"Rotación X: {rotation.x:.2f}rad/s"
                self.label_y.value = f"Rotación Y: {rotation.y:.2f}rad/s"
                self.label_z.value = f"Rotación Z: {rotation.z:.2f}rad/s"
            self.update()
            time.sleep(0.1)


def main(page: ft.Page):
    page.title = "Sensor iPhone 7+"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                [SensorVisualizer(), ft.Text(f"iOS: {os_version}")],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
    )


ft.app(target=main)
