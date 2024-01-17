import flet as ft

def main(page):


    def add_clicar(e):
        page.add(ft.Checkbox(label=nova_tarefa.value))
        nova_tarefa.value = ''
        nova_tarefa.focus()
        nova_tarefa.update()

    nova_tarefa = ft.TextField(hint_text='O que você precisa que seja feito?', width=400)
    page.add(ft.Row([nova_tarefa, ft.ElevatedButton('Adicionar', on_click=add_clicar)]))

ft.app(target=main)