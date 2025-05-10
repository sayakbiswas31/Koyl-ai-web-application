
# 🥦 **Koyl AI: Nutrition Recommendation System**

## 📌 Overview

**Koyl AI** is a web application developed as an **internship test project** 🧑‍💻 to provide **personalized dietary recommendations** based on user-input **health problems** (e.g., high blood pressure, diabetes) and **allergies** (e.g., dairy, nuts).
It features a lightweight **text-matching recommendation engine** 🔍 and a **mock corpus** simulating peer-reviewed sources (PubMed, USDA FoodData Central, EatRight.org, Harvard Nutrition Source).

🚀 **Optimized for low-spec systems (4 GB RAM)**, it ensures a smooth, responsive UI and robust functionality while fulfilling all project requirements.

---

## ✨ Features

* 📝 **Input Form:** Enter health problems and allergies in dedicated text areas with a search button.
* 🤖 **Recommendation Engine:** Lightweight, keyword-based matching (supports synonyms like *“hypertension”* for *“high blood pressure”*).
* 💻 **Responsive UI:** Clean, user-friendly interface built using HTML, CSS, and JavaScript.
* 🚫 **Error Handling:** Client-side (JavaScript) & server-side (Flask) validation for invalid inputs.
* 📦 **Output Display:**


---

## 🛠️ Technologies Used

* 🔙 **Backend:** Flask (Python)
* 🎨 **Frontend:** HTML, CSS, JavaScript
* 🧠 **Recommendation Engine:** Pandas-based text matching (low-memory)
* 📚 **Data:** Mock corpus `corpus.json` with 6 sample entries
* 📦 **Dependencies:**

  ```
  flask==2.3.2  
  pandas==2.0.3  
  ```

---

## 💻 System Requirements

* 🧠 **RAM:** 4 GB minimum
* 💽 **Disk Space:** \~2 GB free
* 💻 **CPU:** Any modern processor
* 🐍 **Python:** 3.8 – 3.10
* 🌐 **Browser:** Chrome, Firefox, etc.
* 🖥️ **OS:** Windows, macOS, or Linux

---

## ⚙️ Setup Instructions

1. 🔁 **Clone or Create Directory:**

   ```bash
   git clone <repo_url>  # Or manually create 'koyl-ai' directory
   ```

   Ensure the following files are present:

   ```
   app.py  
   recommendation_engine.py  
   corpus.json  
   requirements.txt  
   templates/index.html  
   static/styles.css  
   static/script.js  
   ```

2. 🧪 **Set Up Virtual Environment:**

   ```bash
   cd koyl-ai  
   python -m venv venv  
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. 📦 **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. 🚀 **Run the Application:**

   ```bash
   python app.py
   ```

   Open 👉 [http://localhost:5000](http://localhost:5000)
   If port 5000 is in use, change `app.py` to `port=5001`.

---

## 🧪 Usage

1. Go to **[http://localhost:5000](http://localhost:5000)**
2. ✍️ Enter:

   * A **health problem** (e.g., "high blood pressure")
   * Any **allergies** (optional, e.g., "dairy")
3. 🔘 Click **"Get Recommendations"**
4. 📬 View:

   * ✅ **Recommendations:** Green box
   * ❌ **Errors:** Red box (e.g., empty input)
   * ⚠️ **Fallbacks:** Generic advice if no match found

---

## 🧾 Testing

Here are some test cases to try out:

| 🔢 Test | 🩺 Health Problem   | 🚫 Allergies | ✅ Expected Output                                   |
| ------- | ------------------- | ------------ | --------------------------------------------------- |
| 1       | high blood pressure | dairy        | Low-sodium diet, leafy greens, bananas (dairy-free) |
| 2       | diabetes            | nuts         | Quinoa, legumes, veggies (avoid nuts)               |
| 3       | hypertension        | nuts         | DASH diet, nut-free                                 |
| 4       | diabetic            | dairy        | Oats, whole grains, no dairy desserts               |
| 5       | high blood pressure | *(empty)*    | Sodium and potassium-rich diet                      |
| 6       | diabetes            | *(empty)*    | Low-glycemic & fiber-rich foods                     |

* ❌ **Error Case:** Empty health input → `"Error: Health problem is required."`
* ⚠️ **Non-Matching Input:** `"cholesterol, gluten"` → `"No specific recommendations found... Try a general diet..."`


---

## 📌 Notes

* ⚙️ **Optimization:** Uses a **lightweight Pandas-based** matcher (not RAG/transformers) due to system constraints.
* 📂 **Corpus:** Includes only 6 mock entries (high BP, diabetes + dairy/nuts).
* 🔄 **Fallbacks:** Provided when inputs don't match any corpus entries.

---

## 🌱 Future Improvements

* 🔬 Integrate real **PubMed** data using **Biopython**
* 🔡 Add **fuzzy matching** to handle typos
* 🧑‍🎨 Upgrade UI using **Bootstrap**
* 📈 Expand corpus with more conditions & allergies

---


