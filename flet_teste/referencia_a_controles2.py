#Aqui podemos fazer referencias como nodejs
import flet as ft

def main(page):
    nome = ft.Ref[ft.TextField]()
    ultimo_nome = ft.Ref[ft.TextField]()
    bem_vindo = ft.Ref[ft.Column]()

    def btn_click(e):
        bem_vindo.current.controls.append(
            ft.Text(f'Olá, {nome.current.value} {ultimo_nome.current.value}!')
        )
        nome.current.value = ''
        ultimo_nome.current.value = ''
        page.update()
        nome.current.focus()

    page.add(
        ft.TextField(ref=nome, label='Primeiro nome', autofocus=True),
        ft.TextField(ref=ultimo_nome, label='Ultimo nome'),
        ft.ElevatedButton('Diga Olá!', on_click=btn_click),
        ft.Column(ref=bem_vindo)
    )

ft.app(target=main)