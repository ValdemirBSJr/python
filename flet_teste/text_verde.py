import time
import flet as ft

def inicio(page: ft.Page):

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 600
    page.window_height = 400


    t = ft.Text(value="Olá mundo!", color='green', bgcolor='red')
    page.controls.append(t)
    page.update()

    iterado = ft.Text(size='20', font_family='Arial', weight='bold', tooltip='AQUI TEM ITERAÇÃO!!!!')
    #pode inserir com o add
    page.add(iterado)

    for i in range(3):
        iterado.value = f'Passo {i}'
        page.update()
        time.sleep(1)

    #Da pra fazer como containers ou divs onde colocar linhas e colunas
    page.add(
        ft.Row(controls=[
            ft.Text('A'),
            ft.Text('B'),
            ft.Text('C')
        ]),
        ft.Column(controls=[
            ft.Text('1'),
            ft.Text('2'),
            ft.Text('3')
        ]),
    )


#Assim que vc pode fazer interação entre um txt e botão
    def escreve_meu_nome(e):
        botao_nome.text = f'Seu nome é: {meu_nome.value}'
        page.update()

    botao_nome = ft.ElevatedButton(text='Diga meu nome!', on_click=escreve_meu_nome)
    meu_nome = ft.TextField(label="Seu nome aqui...")

    page.add(
        ft.Row(controls=[
            meu_nome,
            botao_nome,
        ])
    )

    for i in range(10):
        page.controls.append(ft.Text(f"Linha {i}"))
        if i > 4:
            page.controls.pop(0)
        page.update()
        time.sleep(0.3)

ft.app(target=inicio)