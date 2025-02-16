import subprocess
import re
import sys
from win32api import *



def get_version_number(file_path): 
    File_information = GetFileVersionInfo(file_path, "\\") 

    ms_file_version = File_information['FileVersionMS'] 
    ls_file_version = File_information['FileVersionLS'] 

    return [str(HIWORD(ms_file_version)), str(LOWORD(ms_file_version)), 
            str(HIWORD(ls_file_version)), str(LOWORD(ls_file_version))] 


def get_version(file_path):
    try:
        try:
            version = get_version_number(file_path)
            return '.'.join(version)
        except Exception as e:
            output = subprocess.check_output([file_path, '--version'], stderr=subprocess.STDOUT)
            version = re.search(r'(\d+\.\d+\.\d+\.\d+)', output.decode('utf-8')).group(1)
            return version
    except Exception as e:
        program = file_path.split('\\')[-1]
        print(f"Erro ao obter a versão do {program}: {e}")
        sys.exit(1)



def check_webdriver_compatibility(browser_path, webdriver_path)->bool:
    browser_version = get_version(browser_path)
    webdriver_version = get_version(webdriver_path)

    return browser_version.split('.')[0] == webdriver_version.split('.')[0]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python checkwebDriverversion.py <caminho_do_browser> <caminho_do_webdriver>")
        sys.exit(1)

    browser_path = sys.argv[1]
    webdriver_path = sys.argv[2]
    if check_webdriver_compatibility(browser_path, webdriver_path):
        print("A versão do WebDriver é compatível com a versão do browser.")
    else:
        print("A versão do WebDriver não é compatível com a versão do browser.")
    