import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)
#Ao executar o aplicativo Flet em um navegador, apenas a opção "Pick files" está disponível e é usada apenas para uploads
#https://flet.dev/docs/guides/python/file-picker-and-uploads/

def main(page: Page):
    # Selecione os dialogos
    def pick_files_result(e: FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelado!"
        )
        selected_files.update()
        print(f'Arquivos selecionados: {e.files}')
        print(f'Arquivos ou diretorios selecionados: {e.path}')

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()

    # Dialogo salvar arquivos
    def save_file_result(e: FilePickerResultEvent):
        save_file_path.value = e.path if e.path else "Cancelado!"
        save_file_path.update()

        print(f'Arquivos selecionados: {e.files}')
        print(f'Arquivos ou diretorios selecionados: {e.path}')
        #criar o arquivo
        #open(e.path, 'w')

    save_file_dialog = FilePicker(on_result=save_file_result)
    save_file_path = Text()

    # Abrir dialogo diretorio
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelado!"
        directory_path.update()

        print(f'Arquivos selecionados: {e.files}')
        print(f'Arquivos ou diretorios selecionados: {e.path}')

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()

    # ocultar todas as caixas de diálogo em sobreposição
    page.overlay.extend([pick_files_dialog, save_file_dialog, get_directory_dialog])

    page.add(
        Row(
            [
                ElevatedButton(
                    "Selecionar arquivos",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ),
                selected_files,
            ]
        ),
        Row(
            [
                ElevatedButton(
                    "Salvar arquivo",
                    icon=icons.SAVE,
                    on_click=lambda _: save_file_dialog.save_file(),
                    disabled=page.web,
                ),
                save_file_path,
            ]
        ),
        Row(
            [
                ElevatedButton(
                    "Abrir diretório",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: get_directory_dialog.get_directory_path(),
                    disabled=page.web,
                ),
                directory_path,
            ]
        ),
    )


flet.app(target=main)

