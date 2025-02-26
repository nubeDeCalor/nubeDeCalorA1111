import flet as ft
from flet_assets import AssetsServer
from assets.widgets.MainNavigationBar import MainNavigationBar
from assets.widgets.TabContent import TabContent

server = AssetsServer("app/src/assets")


def build_page(page: ft.Page):
    page.title = "SkeletoR Diffusion"
    page.horizontal_alignment = "center"
    page.padding = 0


def main(page: ft.Page):
    build_page(page)
    tab_content = TabContent(server=server)
    page.navigation_bar = MainNavigationBar(tab_content)
    page.add(ft.SafeArea(ft.Container(content=tab_content, expand=True), expand=True))


ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir="assets")
