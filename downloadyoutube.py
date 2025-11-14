import ffmpeg
import os
import subprocess
import sys
import tempfile
import pytubefix

def on_progress(stream, chunk, bytes_remaining):
    total_size = getattr(stream, 'filesize', None)
    title = getattr(stream, 'title', 'vídeo')
    if total_size:
        downloaded = total_size - bytes_remaining
        percent = downloaded / total_size * 100
        print(f"Baixando {title}: {percent:.1f}%")
    else:
        print(f"Baixando {title}: {bytes_remaining} bytes restantes")

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
    yt = pytubefix.YouTube(videoUrl, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)
    audio_only = tipo in ('mp3', 'wav', 'webm')
    if audio_only:
        # stream = yt.streams.filter(only_audio=True).first()
        stream = yt.streams.get_audio_only()
    else:
        stream = yt.streams.get_highest_resolution()

    if stream is None:
        print("Nenhum stream disponível para o vídeo.")
        return None

    # Retira os caracteres especiais e espaços do nome do vídeo
    filename = ''.join(e for e in yt.title if e.isalnum())
    if outputDir:
        os.makedirs(outputDir, exist_ok=True)
        final_output = os.path.join(outputDir, f"{filename}.{tipo}")
    else:
        final_output = f"{filename}.{tipo}"

    temp_path = None
    if tipo == 'webm':
        stream.download(output_path=outputDir or None, filename=f"{filename}.webm")
        return final_output

    media_path = stream.download(output_path=outputDir or None, filename=filename)
    if audio_only and tipo in ('mp3', 'wav'):
        try:
            ffmpeg.input(media_path).output(final_output, **({'format': tipo} if tipo == 'mp3' else {})).run(overwrite_output=True)
        finally:
            if media_path and os.path.exists(media_path):
                os.remove(media_path)
        return final_output

    return media_path

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