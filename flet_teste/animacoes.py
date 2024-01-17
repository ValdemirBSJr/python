import flet as ft
from math import pi

def main(page: ft.Page):

    def animate_opacity(e):
        c.opacity = 0 if c.opacity == 1 else 1
        c.update()

    def animate_rotate(e):
        r.rotate.angle += pi /2
        page.update()

    def animate_scale(e):
        es.scale = 2 if es.scale == 1 else 1
        page.update()

    def animate_offset(e):
        o.offset = ft.transform.Offset(0,0)
        o.update()

    def animate_container(e):
        c1.top = 20
        c1.left = 200
        c2.top = 100
        c2.left = 40
        c3.top = 180
        c3.left = 100
        page.update()

    #centraliza tudo na janela
    #page.vertical_alignment = ft.MainAxisAlignment.CENTER
    #page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    #page.spacing = 30


    c = ft.Container(
        width=100,
        height=100,
        bgcolor=ft.colors.BLUE_GREY_200,
        border_radius=10,
        animate_opacity=300,
        on_hover=animate_opacity
    )

    r = ft.Container(
       width=100,
        height=70,
        bgcolor=ft.colors.RED_800,
        border_radius=5,
        rotate=ft.transform.Rotate(0, alignment=ft.alignment.center),
        animate_rotation=ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT),
        on_hover=animate_rotate,
    )

    es = ft.Container(
        ft.Text('Clica ni mim!', color=ft.colors.BLACK38, text_align=ft.alignment.center),
        width=100,
        height=100,
        bgcolor=ft.colors.LIME_400,
        border_radius=7,
        scale=ft.transform.Scale(scale=1),
        animate_scale=ft.animation.Animation(600,ft.AnimationCurve.BOUNCE_OUT),
        alignment=ft.alignment.center,
        on_click=animate_scale,
    )

    o = ft.Container(
        width=100,
        height=100,
        bgcolor=ft.colors.GREEN_600,
        border_radius=10,
        offset=ft.transform.Offset(-4,0),
        animate_offset=ft.animation.Animation(1000),
    )

    c1 = ft.Container(width=50, height=50, bgcolor="red", animate_position=1000)

    c2 = ft.Container(
        width=50, height=50, bgcolor="green", top=60, left=0, animate_position=500
    )

    c3 = ft.Container(
        width=50, height=50, bgcolor="blue", top=120, left=0, animate_position=1000
    )
    btn_animar = ft.ElevatedButton('Animar!', on_click=animate_container)


    page.add(
        c,
        ft.ElevatedButton(
            'Animar opacidade',
            on_click=animate_opacity,
        ),
        r,
        es,
        o,
        ft.ElevatedButton('Mova-se!', on_click=animate_offset),
        ft.Stack([c1, c2, c3, btn_animar], height=250),
    )

ft.app(target=main)