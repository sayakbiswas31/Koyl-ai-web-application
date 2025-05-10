from flask import Flask, request, render_template
from recommendation_engine import generate_recommendations

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = None
    error = None
    
    if request.method == "POST":
        try:
            health_problem = request.form.get("health_problem", "").strip().lower()
            allergies = request.form.get("allergies", "").strip().lower()
            
            if not health_problem:
                error = "Health problem is required"
            else:
                query = f"Nutrition recommendations for {health_problem}"
                if allergies:
                    query += f" with {allergies} allergy"
                
                recommendations = generate_recommendations(query, health_problem, allergies)
        except Exception as e:
            error = f"Error: {str(e)}"
    
    return render_template("index.html", recommendations=recommendations, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
