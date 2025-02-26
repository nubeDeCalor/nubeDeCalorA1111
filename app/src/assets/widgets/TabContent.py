import flet as ft
from .views.BuildCrear import BuildCrear
from .views.BuildGaleria import BuildGaleria


class TabContent(ft.Stack):
    def did_mount(self):
        if self.page.client_storage.get("selected_tab") is not None:
            self.change_to(self.page.client_storage.get("selected_tab"))
        return super().did_mount()

    def __init__(self, index: int = None, server=None):
        super().__init__()
        if not index:
            index = 0
        self.spacing = 0
        self.expand = True
        self.server = server
        self.alignment = ft.alignment.top_center
        # Títulos para cada pestaña
        self.titles = [
            ft.Text("Crear", size=20, weight="bold"),
            ft.Text("Galería", size=20, weight="bold"),
            ft.Text("Configuración", size=20, weight="bold"),
        ]

        # Contenedor del título
        self.title_container = ft.Container(
            content=self.titles[index], alignment=ft.alignment.top_center
        )

        # Contenido de las pestañas
        self.tabs = ft.Tabs(
            selected_index=index,
            tabs=[
                ft.Tab(content=BuildCrear()),
                ft.Tab(content=BuildGaleria(server=server)),
                ft.Tab(content=ft.Text("Contenido de Configuración")),
            ],
            expand=True,
        )

        self.controls = [self.title_container, self.tabs]

    def change_to(self, index):
        self.tabs.selected_index = index
        self.title_container.content = self.titles[index]
        self.page.navigation_bar.selected_index = index
        # self.update()
        self.page.update()
        self.page.client_storage.set("selected_tab", index)
