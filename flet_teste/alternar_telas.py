import flet
from flet import AppBar, ElevatedButton, Page, Text, View, colors


def main(page: Page):
    page.title = "Exemplo de rotas"

    print("Rota Inicial:", page.route)

    def route_change(e):
        print("Mudança de rota:", e.route)
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Flet app")),
                    ElevatedButton("Vá para configurações", on_click=open_settings),
                ],
            )
        )
        if page.route == "/settings" or page.route == "/settings/mail":
            page.views.append(
                View(
                    "/settings",
                    [
                        AppBar(title=Text("Configurações"), bgcolor=colors.SURFACE_VARIANT),
                        Text("Configurações!!", style="bodyMedium"),
                        ElevatedButton(
                            "Vá para configurações de email", on_click=open_mail_settings
                        ),
                    ],
                )
            )
        if page.route == "/settings/mail":
            page.views.append(
                View(
                    "/settings/mail",
                    [
                        AppBar(
                            title=Text("Configurações de email"), bgcolor=colors.SURFACE_VARIANT
                        ),
                        Text("Configurações de email!"),
                        ElevatedButton(
                            "Voltar a tela inicial", on_click=open_root
                        ),
                    ],
                )
            )
        page.update()

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    def open_mail_settings(e):
        page.go("/settings/mail")

    def open_settings(e):
        page.go("/settings")

    def open_root(e):
        page.go("/")

    page.go(page.route)


flet.app(target=main, view=flet.WEB_BROWSER)