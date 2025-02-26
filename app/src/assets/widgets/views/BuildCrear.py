import flet as ft
import time
from .components.SliderWidget import SliderWidget


class BuildCrear(ft.Container):
    def did_mount(self):
        if self.page.platform == ft.PagePlatform.IOS:
            suffix = ft.IconButton(
                ft.Icons.CLOSE,
                on_click=self.close_keyboard,
                padding=2,
                # size_constraints=15,
                icon_size=22,
                width=25,
                height=25,
                alignment=ft.alignment.center,
            )
            self.input_prompt.suffix = suffix
            self.input_nprompt.suffix = suffix
        self.update()
        return super().did_mount()

    def close_keyboard(self, e):
        self.columna_inputs.disabled = True
        self.columna_inputs.update()
        time.sleep(0.01)
        self.columna_inputs.disabled = False
        self.columna_inputs.update()

    def __init__(self):
        super().__init__()
        self.input_prompt = ft.TextField(
            hint_text="Prompt",
            multiline=True,
            data="prompt",
            height=50,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            content_padding=10,
        )
        self.input_nprompt = ft.TextField(
            hint_text="Negative Prompt",
            multiline=True,
            data="nprompt",
            content_padding=5,
            height=50,
            text_vertical_align=ft.VerticalAlignment.CENTER,
        )
        self.slider_steps = SliderWidget("Steps", min=1, max=50, divisions=49)
        self.slider_cfg_scale = SliderWidget(
            "CFG Scale", double=True, min=1, max=15, divisions=140
        )
        self.row_sliders_steps_and_cfg = ft.Row(
            [self.slider_steps, self.slider_cfg_scale],
            alignment=ft.alignment.center,
        )
        self.columna_inputs = ft.Column(
            [
                self.input_prompt,
                self.input_nprompt,
                self.row_sliders_steps_and_cfg,
            ]
        )
        self.columna_main = ft.Column([self.columna_inputs], expand=True, scroll="auto")
        self.expand = True
        self.content = self.columna_main
