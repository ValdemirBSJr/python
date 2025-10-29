import flet as ft
import time


def main(page: ft.Page):

    def animate_container(e):
        c.width = 100 if c.width == 150 else 150
        c.height = 50 if c.height == 150 else 150
        c.bgcolor = 'blue' if c.bgcolor == 'red' else 'red'
        btn.color = 'blue' if btn.color == 'red' else 'red'
        c.update()
        btn.update()

    def animate_img(e):
        sw.content = ft.Image(src=f'https://picsum.photos/150/150?{time.time()}', width=150, height=150)
        page.update()


    btn = ft.ElevatedButton('Animar o container', color=ft.colors.RED, on_click=animate_container)

    c = ft.Container(
        width=150,
        height=150,
        bgcolor=ft.colors.RED,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
        on_animation_end=lambda e: print(f'Fim da animação desse container {e.data}')
    )

    i = ft.Image(src='https://picsum.photos/150/150', width=150, height=150)
    sw = ft.AnimatedSwitcher(i, transition=ft.AnimatedSwitcherTransition.SCALE,
                             duration=500,
                             reverse_duration=500,
                             switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
                             switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
                             )



    page.add(

        c,
        btn,
        sw,
        ft.ElevatedButton('Animar img!', on_click=animate_img)

    )

ft.app(target=main)
