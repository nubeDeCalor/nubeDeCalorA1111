import flet as ft


class MainNavigationBar(ft.NavigationBar):
    def __init__(self, tab_content):
        super().__init__()
        self.tab_content = tab_content
        self.destinations = [
            ft.NavigationBarDestination(
                label="Crear",
                icon=ft.Icons.PALETTE,
                selected_icon=ft.Icons.PALETTE_OUTLINED,
            ),
            ft.NavigationBarDestination(
                label="Galería",
                icon=ft.Icons.PHOTO_ALBUM,
                selected_icon=ft.Icons.PHOTO_ALBUM_OUTLINED,
            ),
            ft.NavigationBarDestination(
                label="Configuración",
                icon=ft.Icons.SETTINGS,
                selected_icon=ft.Icons.SETTINGS_OUTLINED,
            ),
        ]
        self.on_change = self.handle_tab_change

    def handle_tab_change(self, e):
        new_index = e.control.selected_index
        self.tab_content.change_to(new_index)
        self.page.update()
