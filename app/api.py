from flask import Flask, request, jsonify
import subprocess
import sys
import os

app = Flask(__name__)

def run_script(script_path, project_path):

    try:
        result = subprocess.run(
            [sys.executable, script_path, project_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout = result.stdout.decode()
        stderr = result.stderr.decode()
        print("STDOUT:", stdout)
        print("STDERR:", stderr)

        return stdout + stderr
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode()
        print(f"Error al ejecutar el script {script_path}: {stderr}")
        return f"Error al ejecutar el script: {e.stderr.decode()}"

@app.route('/run_colmap', methods=['POST'])
def run_colmap():
    data = request.json
    project_path = data.get("project_path")
    if not project_path:
        return jsonify({"error": "La ruta del proyecto es requerida"}), 400

    output = run_script("./Colmap.py", project_path)
    return jsonify({"output": output})

@app.route('/run_openmvs', methods=['POST'])
def run_openmvs():
    data = request.json
    project_path = data.get("project_path")
    # print(project_path)
    if not project_path:
        return jsonify({"error": "La ruta del proyecto es requerida"}), 400

    output = run_script("./OpenMVS.py", project_path)
    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


