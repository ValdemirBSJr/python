import flet as ft

def main(page: ft.Page):
    nome_invisivel = ft.TextField()
    outro_campo_invisivel = ft.TextField()
    nome_invisivel.visible = False
    outro_campo_invisivel.visible = False

    primeiro_nome = ft.TextField()
    segundo_nome = ft.TextField()
    primeiro_nome.disabled = True
    segundo_nome.disabled =  True

    page.add(nome_invisivel, outro_campo_invisivel, primeiro_nome, segundo_nome)

    #ou coloca num container e desabilita tudo
    campo = ft.TextField()
    outro_campo = ft.TextField()

    c = ft.Column(
        controls=[
            campo,
            outro_campo
        ]
    )

    c.disabled = True
    page.add(c)

ft.app(target=main)