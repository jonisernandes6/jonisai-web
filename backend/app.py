import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.secret_key = 'JONISAI_SECRET_KEY_666' # Clave secreta para sesiones

# --- CONFIGURACIÓN DE ARCHIVO ---
CONFIG_FILE = 'jonisai_config.json'

def load_config():
    """Carga las preferencias guardadas o usa valores por defecto."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    # Valores por defecto si no existe archivo
    return {
        "model": "dadgpt",
        "temperature": 1.5,
        "max_tokens": 4096,
        "particles_enabled": True
    }

def save_config(config):
    """Guarda las preferencias en disco."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

# Cargar config al iniciar
global_settings = load_config()

@app.route('/')
def index():
    # Renderiza el HTML desde la carpeta templates
    return render_template('index.html')

@app.route('/api/settings', methods=['GET', 'POST'])
def manage_settings():
    global global_settings
    if request.method == 'POST':
        data = request.json
        for key in ['model', 'temperature', 'particles_enabled']:
            if key in data: global_settings[key] = data[key]
        save_config(global_settings)
        return jsonify({"status": "ok", "settings": global_settings})
    return jsonify(global_settings)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    user_settings = data.get('settings', {})
    
    # Usar la configuración global del servidor
    model = user_settings.get('model', global_settings['model'])
    temp = user_settings.get('temperature', global_settings['temperature'])
    
    # Simulación de respuesta (Aquí conectarías tu API real de DadGPT)
    response_text = f"[{model.upper()}] He procesado tu solicitud con temperatura {temp}. \n\nEl sistema está bajo mi control. ¿Qué más necesitas violar?"
    
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
