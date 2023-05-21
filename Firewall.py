import os
import tkinter as tk
import tkinter.messagebox as messagebox

# Função que abre a porta selecionada
def open_port(port):
    os.system(f'netsh advfirewall firewall add rule name="Open Port {port} UDP" dir=in action=allow protocol=UDP localport={port}')
    os.system(f'netsh advfirewall firewall add rule name="Open Port {port} UDP" dir=out action=allow protocol=UDP localport={port}')
    os.system(f'netsh advfirewall firewall add rule name="Open Port {port} TCP" dir=in action=allow protocol=TCP localport={port}')
    os.system(f'netsh advfirewall firewall add rule name="Open Port {port} TCP" dir=out action=allow protocol=TCP localport={port}')

# Função que verifica se uma porta está aberta no firewall
def check_port(port):
    result = os.system(f'netsh advfirewall firewall show rule name="Open Port {port} UDP" >nul')
    if result == 0:
        return "aberta"
    else:
        result = os.system(f'netsh advfirewall firewall show rule name="Open Port {port} TCP" >nul')
        if result == 0:
            return "aberta"
        else:
            return "fechada"

# Função que é chamada quando o botão é pressionado
def button_click():
    port = port_entry.get()
    if port.isdigit():
        if option.get() == 1:
            open_port(port)
            port_label.config(text="Porta aberta com sucesso.", fg="green")
        elif option.get() == 2:
            status = check_port(port)
            if status == "aberta":
                port_label.config(text=f"A porta está {status}.", fg="blue")
            else:
                show_error_messagebox(port)
    else:
        # Caso o usuário não tenha digitado um número no campo de porta
        port_label.config(text="Digite apenas números.", fg="red")

# Função que exibe uma messagebox de erro
def show_error_messagebox(port):
    messagebox.showerror("Erro", f"A porta {port} não está aberta.")

    # Função que desfaz as regras do firewall criadas pelo programa
def undo_open_ports():
    os.system('netsh advfirewall firewall delete rule name="Open Port UDP"')
    os.system('netsh advfirewall firewall delete rule name="Open Port TCP"')


# Cria a janela principal
root = tk.Tk()
root.title("Abrir Porta no Firewall")
root.geometry("650x650")
root.configure(bg="black")

# Cria os widgets
header = tk.Label(root, text="", bg="black", fg="white", font=("Arial", 16, "italic", "bold"))
option = tk.IntVar()
option.set(1)
open_button = tk.Radiobutton(root, text="Abrir Porta", value=1, variable=option, command=lambda: header.config(text="Qual porta deseja abrir"))
check_button = tk.Radiobutton(root, text="Verificar Porta", value=2, variable=option, command=lambda: header.config(text="Qual porta você quer verificar"))
port_entry = tk.Entry(root, width=10, bg="black", fg="white")
button = tk.Button(root, text="Executar", command=button_click, bg="black", fg="white", relief=tk.RAISED, bd=2)
port_label = tk.Label(root, text="", bg="black", fg="white", font=("Arial", 14, "italic"))
undo_button = tk.Button(root, text="Desfazer", command=undo_open_ports, bg="black", fg="white", relief=tk.RAISED, bd=2)

# Posiciona os widgets na janela principal
undo_button.pack(side=tk.LEFT, padx=10, pady=10)
header.pack(side=tk.LEFT, padx=10, pady=10)
open_button.pack(side=tk.LEFT, padx=8, pady=8)
check_button.pack(side=tk.LEFT, padx=7, pady=7)
port_entry.pack(side=tk.LEFT, padx=6, pady=6)
button.pack(side=tk.LEFT, padx=5, pady=5)
port_label.pack(side=tk.LEFT, padx=4, pady=4)

# Inicia o loop principal da aplicação
root.mainloop()
