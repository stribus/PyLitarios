# PyLitarios

Este projeto contém diversos scripts Python para diferentes finalidades que auxiliam no meu trabalho, como gerenciar serviços do IIS, automatizar cliques, capturas de tela em base64 e conversão de arquivos.

## Scripts Disponíveis

### 🔄 base64_converter.py

Conversor bidirecional de arquivos para base64 e vice-versa.

**Funcionalidades:**

- Converte qualquer arquivo binário para texto base64
- Converte arquivos de texto base64 de volta para o formato binário original
- Interface amigável com feedback visual
- Suporte para todos os tipos de arquivo

**Uso:**

```bash
# Codificar arquivo para base64
python base64_converter.py encode arquivo.pdf

# Codificar com nome de saída personalizado
python base64_converter.py encode imagem.png imagem_base64.txt

# Decodificar base64 para arquivo binário
python base64_converter.py decode arquivo.pdf.base64.txt

# Decodificar com nome de saída personalizado
python base64_converter.py decode dados.txt arquivo_original.bin
```


### 📸 capture2base64.py

Captura uma área da tela e copia a imagem em base64 para a área de transferência.

### 🖱️ clicker.py

Realiza cliques automatizados conforme parâmetros definidos.

### 🌐 inicializaIIS.py

Ativa e inicializa o serviço W3SVC do IIS.

### 💤 anti_idle.py

Impeça que o computador local entre em espera e evite desconexão por ociosidade em sessões RDP (mstsc).
Interface gráfica para ativar/desativar facilmente.


**Funcionalidades:**

- Mantém o PC local ativo (impede suspensão)
- Simula atividade para evitar desconexão em RDP (mstsc)
- Interface simples para ativar/desativar

**Uso:**

```bash
python anti_idle.py
```

### ⬇️ downloadyoutube.py

Baixa vídeos ou áudios do YouTube em vários formatos (mp3, mp4, wav, webm).


**Funcionalidades:**

- Suporte a download de vídeo ou apenas áudio
- Conversão automática para mp3, wav, webm ou mp4
- Feedback de progresso no terminal

**Uso:**

```bash
# Baixar vídeo em mp4
python downloadyoutube.py "https://www.youtube.com/watch?v=ID" mp4

# Baixar apenas áudio em mp3
python downloadyoutube.py "https://www.youtube.com/watch?v=ID" mp3
```

## Dependências

Verifique o arquivo `requirements.txt` para instalação das dependências necessárias:


```bash
pip install -r requirements.txt
```

## Uso

1. Execute cada script conforme sua função:
   - **inicializaIIS.py**: Ativa e inicializa o serviço W3SVC.
   - **clicker.py**: Realiza cliques automatizados conforme parâmetros definidos.
   - **capture2base64.py**: Captura uma área da tela e copia a imagem em base64 para a área de transferência.
2. É importante executar alguns scripts como administrador, caso necessário.
3. Para criar executáveis, utilize o PyInstaller:


```bash
pyinstaller --onefile inicializaIIS.py
```
