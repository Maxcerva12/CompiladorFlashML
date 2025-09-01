from flask import Flask, request, jsonify, send_from_directory # type: ignore
import logging
import os
import time
from main import compilar_codigo

app = Flask(__name__, static_folder='static', template_folder='templates')


logging.basicConfig(
    filename='compilador_flashml.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

GENERADOS_DIR = os.path.join(app.static_folder, 'generados')
if not os.path.exists(GENERADOS_DIR):
    os.makedirs(GENERADOS_DIR)

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route("/documentation")
def documentation():
    return send_from_directory('templates','documentation.html')

@app.route('/compilar', methods=['POST'])
def compilar():
    codigo = request.json.get('codigo')
    if not codigo:
        error_msg = "No se proporcionó código para compilar"
        logging.error(error_msg)
        return jsonify({'error': error_msg, 'errores': [{'tipo': 'general', 'mensaje': error_msg}]}), 400
    
    logging.info("Recibido código FlashML para compilar desde la interfaz web")
    try:
        
        timestamp = int(time.time())
        archivo_salida = os.path.join(GENERADOS_DIR, f"output_{timestamp}.html")
        resultado = compilar_codigo(codigo, archivo_entrada=f"web_input_{timestamp}.flashml", archivo_salida=archivo_salida)
        
        if resultado['html']:
            logging.info("Compilación exitosa desde la interfaz web")
            return jsonify({
                'success': True,
                'html_path': os.path.relpath(archivo_salida, app.static_folder),
                'intermedio_path': os.path.relpath(resultado['intermedio'], app.static_folder)
            })
        else:
            error_msg = "Errores durante la compilación. Revisa el código."
            logging.error(error_msg)
            return jsonify({'success': False, 'errores': resultado['errores']}), 400
    except Exception as e:
        error_msg = f"Error al compilar desde la interfaz web: {str(e)}"
        logging.error(error_msg)
        return jsonify({'success': False, 'errores': [{'tipo': 'general', 'mensaje': error_msg}]}), 400

@app.route('/output/<filename>')
def serve_output(filename):
    
    try:
        return send_from_directory(GENERADOS_DIR, filename)
    except Exception as e:
        logging.error(f"Error al servir el archivo HTML: {str(e)}")
        return "Archivo HTML no encontrado", 404

@app.route('/archivos', methods=['GET'])
def listar_archivos():
    
    try:
        archivos = []
        for filename in os.listdir(GENERADOS_DIR):
            if filename.endswith(('.html', '.json')):
                filepath = os.path.join(GENERADOS_DIR, filename)
                stat = os.stat(filepath)
                archivos.append({
                    'nombre': filename,
                    'tamano': f"{stat.st_size / 1024:.1f} KB",
                    'fecha': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime)),
                    'path': os.path.relpath(filepath, app.static_folder)
                })
        return jsonify({'archivos': sorted(archivos, key=lambda x: x['fecha'], reverse=True)})
    except Exception as e:
        logging.error(f"Error al listar archivos: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)