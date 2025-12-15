from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>DevOps CI/CD Project - COMSATS</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; background: #f0f8ff; }
        .container { background: white; padding: 30px; border-radius: 15px; display: inline-block; box-shadow: 0 8px 16px rgba(0,0,0,0.1); max-width: 800px; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #e74c3c; font-size: 48px; margin: 20px 0; }
        .tech-list { text-align: left; display: inline-block; margin: 20px; font-size: 18px; }
        .tech-list li { margin: 12px 0; padding: 8px 15px; background: #ecf0f1; border-radius: 5px; }
        .status { color: #27ae60; font-weight: bold; font-size: 20px; margin: 20px 0; }
        .uni { color: #2c3e50; font-weight: bold; font-size: 18px; margin: 10px 0; }
        .course { color: #7f8c8d; font-size: 16px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 DevOps CI/CD Pipeline Project</h1>
        <h2>Visitor #{{count}}</h2>
        
        <div class="uni">COMSATS University Islamabad</div>
        <div class="course">CSC418 - DevOps & Cloud Computing</div>
        
        <p style="margin: 25px 0;">This application demonstrates a complete DevOps pipeline:</p>
        
        <ul class="tech-list">
            <li>✅ Stage 1: Code Fetch (GitHub → Jenkins)</li>
            <li>✅ Stage 2: Docker Image Creation & Push</li>
            <li>✅ Stage 3: Kubernetes Deployment</li>
            <li>✅ Stage 4: Prometheus/Grafana Monitoring</li>
        </ul>
        
        <div class="status">✅ Pipeline Status: All 4 Stages Completed Successfully</div>
        
        <p style="margin-top: 30px;">
            <strong>Submission Date:</strong> 16-12-2025<br>
            <strong>Student:</strong> [Your Name]<br>
            <strong>Instructor:</strong> Dr. Muhammad Imran
        </p>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    conn = sqlite3.connect('/data/visits.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS visits (id INTEGER PRIMARY KEY, count INTEGER)')
    
    c.execute('SELECT count FROM visits WHERE id=1')
    row = c.fetchone()
    
    if row:
        count = row[0] + 1
        c.execute('UPDATE visits SET count=? WHERE id=1', (count,))
    else:
        count = 1
        c.execute('INSERT INTO visits (id, count) VALUES (1, ?)', (count,))
    
    conn.commit()
    conn.close()
    return render_template_string(HTML, count=count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
