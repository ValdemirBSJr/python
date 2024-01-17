import flet as ft

def main(page: ft.Page):
    def chkbox_changed(e):
        output_text.value = (
            f'Você aprendeu a: {todo_check}.'
        )
        page.update()

    output_text = ft.Text()
    todo_check = ft.Checkbox(label='Todo: Aprender a usar', value=False, on_change=chkbox_changed)
    page.add(todo_check, output_text)

ft.app(target=main)