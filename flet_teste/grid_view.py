#para exibir muitos itens na tela, sempre devemos usar listview ou gridview senao fica lento
#GridViewpermite organizar controles em uma grade roláve

'''
Com a rolagem do GridView e o redimensionamento da janela são suaves e responsivos!
É possível especificar um número fixo de linhas ou colunas (executamentos)
com runs_count propriedade ou o tamanho máximo de um "telha" com max_extent propriedade,
então o número de execuções pode variar automaticamente. Em nosso exemplo,
definimos o tamanho máximo do bloco para 150 pixels e definimos sua forma como "quadrado"
com child_aspect_ratio=1. child_aspect_ratio é a razão entre o eixo transversal e a extensão
do eixo principal de cada criança. Tente mudá-lo para 0.5 ou 2.
'''

import flet as ft
import os

os.environ['FLET_WS_MAX_MESSAGE_SIZE'] = '8000000'

def main(page: ft.Page):
    
    gv = ft.GridView(expand=True, max_extent=150, child_aspect_ratio=1)
    page.add(gv)

    for i in range(500):
        gv.controls.append(
            ft.Container(
                ft.Text(f'Item: {i}'),
                width=100,
                height=100,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.AMBER_100,
                border=ft.border.all(1, ft.colors.AMBER_400),
                border_radius=ft.border_radius.all(5),
            )
        )

    page.update()

ft.app(target=main, view=ft.AppView.FLET_APP_WEB)
