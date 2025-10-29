import flet as ft

def main(page):

    nome = ft.TextField(label='Primeiro nome', autofocus=True)
    ultimo_nome = ft.TextField(label='Último nome')
    bem_vindo = ft.Column()

    def btn_click(e):
        bem_vindo.controls.append(ft.Text(f'Olá, {nome.value} {ultimo_nome.value}!'))
        nome.value = ''
        ultimo_nome.value = ''
        page.update()
        nome.focus()

    page.add(
        nome,
        ultimo_nome,
        ft.ElevatedButton('Diga olá!', on_click=btn_click),
        bem_vindo,
    )

ft.app(target=main)