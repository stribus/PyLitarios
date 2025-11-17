#!/usr/bin/env python3
"""
Conversor de arquivos para Base64 e vice-versa

Este script permite:
1. Converter qualquer arquivo binário para um arquivo de texto com conteúdo em base64
2. Converter um arquivo de texto base64 de volta para o arquivo binário original

Uso:
    python base64_converter.py encode <arquivo_entrada> [arquivo_saida.txt]
    python base64_converter.py decode <arquivo_base64.txt> [arquivo_saida]
"""

import base64
import binascii
import sys
import os
from pathlib import Path
from typing import Optional

def encode_file_to_base64(input_file: str, output_file: Optional[str] = None) -> bool:
    """
    Converte um arquivo binário para texto base64.
    
    Args:
        input_file: Caminho do arquivo de entrada
        output_file: Caminho do arquivo de saída (opcional)
        
    Returns:
        bool: True se a conversão foi bem-sucedida, False caso contrário
    """
    try:
        # Define o arquivo de saída se não fornecido
        if output_file is None:
            output_file = f"{input_file}.base64.txt"
        
        # Lê o arquivo binário
        print(f"📖 Lendo arquivo: {input_file}")
        with open(input_file, 'rb') as f:
            file_content = f.read()
        
        # Converte para base64
        print(f"🔄 Convertendo para base64...")
        base64_content = base64.b64encode(file_content)
        
        # Salva o conteúdo base64 em um arquivo de texto
        print(f"💾 Salvando em: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(base64_content.decode('utf-8'))
        
        file_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file)
        
        print(f"✅ Conversão concluída com sucesso!")
        print(f"   Tamanho original: {file_size:,} bytes")
        print(f"   Tamanho base64: {output_size:,} bytes")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{input_file}' não encontrado.")
        return False
    except PermissionError:
        print(f"❌ Erro: Sem permissão para ler/escrever arquivos.")
        return False
    except Exception as e:
        print(f"❌ Erro ao converter arquivo: {e}")
        return False

def decode_base64_to_file(input_file: str, output_file: Optional[str] = None) -> bool:
    """
    Converte um arquivo de texto base64 de volta para arquivo binário.
    
    Args:
        input_file: Caminho do arquivo base64 de entrada
        output_file: Caminho do arquivo de saída (opcional)
        
    Returns:
        bool: True se a conversão foi bem-sucedida, False caso contrário
    """
    try:
        # Define o arquivo de saída se não fornecido
        if output_file is None:
            # Remove a extensão .txt e .base64 se existirem
            output_file = input_file.replace('.base64.txt', '').replace('.txt', '')
            if output_file == input_file:
                output_file = f"{input_file}.decoded"
        
        # Lê o arquivo de texto base64
        print(f"📖 Lendo arquivo base64: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            base64_content = f.read().strip()
        
        # Decodifica o base64
        print(f"🔄 Decodificando base64...")
        file_content = base64.b64decode(base64_content)
        
        # Salva o arquivo binário
        print(f"💾 Salvando arquivo binário em: {output_file}")
        with open(output_file, 'wb') as f:
            f.write(file_content)
        
        input_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file)
        
        print(f"✅ Decodificação concluída com sucesso!")
        print(f"   Tamanho base64: {input_size:,} bytes")
        print(f"   Tamanho final: {output_size:,} bytes")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{input_file}' não encontrado.")
        return False
    except binascii.Error:
        print(f"❌ Erro: O arquivo não contém base64 válido.")
        return False
    except PermissionError:
        print(f"❌ Erro: Sem permissão para ler/escrever arquivos.")
        return False
    except Exception as e:
        print(f"❌ Erro ao decodificar arquivo: {e}")
        return False


def print_usage():
    """Imprime instruções de uso do script."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║           Conversor de Arquivos Base64                        ║
╚═══════════════════════════════════════════════════════════════╝

Uso:
    python base64_converter.py encode <arquivo_entrada> [arquivo_saida.txt]
    python base64_converter.py decode <arquivo_base64.txt> [arquivo_saida]

Comandos:
    encode    Converte um arquivo binário para texto base64
    decode    Converte um arquivo base64 de volta para binário

Exemplos:
    # Codificar uma imagem para base64
    python base64_converter.py encode imagem.png

    # Codificar com nome de saída específico
    python base64_converter.py encode imagem.png imagem_codificada.txt

    # Decodificar um arquivo base64
    python base64_converter.py decode imagem.png.base64.txt

    # Decodificar com nome de saída específico
    python base64_converter.py decode dados.txt arquivo_original.bin
    """)


def main():
    """Função principal do script."""
    # Verifica argumentos
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    input_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Executa o comando apropriado
    if command == 'encode':
        success = encode_file_to_base64(input_file, output_file)
    elif command == 'decode':
        success = decode_base64_to_file(input_file, output_file)
    else:
        print(f"❌ Comando desconhecido: '{command}'")
        print_usage()
        sys.exit(1)
    
    # Retorna código de saída apropriado
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
