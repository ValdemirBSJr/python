import flet as ft

def main(page: ft.Page):

    #caracteristicas da janela
    page.title = 'Exemplo de contador em flet'
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 400
    page.window_resizable = False

    #cria o campo que vai conter o valor
    txt_numero = ft.TextField(value='0', text_align=ft.TextAlign.RIGHT, width=100)

    #funcoes que fazem os calculos
    def menos_click(e):
        txt_numero.value = str(int(txt_numero.value) - 1)
        page.update()

    def mais_click(e):
        txt_numero.value = str(int(txt_numero.value) + 1)
        page.update()

    #monta a pagina
    page.add(

        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=menos_click),
                txt_numero,
                ft.IconButton(ft.icons.ADD, on_click=mais_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

#passa a funcao main pa ser inicializada
ft.app(target=main)