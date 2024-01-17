#para exibir muitos itens na tela, sempre devemos usar listview ou gridview senao fica lento
import flet as ft

def main(page: ft.Page):
    lv = ft.ListView(expand=True, height=300, spacing=10)

    for i in range(500):
        lv.controls.append(ft.Text(f'Linha: {i}'))
    page.add(lv)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)