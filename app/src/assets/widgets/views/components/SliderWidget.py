import flet as ft


class SliderWidget(ft.Container):
    def update_label(self, e):
        try:
            value = float(e.control.value) if self.double else int(e.control.value)
        except ValueError:
            value = self.slider.min  # Si no es un número válido, asignar el mínimo

        value = max(
            self.slider.min, min(value, self.slider.max)
        )  # Asegurar dentro del rango
        self.slider.value = value

        formatted_value = round(value, 1) if self.double else int(value)
        self.slider.label = f"{self.title}: {formatted_value}"
        self.text_slider.value = f"{self.title}: {formatted_value}"
        self.input_slider.value = str(formatted_value)

        self.update()

    def __init__(self, title, double=False, min=1, max=15, divisions=14):
        super().__init__()
        self.title = title
        self.double = double
        self.expand = True

        self.slider = ft.Slider(
            min=min,
            max=max,
            value=min,  # Valor inicial en el mínimo para evitar problemas
            divisions=divisions,
            label=f"{title}: {min}",
            expand=True,
            on_change=self.update_label,
        )

        formatted_value = (
            round(self.slider.value, 1) if double else int(self.slider.value)
        )

        self.text_slider = ft.Text(f"{self.title}: {formatted_value}", expand=True)

        self.input_slider = ft.TextField(
            value=str(formatted_value),
            on_change=self.update_label,
            width=60,
            content_padding=5,
            height=50,
            data="tf",
            input_filter=ft.InputFilter(regex_string=r"^\d*\.?\d{0,1}$", allow=True)
            if double
            else ft.NumbersOnlyInputFilter(),
            text_vertical_align=ft.VerticalAlignment.CENTER,
            text_align=ft.TextAlign.END,
        )

        self.content = ft.Column(
            [
                ft.Row(
                    [self.text_slider, self.input_slider],
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                self.slider,
            ],
            spacing=5,
        )
