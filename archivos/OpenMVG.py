import subprocess
import os
import sys
import time

def openMVG_main(path):
    if not os.path.exists(path):
        print(f"Error: el directorio '{path}' no existe.")
        sys.exit(1)

    # Verifica y crea los directorios de salida si no existen
    init_dir = os.path.join(path, "../init")
    matches_dir = os.path.join(path, "../matches")
    reconstruction_dir = os.path.join(path, "../reconstruction")
    os.makedirs(init_dir, exist_ok=True)
    os.makedirs(matches_dir, exist_ok=True)
    os.makedirs(reconstruction_dir, exist_ok=True)

    cmds = [
        {
            "description": "Listar imágenes en el directorio",
            "command": f"openMVG_main_SfMInit_ImageListing -i {path} -o {init_dir} -d /Users/pierre/Development/openMVG/src/openMVG/exif/sensor_width_database/sensor_width_camera_database.txt -f 2340",
            "expected_output": os.path.join(init_dir, "sfm_data.json")
        },
        {
            "description": "Calcular características",
            "command": f"openMVG_main_ComputeFeatures -i {os.path.join(init_dir, 'sfm_data.json')} -o {matches_dir} -m SIFT",
            "expected_output": os.path.join(matches_dir, "image_describer.json")
        },
        {
            "description": "Generar pares de coincidencias",
            "command": f"openMVG_main_PairGenerator -i {os.path.join(init_dir, 'sfm_data.json')} -o {os.path.join(matches_dir, 'pairs.bin')}",
            "expected_output": os.path.join(matches_dir, "pairs.bin")
        },
        {
            "description": "Calcular coincidencias",
            "command": f"openMVG_main_ComputeMatches -i {os.path.join(init_dir, 'sfm_data.json')} -p {os.path.join(matches_dir, 'pairs.bin')} -o {os.path.join(matches_dir, 'matches.putative.bin')}",
            "expected_output": os.path.join(matches_dir, "matches.putative.bin")
        },
        {
            "description": "Filtrar coincidencias geométricas",
            "command": f"openMVG_main_GeometricFilter -i {os.path.join(init_dir, 'sfm_data.json')} -m {os.path.join(matches_dir, 'matches.putative.bin')} -g f -o {os.path.join(matches_dir, 'matches.f.bin')}",
            "expected_output": os.path.join(matches_dir, "matches.f.bin")
        },
        {
            "description": "Reconstrucción incremental de estructura",
            "command": f"openMVG_main_Sfm --sfm_engine INCREMENTAL --input_file {os.path.join(init_dir, 'sfm_data.json')} --match_dir {matches_dir} --output_dir {reconstruction_dir}",
            "expected_output": os.path.join(reconstruction_dir, "sfm_data.bin")
        },
        {
            "description": "Colorizar estructura",
            "command": f"openMVG_main_ComputeSfM_DataColor -i {os.path.join(reconstruction_dir, 'sfm_data.bin')} -o {os.path.join(reconstruction_dir, 'colorized.ply')}",
            "expected_output": os.path.join(reconstruction_dir, "colorized.ply")
        },
        {
            "description": "Computar structure from known poses",
            "command": f"openMVG_main_ComputeStructureFromKnownPoses -i {os.path.join(reconstruction_dir, 'sfm_data.bin')} -m {matches_dir} -o {os.path.join(matches_dir, 'robustFitting.json')} -r 4.0",
            "expected_output": os.path.join(matches_dir, "robustFitting.json")
        },
        {
            "description": "Exportar imágenes sin distorsión",
            "command": f"openMVG_main_ExportUndistortedImages -i {os.path.join(reconstruction_dir, 'sfm_data.bin')} -o {os.path.join(matches_dir, 'undistortedImages')}",
            "expected_output": os.path.join(matches_dir, "undistortedImages")
        },
        {
            "description": "Convertir a formato OpenMVS",
            "command": f"openMVG_main_openMVG2openMVS -i {os.path.join(reconstruction_dir, 'sfm_data.bin')} -d {os.path.join(matches_dir, 'undistortedImages/')} -o {os.path.join(reconstruction_dir, 'scene.mvs')}",
            "expected_output": os.path.join(reconstruction_dir, "scene.mvs")
        }
    ]

    for cmd in cmds:
        print(f"Ejecutando: {cmd['description']}")
        try:
            result = subprocess.run(cmd["command"], shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)  # Mostrar salida estándar
            print(result.stderr)  # Mostrar salida de error, si existe
            
            # Espera hasta que el archivo de salida esperado esté disponible
            expected_output = cmd["expected_output"]
            if not os.path.exists(expected_output):
                print(f"Esperando que se genere el archivo {expected_output}...")
                time.sleep(3)
                if not os.path.exists(expected_output):
                    print(f"Error: No se generó el archivo esperado {expected_output}.")
                    sys.exit(1)

        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar {cmd['description']}: {e}")
            print(f"Salida de error:\n{e.stderr}")  # Captura y muestra el error
            sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Uso: python OpenMVG.py <ruta_al_directorio>")
        sys.exit(1)
    
    path = sys.argv[1]
    openMVG_main(path)

if __name__ == "__main__":
    main()

