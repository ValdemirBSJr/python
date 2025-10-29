import flet as ft
import time
'''
Web Armazenamento local.
Desktop - arquivo JSON.
iOS - NSUserDefaults.
Android - SharedPreferências.
'''

def main(page: ft.Page):
    #page.client_storage.set('numero.config', 12345)
    #page.client_storage.set('valor_BOOL', True)
    #page.client_storage.set('cores', ['azul', 'verde', 'amarelo'])

    num = page.client_storage.get('numero.config')
    print(num)
    print(page.client_storage.get('valor_BOOL'))

    cores = page.client_storage.get('cores')
    for cor in cores:
        print(cor)

    page.add(
        ft.Text(num),
        ft.Text(page.client_storage.get('valor_BOOL')),
        ft.Text('Agora um forzão:', color=ft.colors.RED, weight='bold',  tooltip='Olha o contador la embaixo')
    )

    for cor in cores:
        page.controls.append(ft.Text(cor))
        page.update()
        time.sleep(0.5)

    #apaga tudo armazenado do lado do cliente
    #page.client_storage.clear()

ft.app(target=main)