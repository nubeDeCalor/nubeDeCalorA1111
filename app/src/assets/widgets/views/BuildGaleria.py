import flet as ft
from .components.GalleryImageWidget import GalleryImageWidget
import os

real_gallery = "C:/Users/Julian/Desktop/trestp/app/src/assets/gallery"


class BuildGaleria(ft.Container):
    def did_mount(self):
        # self.img.src = self.server.assets
        # self.update()
        return super().did_mount()

    def __init__(self, server):
        super().__init__()
        self.server = server
        imgs = []
        # gallery is on C:\Users\Julian\Desktop\trestp\app\src\assets\gallery
        for root, dirs, files in os.walk(real_gallery):
            for file in files:
                # compress_image(
                #     f"{real_gallery}/{file}",
                #     f"{real_gallery}/comp/{file}",
                #     quality=80,
                # )
                imgs.append(
                    GalleryImageWidget(image_src=f"{self.server.assets}/gallery/{file}")
                )
                print(f"{self.server.assets}/gallery/{file}")
        self.columna_main = ft.GridView(
            [*imgs, *imgs, *imgs],
            expand=True,  # Expande el GridView para ocupar todo el espacio disponible
            runs_count=2,  # Muestra 2 imágenes por fila en dispositivos móviles
            max_extent=150,  # Tamaño máximo de cada imagen
            child_aspect_ratio=1.0,  # Relación de aspecto 1:1 (cuadrada)
            spacing=5,  # Espacio entre imágenes en el eje principal
            run_spacing=5,  # Espacio entre filas
            auto_scroll=True,  # Permite el desplazamiento automático
            cache_extent=200,  # Cache para mejorar el rendimiento al desplazar
            clip_behavior=ft.ClipBehavior.NONE,  # No recortar el contenido,
        )
        self.expand = True
        self.content = self.columna_main
