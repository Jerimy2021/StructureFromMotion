import os
import subprocess
import sys

def run_command(command, cwd=None):
    """Ejecuta un comando de shell en la carpeta especificada y captura la salida."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {command}")
        print(e.stderr.decode())
        sys.exit(1)  # Termina el script en caso de error

def main(project_path):
    # Cambia el directorio de trabajo al directorio del proyecto
    os.chdir(project_path)
    # print(project_path)

    # Paso 1: Ejecutar InterfaceCOLMAP en dense/sparse
    # print("Ejecutando InterfaceCOLMAP...")
    run_command("InterfaceCOLMAP -i ./dense -o ./model.mvs")

    # Paso 2: Ejecutar DensifyPointCloud en dense
    # print("Ejecutando DensifyPointCloud...")
    run_command("DensifyPointCloud --input-file ./model.mvs --working-folder ./ --output-file ./model_dense.mvs --archive-type -1", cwd=project_path)

    # Paso 3: Ejecutar ReconstructMesh en dense
    # print("Ejecutando ReconstructMesh...")
    run_command("ReconstructMesh --input-file ./model_dense.mvs --working-folder ./ --output-file ./model_dense_mesh.mvs", cwd=project_path)

    # Paso 4: Ejecutar RefineMesh en dense
    # print("Ejecutando RefineMesh...")
    run_command("RefineMesh -i ./model_dense.mvs -m ./model_dense_mesh.ply -o ./scene_mesh_refined.mvs", cwd=project_path)

    # Paso 5: Ejecutar TextureMesh en dense
    #print("Ejecutando TextureMesh...")
    run_command("TextureMesh -i model_dense.mvs -m model_dense_mesh.ply -o scene_mesh_refined_textured.mvs", cwd=project_path)

    #print("Proceso completado exitosamente.")

    output = "proceso completado exitosamente"
    return output

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <ruta_al_proyecto>")
        sys.exit(1)

    # Obtener la ruta del proyecto de los argumentos del script
    project_path = sys.argv[1]
    main(project_path)

