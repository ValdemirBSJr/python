#https://flet.dev/docs/guides/python/user-controls/

import flet as ft

class Contador(ft.UserControl):
    def __init__(self, contador_inicial):
        super().__init__()
        self.counter = contador_inicial

    def build(self):
        text = ft.Text(str(self.counter))
        def add_click(e):
            self.counter += 1
            text.value = str(self.counter)
            self.update()

        return ft.Row([text, ft.ElevatedButton('Add', on_click=add_click)])

def main(page):
    page.add(
        Contador(100),
        Contador(200)
    )

ft.app(target=main)