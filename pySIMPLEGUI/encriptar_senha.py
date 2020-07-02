import PySimpleGUI as sg
import hashlib

'''      
Crie um login seguro para seus scripts sem precisar incluir sua senha no programa. 
Crie um código de hash SHA1 para sua senha usando a GUI. 
Cole na variável no programa final 
1. Escolha uma senha 
2. Gere um código de hash para a senha escolhida executando o programa e digitando 'gui' como a senha 
3. Digite a senha na GUI 
4. Copie e cole o código de hash da janela GUI na variável chamado login_password_hash 
5. Execute o programa novamente e teste seu login!    
'''


# Use this GUI to get your password's hash code
def HashGeneratorGUI():
    layout = [[sg.T('Password Hash Generator', size=(30, 1), font='Any 15')],
              [sg.T('Password'), sg.In(key='password')],
              [sg.T('SHA Hash'), sg.In('', size=(40, 1), key='hash')],
              ]

    window = sg.Window('SHA Generator', layout, auto_size_text=False, default_element_size=(10, 1),
                       text_justification='r', return_keyboard_events=True, grab_anywhere=False)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit(69)

        password = values['password']
        try:
            password_utf = password.encode('utf-8')
            sha1hash = hashlib.sha1()
            sha1hash.update(password_utf)
            password_hash = sha1hash.hexdigest()
            window['hash'].update(password_hash)
        except:
            pass

        # ----------------------------- Paste this code into your program / script -----------------------------


# determine if a password matches the secret password by comparing SHA1 hash codes
def PasswordMatches(password, hash):
    password_utf = password.encode('utf-8')
    sha1hash = hashlib.sha1()
    sha1hash.update(password_utf)
    password_hash = sha1hash.hexdigest()
    if password_hash == hash:
        return True
    else:
        return False


login_password_hash = '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8'
password = sg.popup_get_text('Password', password_char='*')
if password == 'senha':  # Remove when pasting into your program
    HashGeneratorGUI()  # Remove when pasting into your program
    exit(69)  # Remove when pasting into your program
if PasswordMatches(password, login_password_hash):
    print('Login SUCCESSFUL')
else:
    print('Login FAILED!!')