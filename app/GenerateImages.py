import subprocess
import sys
import os

def check_and_install_ffmpeg():
    try:
        # Verificar si ffmpeg está instalado
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("ffmpeg ya está instalado.")
    except subprocess.CalledProcessError:
        print("ffmpeg no está instalado. Intentando instalar...")
        # Instalar ffmpeg en Ubuntu usando apt
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True)
            print("ffmpeg instalado con éxito.")
        except Exception as e:
            print(f"No se pudo instalar ffmpeg automáticamente. Error: {e}")
            sys.exit(1)

def extract_frames(video_path, output_pattern, fps=2):
    if not os.path.exists(video_path):
        print(f"El archivo de video no existe: {video_path}")
        sys.exit(1)
    
    command = [
        "ffmpeg", 
        "-i", video_path, 
        "-vf", f"fps={fps}", 
        output_pattern
    ]
    try:
        subprocess.run(command, check=True)
        print("Imágenes generadas con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar ffmpeg: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ruta del video y patrón de salida de las imágenes
    video_path = "/home/utec/Desktop/utechie_1.mp4"  # Cambia esto por la ruta de tu video
    output_pattern = "/home/utec/Desktop/prueba/images/imagen_%04d.png"  # Cambia esto si necesitas otro formato
    
    # Verificar e instalar ffmpeg si es necesario
    check_and_install_ffmpeg()
    
    # Generar imágenes del video
    extract_frames(video_path, output_pattern)
