import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, ImageTk
import base64
import pyperclip
import io

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Captura")
        self.root.geometry("200x200")
        self.captura_btn = tk.Button(self.root, text="Capturar", command=self.iniciar_captura)
        self.captura_btn.pack(expand=True, fill='both')
        self.img_label = None

    def iniciar_captura(self):
        # Oculta a janela principal para permitir seleção
        self.root.withdraw()

        try:
            self.captureArea = tk.Toplevel(self.root)
            self.captureArea.attributes("-fullscreen", True)
            self.captureArea.attributes("-topmost", True)
            self.captureArea.attributes("-alpha", 0.3)
            self.captureArea.configure(background='grey')

            
            self.start_x = None
            self.start_y = None
            self.current_x = None
            self.current_y = None
            
            self.canvas = tk.Canvas(self.captureArea, bg='grey')
            self.canvas.pack(fill='both', expand=True)
            
            
            # Binding dos eventos do mouse
            self.canvas.bind("<ButtonPress-1>", self.on_press)
            self.canvas.bind("<B1-Motion>", self.on_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_release)

            # Tecla de escape para sair
            self.captureArea.bind("<Escape>", lambda e: self.stop_capture())
            
        
        except Exception as e:    
            messagebox.showerror("Erro", str(e))  
            if hasattr(self, "captureArea"):
                self.captureArea.destroy                          
            self.root.deiconify()

    def exibir_imagem(self, imagem):
        try:
            print("Exibindo imagem")
            imgysize = imagem.size[1]
            imgxsize = imagem.size[0]
            imgShow = imagem
            self.imagem = imagem
            if imgysize > 800 or imgxsize > 800:
                imgShow = imagem.resize((int(imgxsize/2), int(imgysize/2)))
            imgysize = imagem.size[1] +100
            imgxsize = imagem.size[0] +100
            self.root.geometry(f"{imgxsize}x{imgysize}")
            if self.img_label is None:
                self.img_label = tk.Label(self.root)
                self.img_label.pack()
            self.photo = ImageTk.PhotoImage(imagem)
            self.img_label.configure(image=self.photo)

            # Ajusta os botões Capturar e Copiar
            self.botao_frame = tk.Frame(self.root)
            self.botao_frame.pack(side=tk.BOTTOM, fill='x')

            if hasattr(self, "captura_btn"):
                self.captura_btn.destroy()
            
            if not(hasattr(self, "capturar_novamente_btn")):
                self.capturar_novamente_btn = tk.Button(self.botao_frame, text="Capturar", command=self.iniciar_captura)
                self.capturar_novamente_btn.pack(side=tk.LEFT, expand=True, fill='both')

            if not(hasattr(self, "copiar_btn")):
                self.copiar_btn = tk.Button(self.botao_frame, text="Copiar", command=self.copiar_para_area_de_transferencia)
                self.copiar_btn.pack(side=tk.LEFT, expand=True, fill='both')
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def copiar_para_area_de_transferencia(self):
        buffer = io.BytesIO()
        self.imagem.save(buffer, format="PNG")
        base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        pyperclip.copy(base64_str)
        messagebox.showinfo("Copiar", "Imagem em base64 copiada!")
        
    def on_press(self, event):
        try:
            # Salvar posição inicial
            self.start_x = event.x
            self.start_y = event.y
        except Exception as e:
            messagebox.showerror("Erro",f"Erro ao capturar a posição inicial: {e}")
            self.captureArea.destroy()
            self.root.deiconify()

    def on_drag(self, event):
        try:
            # Atualizar posição atual
            self.current_x = event.x
            self.current_y = event.y
            
            # Redesenhar retângulo
            self.canvas.delete("selection")
            self.canvas.create_rectangle(
                self.start_x, self.start_y,
                self.current_x, self.current_y,
                outline='red', tags="selection", width=3
            )
            #print(f"Arrastando: {self.start_x}, {self.start_y}, {self.current_x}, {self.current_y}")
        
        except Exception as e:
            print(f"Erro ao arrastar: {e}")
            if hasattr(self, "canvas"):
                self.canvas.delete("selection")
    
    
    def on_release(self, event):
        try:
            # Capturar a área selecionada
            if self.start_x and self.start_y and self.current_x and self.current_y:
                x1 = min(self.start_x, self.current_x)
                y1 = min(self.start_y, self.current_y)
                x2 = max(self.start_x, self.current_x)
                y2 = max(self.start_y, self.current_y)

                print (f"Capturando área: {x1}, {y1}, {x2}, {y2}")
                # Fecha a janela
                self.captureArea.withdraw()
                self.captureArea.after(100, lambda: self.capturar_area(x1, y1, x2, y2))
                
                print("Área capturada")
                
        finally:
            self.start_x = None
            self.start_y = None
            self.current_x = None
            self.current_y = None        
            # if hasattr(self, "captureArea"):
            #     self.captureArea.destroy()
            #     self.root.deiconify()
        

    def capturar_area(self, x1, y1, x2, y2):
        try:
            # Captura a tela
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            
            self.root.deiconify()
            self.exibir_imagem(screenshot)
            
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            raise e
        
    def stop_capture(self):
        if hasattr(self, "captureArea"):
            self.captureArea.destroy()
            self.root.deiconify()
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()