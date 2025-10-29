#https://flet.dev/docs/guides/python/user-controls/

import flet as ft

class Contador(ft.UserControl):
    def build(self):
        self.counter = 0
        text = ft.Text(str(self.counter))

        def add_click(e):
            self.counter += 1
            text.value = str(self.counter)
            self.update()

        return ft.Row([text, ft.ElevatedButton("Add", on_click=add_click)])

def main(page):
    page.add(Contador(), Contador())

ft.app(target=main)