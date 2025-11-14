import win32serviceutil
import win32service
import win32api
import ctypes
import sys
import traceback
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Interface principal
class IISInitApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inicializando IIS")
        self.geometry("400x450")
        self.resizable(False, False)
        self.steps = [
            "Verificando serviços",
            "Verificando status do serviço W3SVC",
            "Habilitando serviço W3SVC",
            "Verificando serviço rodando",
            "Inicializando serviço"
        ]
        self.status = ["pendente"] * len(self.steps)
        self.monitoring = False
        self.monitoring_thread = None
        self.service_name = "W3SVC"
        self.create_widgets()
        self.after(500, self.run_steps)

    def create_widgets(self):
        tk.Label(self, text="Inicializando IIS", font=("Arial", 16, "bold")).pack(pady=10)
        self.frame = tk.Frame(self)
        self.frame.pack(pady=10)
        self.check_vars = []
        for i, step in enumerate(self.steps):
            var = tk.StringVar(value="[ ]")
            self.check_vars.append(var)
            lbl = tk.Label(self.frame, textvariable=var, font=("Arial", 12))
            lbl.grid(row=i, column=0, sticky="w")
            tk.Label(self.frame, text=step, font=("Arial", 12)).grid(row=i, column=1, sticky="w")
        self.result_label = tk.Label(self, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=10)
        
        # Separador
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=10)
        
        # Seção de monitoramento
        tk.Label(self, text="Monitoramento Contínuo", font=("Arial", 14, "bold")).pack(pady=5)
        
        self.monitor_btn = tk.Button(self, text="Iniciar Monitoramento", 
                                   command=self.toggle_monitoring, 
                                   bg="green", fg="white", font=("Arial", 11, "bold"))
        self.monitor_btn.pack(pady=5)
        
        self.monitor_status_label = tk.Label(self, text="Monitoramento: Parado", 
                                           font=("Arial", 10), fg="red")
        self.monitor_status_label.pack(pady=5)
        
        self.ok_btn = tk.Button(self, text="OK", state="disabled", command=self.close_app)
        self.ok_btn.pack(pady=10)

    def mark_step(self, idx, success=True):
        self.check_vars[idx].set("[✔]" if success else "[✖]")
    
    def toggle_monitoring(self):
        if not self.monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()
    
    def start_monitoring(self):
        if not is_admin():
            messagebox.showerror("Erro", "Execute como administrador para usar o monitoramento.")
            return
        
        self.monitoring = True
        self.monitor_btn.config(text="Parar Monitoramento", bg="red")
        self.monitor_status_label.config(text="Monitoramento: Ativo", fg="green")
        
        # Inicia thread de monitoramento
        self.monitoring_thread = threading.Thread(target=self.monitor_service, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        self.monitoring = False
        self.monitor_btn.config(text="Iniciar Monitoramento", bg="green")
        self.monitor_status_label.config(text="Monitoramento: Parado", fg="red")
    
    def monitor_service(self):
        while self.monitoring:
            try:
                # Verifica status do serviço
                serviceStatus = win32serviceutil.QueryServiceStatus(self.service_name)
                
                if serviceStatus[1] != win32service.SERVICE_RUNNING:
                    # Serviço parou, tentar reiniciar
                    self.after(0, lambda: self.monitor_status_label.config(
                        text="Serviço parou! Reiniciando...", fg="orange"))
                    
                    success = self.restart_service()
                    
                    if success:
                        self.after(0, lambda: self.monitor_status_label.config(
                            text="Serviço reiniciado com sucesso!", fg="green"))
                    else:
                        self.after(0, lambda: self.monitor_status_label.config(
                            text="Erro ao reiniciar serviço!", fg="red"))
                        # Para o monitoramento em caso de erro
                        self.after(0, self.stop_monitoring)
                        break
                
                # Aguarda 5 segundos antes da próxima verificação
                time.sleep(5)
                
            except Exception as e:
                self.after(0, lambda: self.monitor_status_label.config(
                    text=f"Erro no monitoramento: {str(e)}", fg="red"))
                self.after(0, self.stop_monitoring)
                break
    
    def restart_service(self):
        try:
            # # Abre gerenciador de serviços
            # scm_handle = win32service.OpenSCManager(
            #     None, None, win32service.SC_MANAGER_ALL_ACCESS
            # )
            # service_handle = win32service.OpenService(
            #     scm_handle, self.service_name, win32service.SERVICE_ALL_ACCESS
            # )
            
            # if service_handle == 0:
            #     return False
            
            # # Verifica se está habilitado
            # serviceConfig = win32service.QueryServiceConfig(service_handle)
            # if serviceConfig[1] == win32service.SERVICE_DISABLED:
            #     # Habilita o serviço
            #     win32service.ChangeServiceConfig(
            #         service_handle,
            #         win32service.SERVICE_NO_CHANGE,
            #         win32service.SERVICE_AUTO_START,
            #         win32service.SERVICE_NO_CHANGE,
            #         None, None, False, None, None, None, None
            #     )
            
            # # Inicia o serviço
            # win32serviceutil.StartService(self.service_name)
            
            # win32service.CloseServiceHandle(service_handle)
            # win32service.CloseServiceHandle(scm_handle)
            
            for i, step in enumerate(self.steps):
                self.check_vars[i].set("[ ]")
                
            self.run_steps()
            
            return True
            
        except Exception as e:
            print(f"Erro ao reiniciar serviço: {e}")
            return False

    def run_steps(self):
        # Verifica admin
        if not is_admin():
            self.result_label.config(text="Execute como administrador.", fg="red")
            self.mark_step(0, False)
            self.ok_btn.config(state="normal")
            return
        self.mark_step(0)
        self.update()
        
        try:
            # Verifica status do serviço
            serviceStatus = win32serviceutil.QueryServiceStatus(self.service_name)
            self.mark_step(1)
            self.update()

            # Abre gerenciador de serviços
            scm_handle = win32service.OpenSCManager(
                None, None, win32service.SC_MANAGER_ALL_ACCESS
            )
            service_handle = win32service.OpenService(
                scm_handle, self.service_name, win32service.SERVICE_ALL_ACCESS
            )
            if service_handle == 0:
                self.result_label.config(text=f"Não foi possível abrir o serviço {self.service_name}.", fg="red")
                self.mark_step(2, False)
                self.ok_btn.config(state="normal")
                return

            # Verifica se está habilitado
            serviceConfig = win32service.QueryServiceConfig(service_handle)
            if serviceConfig[1] == win32service.SERVICE_DISABLED:
                self.mark_step(2)
                self.result_label.config(text=f"Habilitando o serviço {self.service_name}...")
                self.update()
                win32service.ChangeServiceConfig(
                    service_handle,
                    win32service.SERVICE_NO_CHANGE,
                    win32service.SERVICE_AUTO_START,
                    win32service.SERVICE_NO_CHANGE,
                    None, None, False, None, None, None, None
                )
                if win32service.QueryServiceConfig(service_handle)[1] == win32service.SERVICE_DISABLED:
                    self.result_label.config(text=f"Não foi possível habilitar o serviço {self.service_name}.", fg="red")
                    self.mark_step(2, False)
                    self.ok_btn.config(state="normal")
                    win32service.CloseServiceHandle(service_handle)
                    win32service.CloseServiceHandle(scm_handle)
                    return
                self.result_label.config(text=f"Serviço {self.service_name} habilitado com sucesso.")
            else:
                self.mark_step(2)
            self.update()

            # Verifica se está rodando
            if serviceStatus[1] != win32service.SERVICE_RUNNING:
                self.mark_step(3)
                self.result_label.config(text=f"Inicializando o serviço {self.service_name}...")
                self.update()
                win32serviceutil.StartService(self.service_name)
                self.mark_step(4)
                self.result_label.config(text=f"Serviço {self.service_name} iniciado com sucesso.", fg="green")
            else:
                self.mark_step(3)
                self.mark_step(4)
                self.result_label.config(text=f"O serviço {self.service_name} já está em execução.", fg="green")

            win32service.CloseServiceHandle(service_handle)
            win32service.CloseServiceHandle(scm_handle)
            self.ok_btn.config(state="normal")
        except Exception as e:
            self.result_label.config(text=f"Erro: {str(e)}", fg="red")
            for i in range(len(self.steps)):
                if self.check_vars[i].get() == "[ ]":
                    self.mark_step(i, False)
            self.ok_btn.config(state="normal")
    
    def close_app(self):
        # Para o monitoramento antes de fechar
        if self.monitoring:
            self.stop_monitoring()
        self.quit()

def main():
    app = IISInitApp()
    app.mainloop()
    sys.exit(0)

if __name__ == "__main__":
    main()

