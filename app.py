from flask import Flask, request, jsonify, render_template
from models import db, Application

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database
with app.app_context():
    db.create_all()

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/screening')
def screening_page():
    return render_template('screening.html')

@app.route('/results')
def results_page():
    return render_template('results.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/apply', methods=['POST'])
def apply():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    domain = data.get('domain')
    duration = data.get('duration')

    if not all([name, email, domain, duration]):
        return jsonify({"error": "All fields are required"}), 400

    application = Application(name=name, email=email, domain=domain, duration=duration)
    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Application submitted successfully", "application_id": application.id}), 201

@app.route('/verify/<int:app_id>', methods=['GET'])
def verify(app_id):
    application = Application.query.get(app_id)
    if application:
        return jsonify({
            "name": application.name,
            "email": application.email,
            "domain": application.domain,
            "duration": application.duration
        })
    else:
        return jsonify({"error": "Application not found"}), 404

# Placeholder AI endpoints
@app.route('/api/analyze-speech', methods=['POST'])
def analyze_speech():
    # Mock simple analysis returning fluency between 0.4 and 0.95 depending on length
    file = request.files.get('audio')
    size = 0
    if file:
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
    fluency = max(0.4, min(0.95, (size / (1024*64)) + 0.6))
    return jsonify({ 'fluency': round(fluency, 2) })

@app.route('/api/analyze-emotion', methods=['POST'])
def analyze_emotion():
    # Mock calmness based on image size heuristic
    file = request.files.get('image')
    size = 0
    if file:
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
    calmness = max(0.4, min(0.95, 1.0 - (size / (1024*200)) ))
    return jsonify({ 'calmness': round(calmness, 2) })

@app.route('/api/generate-score', methods=['POST'])
def generate_score():
    data = request.get_json(force=True)
    speech = float(data.get('voiceScore', 0.7))
    memory = float(data.get('memoryScore', 0.7))
    emotion = float(data.get('emotionScore', 0.7))
    # Weighted aggregate: speech 35%, memory 40%, emotion 25%
    risk_inverse = (speech*0.35 + memory*0.40 + emotion*0.25)
    risk_score = max(0.0, min(1.0, 1.0 - risk_inverse))
    why = {
        'speech': 'Frequent pauses detected' if speech < 0.6 else 'Clear, fluent speech',
        'memory': 'Low recall accuracy' if memory < 0.6 else 'Good recall accuracy',
        'emotion': 'Signs of confusion or stress' if emotion < 0.6 else 'Calm and stable expressions'
    }
    result = {
        'speech': speech,
        'memory': memory,
        'emotion': emotion,
        'riskScore': risk_score,
        'why': why
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
