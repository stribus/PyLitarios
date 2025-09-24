import pytubefix
import ffmpeg
import os
import sys
import subprocess

def validateUrl(url):

    if not url.startswith("https://") and not url.startswith("http://") and url.startswith("www."):
        url = "https://" + url
    if "https://www.youtube.com/watch?v=" in url:
        return True
    if "https://youtu.be/" in url:
        return True
    if "https://www.youtube.com/playlist?list=" in url:
        return True
    if "https://www.youtube.com/live/" in url:
        return True
    return False

def checkAndUpdatePytubefix():
    return # Desativado para evitar problemas em ambientes sem internet
    try:
        subprocess.run(["pip", "show", "pytubefix"], check=True, capture_output=True)
        subprocess.run(["pip", "install", "--upgrade", "pytubefix"], check=True)
        subprocess.run(["pip", "install", "--upgrade", "ffmpeg-python"], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["pip", "install", "pytubefix"], check=True)
        subprocess.run(["pip", "install", "ffmpeg-python"], check=True)

def downloadAudio(videoUrl, tipo='mp3', outputDir=''):
    yt = pytubefix.YouTube(videoUrl, use_po_token=True, client='WEB')
    if tipo == 'mp3' or tipo == 'wav':
        stream = yt.streams.filter(only_audio=True).first()
    else:
        stream = yt.streams.get_highest_resolution()

    if stream is None:
        print("Nenhum stream disponível para o vídeo.")
        return None

    # Retira os caracteres especiais e espaços do nome do vídeo
    filename = ''.join(e for e in yt.title if e.isalnum())
    if outputDir:
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        outputPath = os.path.join(outputDir, f"{filename}.{tipo}")
    else:
        outputPath = f"{filename}.{tipo}"

    if tipo == 'webm':
        stream.download(filename=outputPath)
        return outputPath

    ffmpeg.input(stream.url).output(outputPath).run()
    return outputPath

if __name__ == "__main__":
    checkAndUpdatePytubefix()

    if len(sys.argv) < 2:
        print("Falta o link do vídeo")
        print("Uso: python downloadyoutube.py <link do vídeo> [mp3|wav|mp4]")
        sys.exit(1)

    url = sys.argv[1]
    if not validateUrl(url):
        print("Link inválido")
        sys.exit(1)

    tipo = 'mp4'
    if len(sys.argv) > 2:
        tipo = sys.argv[2]

    downloadAudio(url, tipo)