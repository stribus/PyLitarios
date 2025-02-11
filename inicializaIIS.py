import win32serviceutil
import win32service
import win32api
from tkinter import messagebox
import ctypes
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    messagebox.showerror("Este script precisa ser executado como administrador.", "Por favor, execute este script como administrador.")
    sys.exit(1)

# Nome do serviço que você deseja ativar e inicializar
service_name = "W3SVC"
try:
    # Verifica o status do serviço
    serviceStatus = win32serviceutil.QueryServiceStatus(service_name)
    
    # Abre o gerenciador de serviços
    scm_handle = win32service.OpenSCManager(
        None, None, win32service.SC_MANAGER_ALL_ACCESS
    )

    # Abre o serviço específico
    service_handle = win32service.OpenService(
        scm_handle, service_name, win32service.SERVICE_ALL_ACCESS
    )
    if service_handle == 0:
        messagebox.showerror("Erro", f"Não foi possível abrir o serviço {service_name}.")
        sys.exit(1)
    
    #verifica se o serviço está abilitado ou desabilitado
    # se desabilitado, habilita o serviço
    serviceConfig = win32service.QueryServiceConfig(service_handle)
    if serviceConfig[1] == win32service.SERVICE_DISABLED:
        messagebox.showinfo(message=f"Habilitando o serviço {service_name}...")
        win32service.ChangeServiceConfig(
                service_handle,
                win32service.SERVICE_NO_CHANGE,  # Tipo de serviço (não alterar)
                win32service.SERVICE_AUTO_START,  # Tipo de inicialização: automática
                win32service.SERVICE_NO_CHANGE,  # Controle de erro (não alterar)
                None,  # Caminho do binário (não alterar)
                None,  # Grupo de carga (não alterar)
                False,  # bFetchTag (não alterar)
                None,  # Dependências (não alterar)
                None,  # Nome da conta de serviço (não alterar)
                None,  # Senha da conta de serviço (não alterar)
                None,  # Nome de exibição (não alterar)                
            )
        if win32service.QueryServiceConfig(service_name)[1] == win32service.SERVICE_DISABLED:
            messagebox.showerror("Erro", f"Não foi possível habilitar o serviço {service_name}.")
            sys.exit(1)
        messagebox.showinfo(message=f"Serviço {service_name} habilitado com sucesso.")

    # Se o serviço não estiver em execução, inicia o serviço
    if serviceStatus[1] != win32service.SERVICE_RUNNING:
        messagebox.showinfo(message=f"Iniciando o serviço {service_name}...")
        win32serviceutil.StartService(service_name)
        messagebox.showinfo(message=f"Serviço {service_name} iniciado com sucesso.")
    else:
        messagebox.showinfo(message=f"O serviço {service_name} já está em execução.")

    # Verifica o status novamente após a tentativa de inicialização
    serviceStatus = win32serviceutil.QueryServiceStatus(service_name)
    messagebox.showinfo(message=f"Status do serviço {service_name} após a inicialização: {serviceStatus}")
except Exception as e:
    messagebox.showerror("Erro", str(e))
finally:
    # Fecha os handles
    win32service.CloseServiceHandle(service_handle)
    win32service.CloseServiceHandle(scm_handle)
    sys.exit(0)