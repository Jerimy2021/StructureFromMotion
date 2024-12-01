import os
import subprocess
import sys

def run_command(command, cwd=None):
    """Ejecuta un comando de shell en la carpeta especificada y captura la salida."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {command}")
        print(e.stderr.decode())
        sys.exit(1)  # Termina el script en caso de error

def main(project_path):
    # Cambia el directorio de trabajo al directorio del proyecto
    os.chdir(project_path)

    # Paso 1: Ejecutar feature_extractor
    # print("Ejecutando feature_extractor...")
    run_command("colmap feature_extractor --database_path ./database.db --image_path ./images")

    # Paso 2: Ejecutar exhaustive_matcher
    # print("Ejecutando exhaustive_matcher...")
    run_command("colmap exhaustive_matcher --database_path ./database.db")

    # Paso 3: Crear carpeta 'sparse' si no existe
    sparse_path = os.path.join(project_path, "sparse")
    if not os.path.exists(sparse_path):
        os.makedirs(sparse_path)

    # Paso 4: Ejecutar mapper
    # print("Ejecutando mapper...")
    run_command("colmap mapper --database_path ./database.db --image_path ./images --output_path ./sparse")

    # Paso 5: Ejecutar image_undistorter
    # print("Ejecutando image_undistorter...")
    run_command("colmap image_undistorter --image_path ./images --input_path ./sparse/0 --output_path ./dense --output_type COLMAP")

    # Paso 6: Ejecutar model_converter
    # print("Ejecutando model_converter...")
    run_command("colmap model_converter --input_path ./dense/sparse --output_path ./dense/sparse --output_type TXT")

    #print("Proceso completado exitosamente.")
    output = "proceso completado exitosamente"
    return output

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python Colmap.py <ruta_al_proyecto>")
        sys.exit(1)
    
    # Obtener la ruta del proyecto de los argumentos del script
    project_path = sys.argv[1]
    main(project_path)

