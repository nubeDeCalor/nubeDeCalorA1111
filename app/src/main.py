import flet as ft
import threading
import time
from pyobjus import autoclass
from pyobjus.dylib_manager import load_framework, INCLUDE

load_framework(INCLUDE.Foundation)

NSProcessInfo = autoclass("NSProcessInfo")
process_info = NSProcessInfo.processInfo()
os_version = process_info.operatingSystemVersionString.UTF8String()
processor_count = f"{process_info.activeProcessorCount}/{process_info.processorCount}"
physical_memory = f"{process_info.physicalMemory}"
isLowPowerModeEnabled = process_info.isLowPowerModeEnabled

try:
    print(
        f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(process_info.systemUptime))}"
    )
except Exception as e:
    print(e)


def main(page: ft.Page):
    page.title = "Data Visualization"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                [
                    ft.Text(f"iOS: {os_version}"),
                    ft.Text(f"CPU: {processor_count}"),
                    ft.Text(f"Memory: {physical_memory}"),
                    ft.Text(f"Low Power Mode: {isLowPowerModeEnabled}"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                scroll="auto",
            ),
        )
    )


ft.app(target=main)
