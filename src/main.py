from gui import Application
import customtkinter as tk

def main():
    janela = tk.CTk()
    janela.title("Renomeia Lote BRC v4.3")  # Define o título da janela
    janela.geometry("850x740")
    app=Application(master=janela)
    janela.mainloop()  # Inicia a GUI

if __name__ == "__main__":
    main()


