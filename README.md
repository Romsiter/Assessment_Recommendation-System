# Assessment Recommendation System

An AI-powered recommendation system to assist hiring managers in selecting relevant SHL assessments based on natural language job descriptions or URLs. It leverages semantic search and constraint-based filtering to provide highly accurate and tailored recommendations.

---

## 🚀 Features

- **Natural Language Processing:** Parses job descriptions and requirements.
- **Semantic Search:** Finds assessments closely matching job descriptions.
- **Constraint-Based Filtering:** Filters by duration, test type, remote support, and adaptive/IRT capabilities.
- **Interactive UI:** User-friendly frontend for quick querying.
- **RESTful API:** Simple endpoints for easy integration.

---

## 📌 Live Demo & API

- **Live Demo:** [Click here](https://your-demo-link.com)
- **API Endpoint:** [Click here](https://your-api-link.com)

*Note: Replace these dummy links with your actual deployment URLs.*

---

## 🛠 Architecture

The project comprises two main components:

### Backend (FastAPI)
- Computes semantic embeddings and queries FAISS for efficient retrieval.
- Applies filters based on constraints.
- Provides RESTful endpoints.

### Frontend (Streamlit)
- Collects job descriptions.
- Displays recommendations clearly in tabular format.

---

## 📦 Installation & Setup

### Prerequisites

- Python 3.8+
- Git

### Clone the Repository
```bash
git clone https://github.com/Romsiter/Assessment_Recommendation-System.git
cd Assessment_Recommendation-System
