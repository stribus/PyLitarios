import tkinter as tk
import pyautogui
import time
import keyboard
import sys
import threading
from tkinter import messagebox





class App:
    def __init__(self, janela):
        
        self.janela = janela
        self.janela.title("Clicker")
        self.janela.geometry("250x150")
        self.janela.config(bg="#FFFFFF")

        quantidade_label = tk.Label(janela, text="Quantidade de Clicks:", bg="#FFFFFF")
        quantidade_label.pack()
        self.entrada = tk.Entry(janela)
        self.entrada.insert(0, "2")
        self.entrada.pack(pady=(0,10))

        self.intervalo_label = tk.Label(janela, text="Intervalo (ms):", bg="#FFFFFF")
        self.intervalo_label.pack()
        self.intervalo_entrada = tk.Entry(janela)
        self.intervalo_entrada.insert(0, "500")
        self.intervalo_entrada.pack(pady=(0,10))

        self.botao = tk.Button(janela, text="Iniciar", command=self.iniciar_cliques)
        self.botao.pack()
        
        self.janela.bind("<Escape>", lambda e: self.stop_clicks())

        
        

    def iniciar_cliques(self):
        try:            
            self.botao["state"] = "disabled"
            self.break_flag = False
            
            self.thread_esc = threading.Thread(target=self.monitorar_esc, daemon=True)
            self.thread_esc.start()
            
            if not self.entrada.get().isdigit() or not self.intervalo_entrada.get().isdigit():
                messagebox.showerror("Erro", "Por favor insira apenas valores numéricos.")
                return
            quantidade = int(self.entrada.get())
            intervalo = float(self.intervalo_entrada.get()) / 1000
            self.janela.withdraw()
            time.sleep(intervalo)  # Aguarda intervalo antes de começar
            for _ in range(quantidade):
                if self.break_flag:
                    break
                pyautogui.click()
                time.sleep(intervalo)  # Intervalo de acordo com a entrada
        finally:
            self.break_flag = True
            self.botao["state"] = "normal"
            self.janela.deiconify()
            
            

    def monitorar_esc(self):
        while True:
            if keyboard.is_pressed("esc"):
                self.stop_clicks()
                break
            if self.break_flag:
                break
            time.sleep(0.1)
        
    def stop_clicks(self):
        self.break_flag = True
        self.botao["state"] = "normal"
        self.janela.deiconify()


root = tk.Tk()
app = App(root)
root.mainloop()