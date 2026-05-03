# 🏠 Interior AI – Smart Room Design for Indian Homes

An intelligent interior design web application that helps users visualize and plan room designs based on real-world constraints.

---

## 🚀 Project Overview

**Interior AI** is a smart system that allows users to upload a room image and receive:

* 🎨 Color-based design transformation
* 🧠 Practical layout suggestions
* 📺 Smart placement recommendations (TV, furniture)
* 🧊 Interactive 3D room preview

Unlike generic AI tools, this system focuses on **realistic and feasible design decisions**, especially for **Indian homes with limited space and existing structures**.

---

## ✨ Key Features

### 🖼️ Image-Based Design

* Upload your room image
* Apply themes like **Purple Luxury, Grey Modern**
* Visual transformation using image processing

---

### 🧠 Constraint-Aware Suggestions (USP)

* Detects practical limitations:

  * Existing shelves
  * Door positions
  * Empty wall areas
* Suggests realistic placements:

  * TV positioning
  * Lighting improvements
  * Wall usage

---

### 💰 Budget-Based Recommendations

* Low / Medium / High budget options
* Suggests cost-effective solutions

---

### 🧊 3D Room Preview

* Built using **Three.js**
* Visualize room layout interactively
* Rotate and zoom functionality

---

## 🏗️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### Image Processing

* OpenCV
* Pillow
* NumPy

### 3D Visualization

* Three.js

---

## 📁 Project Structure

```
interior-ai/
│
├── backend/
│   ├── app.py
│   ├── image_processor.py
│   ├── logic_engine.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── viewer3d.js
│
├── uploads/
├── outputs/
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/vijayaragavan-dev/interior-ai.git
cd interior-ai
```

---

### 2️⃣ Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

---

### 3️⃣ Run Server

```bash
python app.py
```

---

### 4️⃣ Open Application

Open in browser:

```
http://127.0.0.1:5000/
```

---

## 🧪 How It Works

1. Upload your room image
2. Select preferences (color, style, budget)
3. System processes image using OpenCV
4. Logic engine generates smart suggestions
5. Output includes:

   * Enhanced image
   * Design recommendations
   * 3D preview

---

## 🧠 Unique Selling Point (USP)

> This system is **constraint-aware**, meaning it does not generate unrealistic designs.
> It analyzes the room structure and provides **practical, implementable solutions**.

---

## 🔒 Security & Privacy

* No external APIs used
* Fully offline processing
* No user data stored

---

## 🚧 Future Improvements

* Automatic wall detection using AI
* Furniture recognition
* Mobile app version
* Advanced 3D modeling

---

## 👨‍💻 Author

**Vijayaragavan**
CSE Student | Full Stack Developer

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
