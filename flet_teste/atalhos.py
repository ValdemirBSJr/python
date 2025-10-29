import flet as ft

def main(page: ft.Page):
    def on_keyboard(e: ft.KeyboardType):
        page.add(
            ft.Text(f'Chave: {e.key}, shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}')
        )

    page.on_keyboard_event = on_keyboard
    page.add(
        ft.Text('Pressione qualquer tecla com a combinação de CTRL, ALT, SHIFT e META')
    )

ft.app(target=main)