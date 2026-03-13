"""
anti_idle.py

Impeça que o computador local entre em espera e evite desconexão por ociosidade em sessões RDP (mstsc).
Interface gráfica para ativar/desativar facilmente.

Requisitos: pyautogui, tkinter
"""
import tkinter as tk
from tkinter import messagebox
import threading
import time
import pyautogui
import ctypes

class AntiIdle:
    def __init__(self):
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            try:
                # Simula movimento mínimo do mouse (local e RDP)
                print("🔄 Simulando movimento do mouse...")
                x, y = pyautogui.position()
                pyautogui.move(50, 0, duration=0.1)
                pyautogui.move(-50, 0, duration=0.1)
                # Impede suspensão local (Windows)
                try:
                    ES_CONTINUOUS = 0x80000000
                    ES_SYSTEM_REQUIRED = 0x00000001
                    ES_DISPLAY_REQUIRED = 0x00000002
                    ctypes.windll.kernel32.SetThreadExecutionState(
                        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
                    )
                except Exception:
                    print("⚠️ Aviso: Falha ao impedir suspensão do sistema.")
                print("💤 Aguardando próximo ciclo...")
                time.sleep(50)  # repete a cada 50 segundos
            except Exception as e:
                # Não interrompe o loop em caso de erro
                print(f"⚠️ Aviso: Ocorreu um erro no loop anti-ociosidade: {e}")
                time.sleep(5)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Anti-Ociosidade (Local + RDP)")
        self.anti_idle = AntiIdle()
        self.status_var = tk.StringVar(value="Desativado ❌")
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack()
        self.status_label = tk.Label(frame, textvariable=self.status_var, font=("Segoe UI", 14))
        self.status_label.pack(pady=(0, 10))
        self.toggle_btn = tk.Button(frame, text="Ativar", width=15, command=self.toggle)
        self.toggle_btn.pack(pady=5)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle(self):
        if self.anti_idle.running:
            self.anti_idle.stop()
            self.status_var.set("Desativado ❌")
            self.toggle_btn.config(text="Ativar")
        else:
            try:
                self.anti_idle.start()
                self.status_var.set("Ativado ✅")
                self.toggle_btn.config(text="Desativar")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao ativar: {e}")

    def on_close(self):
        self.anti_idle.stop()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
