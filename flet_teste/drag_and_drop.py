import flet as ft

def main(page: ft.Page):
    page.title = 'Exemplo Drag and Drop'

    def drag_accept(e):
        #pega a origem do controle dragavel pelo ID
        src = page.get_control(e.src_id)
        #atualiza texto dentro do dragavel
        src.content.content.value = '0'
        #reseta o source group, isso e pra que ele nao possa mais ser dragavel
        src.group = ''
        #atualizar o texto do drag
        e.control.content.content.value = '1'
        #reseta borda
        e.control.content.border = None
        page.update()

    def drag_will_accept(e):
        #borda preta quando é permitido e vermelha quando nao
        e.control.content.border = ft.border.all(
            2, ft.colors.BLACK45 if e.data == 'true' else ft.colors.RED
        )
        e.control.update()

    def drag_leave(e):
        e.control.content.border = None
        e.control.update()

    page.add(
        ft.Row(
            [
                ft.Draggable(
                    group='number',
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.CYAN_200,
                        border_radius=5,
                        content=ft.Text('1', size=20),
                        alignment=ft.alignment.center,
                    ),
                    content_when_dragging=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.BLUE_GREY_200,
                        border_radius=5,
                    ),
                    content_feedback=ft.Text('1'),
                ),
                ft.Container(width=100),
                ft.DragTarget(
                    group='number',
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.PINK_200,
                        border_radius=5,
                        content=ft.Text('0', size=20),
                        alignment=ft.alignment.center,
                    ),
                    on_accept=drag_accept,
                    on_will_accept=drag_will_accept,
                    on_leave=drag_leave,
                ),
            ]
        )
    )

ft.app(target=main)