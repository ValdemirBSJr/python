import flet as ft


def main(page: ft.Page):
    def button_clicked(e):
        output_text.value = f"Valor do dropdown é:  {color_dropdown.value}"
        page.update()

    output_text = ft.Text()
    color_dropdown = ft.Dropdown(
        width=300,
        on_change=button_clicked,
        options=[
            ft.dropdown.Option("Vermelho"),
            ft.dropdown.Option("Verde"),
            ft.dropdown.Option("Azul"),
        ],
    )
    page.add(color_dropdown, output_text)

ft.app(target=main)