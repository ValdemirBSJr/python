import flet as ft
'''
Quando page.update() é chamado de uma mensagem que está sendo enviada para o servidor Flet 
através de WebSockets contendo atualizações de página desde o último page.update(). 
O envio de uma mensagem grande com milhares de controles adicionados pode fazer com que um 
usuário aguarde alguns segundos até que as mensagens sejam totalmente recebidas e os controles 
sejam renderizados.

Para aumentar a usabilidade do seu programa e apresentar os resultados a um usuário o mais 
rápido possível, você pode enviar atualizações de página em lotes. Por exemplo, o programa a 
seguir adiciona 5.100 controles filho a um ListView em lotes de 500 itens:
'''
def main(page: ft.Page):

    # add ListView to a page first
    lv = ft.ListView(expand=1, spacing=10, item_extent=50)
    page.add(lv)

    for i in range(5100):
        lv.controls.append(ft.Text(f"Line {i}"))
        # send page to a page
        if i % 500 == 0:
            page.update()
    # send the rest to a page
    page.update()

ft.app(target=main, view=ft.AppView.FLET_APP_WEB)