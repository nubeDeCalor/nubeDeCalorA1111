import flet as ft


class GalleryImageWidget(ft.Container):
    def build(self):
        self.pic = ft.Image(
            src=self.image_src,
            fit=ft.ImageFit.COVER,
            expand=True,
            filter_quality=ft.FilterQuality.LOW,
        )
        self.hq_pic = ft.Image(
            src=self.image_src,
            fit=ft.ImageFit.COVER,
            expand=True,
            filter_quality=ft.FilterQuality.HIGH,
        )
        self.content = self.pic

    def did_mount(self):
        return super().did_mount()

    def click(self, e):
        self.ad = ft.AlertDialog(
            content=ft.InteractiveViewer(content=self.hq_pic, max_scale=4, min_scale=1),
            bgcolor=ft.Colors.BLACK12,
            inset_padding=0,
            actions=[
                ft.Button("HiRes Fix"),
                ft.Button(
                    "Img2Img",
                ),
            ],
        )
        self.page.open(self.ad)

    def __init__(self, image_src):
        super().__init__()
        self.image_src = image_src
        self.build()
        self.on_click = self.click
