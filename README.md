# PyLitarios

Este projeto contém diversos scripts Python para diferentes finalidades que auxiliam no meu trabalho, como gerenciar serviços do IIS, automatizar cliques e capturas de tela em base64.

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
````
