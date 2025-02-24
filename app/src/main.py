import flet as ft
import threading
import time
from pyobjus import autoclass
from pyobjus.dylib_manager import load_framework, INCLUDE

load_framework(INCLUDE.Foundation)

NSProcessInfo = autoclass("NSProcessInfo")
process_info = NSProcessInfo.processInfo()
os_version = process_info.operatingSystemVersionString.UTF8String()


class SensorVisualizer(ft.Container):
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.motion_manager = None
        self.update_thread = None

        # UI Elements
        self.labels = {
            "accel": [
                ft.Text("Aceleración X: --"),
                ft.Text("Aceleración Y: --"),
                ft.Text("Aceleración Z: --"),
            ],
            "gyro": [
                ft.Text("Rotación X: --"),
                ft.Text("Rotación Y: --"),
                ft.Text("Rotación Z: --"),
            ],
            "device_motion": [
                ft.Text("Aceleración User X: --"),
                ft.Text("Aceleración User Y: --"),
                ft.Text("Aceleración User Z: --"),
                ft.Text("Gravedad X: --"),
                ft.Text("Gravedad Y: --"),
                ft.Text("Gravedad Z: --"),
            ],
        }

        self.sensor_status = ft.Text("Estado: Detenido")
        self.sensor_type = ft.Text("Sensor: --")
        self.start_button = ft.ElevatedButton("Iniciar", on_click=self.toggle_sensor)

        self.content = ft.Column(
            controls=[
                self.sensor_status,
                self.sensor_type,
                *self.labels["accel"],
                *self.labels["gyro"],
                *self.labels["device_motion"],
                self.start_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    def toggle_sensor(self, event):
        if not self.is_running:
            self.start_sensor()
        else:
            self.stop_sensor()
        self.update()

    def start_sensor(self):
        try:
            self.motion_manager = autoclass("CMMotionManager").alloc().init()

            # Prioridad de sensores: Device Motion > Acelerómetro > Giroscopio
            if self.motion_manager.isDeviceMotionAvailable():
                self.setup_device_motion()
            elif self.motion_manager.isAccelerometerAvailable():
                self.setup_accelerometer()
            elif self.motion_manager.isGyroAvailable():
                self.setup_gyro()
            else:
                self.show_error("No hay sensores disponibles")
                return

            self.is_running = True
            self.start_button.text = "Detener"
            self.sensor_status.value = "Estado: Activado"

            self.update_thread = threading.Thread(
                target=self.update_sensor_data, daemon=True
            )
            self.update_thread.start()

        except Exception as e:
            self.show_error(f"Error: {str(e)}")

    def setup_device_motion(self):
        self.motion_manager.deviceMotionUpdateInterval = 0.1
        self.motion_manager.startDeviceMotionUpdates()
        self.sensor_type.value = "Sensor: Device Motion (Fusionado)"
        self.hide_labels(["gyro", "accel"])

    def setup_accelerometer(self):
        self.motion_manager.accelerometerUpdateInterval = 0.1
        self.motion_manager.startAccelerometerUpdates()
        self.sensor_type.value = "Sensor: Acelerómetro"
        self.hide_labels(["gyro", "device_motion"])

    def setup_gyro(self):
        self.motion_manager.gyroUpdateInterval = 0.1
        self.motion_manager.startGyroUpdates()
        self.sensor_type.value = "Sensor: Giroscopio"
        self.hide_labels(["accel", "device_motion"])

    def hide_labels(self, types_to_hide):
        for sensor_type in types_to_hide:
            for label in self.labels[sensor_type]:
                label.visible = False

    def update_sensor_data(self):
        while self.is_running and self.motion_manager:
            try:
                if self.motion_manager.isDeviceMotionActive():
                    self.process_device_motion()
                elif self.motion_manager.isAccelerometerActive():
                    self.process_accelerometer()
                elif self.motion_manager.isGyroActive():
                    self.process_gyro()

                self.update()
                time.sleep(0.1)
            except Exception as e:
                self.show_error(f"Error en hilo: {str(e)}")
                break

    def process_device_motion(self):
        motion_data = self.motion_manager.deviceMotion
        if motion_data:
            # Aceleración del usuario (sin gravedad)
            user_accel = motion_data.userAcceleration
            self.labels["device_motion"][0].value = f"Acel User X: {user_accel.x:.2f}g"
            self.labels["device_motion"][1].value = f"Acel User Y: {user_accel.y:.2f}g"
            self.labels["device_motion"][2].value = f"Acel User Z: {user_accel.z:.2f}g"

            # Vector de gravedad
            gravity = motion_data.gravity
            self.labels["device_motion"][3].value = f"Gravedad X: {gravity.x:.2f}g"
            self.labels["device_motion"][4].value = f"Gravedad Y: {gravity.y:.2f}g"
            self.labels["device_motion"][5].value = f"Gravedad Z: {gravity.z:.2f}g"

    def process_accelerometer(self):
        accel_data = self.motion_manager.accelerometerData
        if accel_data:
            accel = accel_data.acceleration
            self.labels["accel"][0].value = f"Acel X: {accel.x:.2f}g"
            self.labels["accel"][1].value = f"Acel Y: {accel.y:.2f}g"
            self.labels["accel"][2].value = f"Acel Z: {accel.z:.2f}g"

    def process_gyro(self):
        gyro_data = self.motion_manager.gyroData
        if gyro_data:
            rot = gyro_data.rotationRate
            self.labels["gyro"][0].value = f"Rot X: {rot.x:.2f}rad/s"
            self.labels["gyro"][1].value = f"Rot Y: {rot.y:.2f}rad/s"
            self.labels["gyro"][2].value = f"Rot Z: {rot.z:.2f}rad/s"

    def stop_sensor(self):
        self.is_running = False
        if self.motion_manager:
            self.motion_manager.stopDeviceMotionUpdates()
            self.motion_manager.stopAccelerometerUpdates()
            self.motion_manager.stopGyroUpdates()
        self.start_button.text = "Iniciar"
        self.sensor_status.value = "Estado: Detenido"
        self.sensor_type.value = "Sensor: --"

    def show_error(self, message):
        self.sensor_status.value = message
        self.is_running = False
        self.start_button.text = "Iniciar"
        self.update()


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
