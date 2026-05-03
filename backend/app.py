import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS

from image_processor import process_room_image, detect_room_features
from logic_engine import generate_suggestions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, '..', 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(BASE_DIR, '..', 'outputs')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

CORS(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route('/generate', methods=['POST'])
def generate():
    try:
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image uploaded'
            }), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp'
            }), 400

        color = request.form.get('color', '').strip()
        style = request.form.get('style', '').strip()
        budget = request.form.get('budget', '').strip()

        if not color or not style or not budget:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: color, style, budget'
            }), 400

        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            features = detect_room_features(filepath)
        except Exception as e:
            features = {
                'has_windows': True,
                'has_doors': True,
                'has_shelves': False,
                'empty_walls': ['left', 'right'],
                'room_dimensions': {'width': 1200, 'height': 800}
            }

        output_filename = f"output_{uuid.uuid4()}.png"
        output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        try:
            process_room_image(filepath, color, style, output_filepath)
        except Exception as e:
            import shutil
            shutil.copy(filepath, output_filepath)

        suggestions = generate_suggestions(color, style, budget, features)

        return jsonify({
            'success': True,
            'image_url': f'/outputs/{output_filename}',
            'suggestions': suggestions,
            'features_detected': {
                'has_windows': features.get('has_windows', False),
                'has_doors': features.get('has_doors', False),
                'has_shelves': features.get('has_shelves', False),
                'empty_walls': features.get('empty_walls', [])
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/outputs/<path:filename>', methods=['GET'])
def get_output(filename):
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    return jsonify({'error': 'File not found'}), 404


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)