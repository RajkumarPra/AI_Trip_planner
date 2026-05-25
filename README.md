# AI Travel Planner ✈️

The **AI Travel Planner** is an intelligent, dynamic, and state-of-the-art web application designed to act as your personal travel concierge. By leveraging a powerful Agentic Workflow with Groq and a fast FastAPI backend, it provides curated travel itineraries instantly. The application features a premium dark-themed UI built from the ground up with HTML, Vanilla CSS, and JavaScript.

## ✨ Features

- **Intelligent Itinerary Generation:** Generates comprehensive travel plans based on origin, destination, and custom preferences.
- **Agentic AI Backend:** Powered by `Langgraph` and Groq LLMs.
- **Premium User Interface:** A highly interactive frontend utilizing glassmorphism, custom scrollbars, glowing gradients, and fluid layout structures.
- **Dynamic CSS Animations:** Features real-time visual route paths with continuously traveling animated vehicles (airplanes ✈️ and buses 🚌) across the screen.
- **Travel History Sidebar:** Automatically saves all your planned trips locally in your browser so you can access them instantly without re-fetching from the AI.
- **Skeleton Loading States:** A smooth and engaging loading experience featuring pulsing wireframes and cycling status texts while your itinerary is being generated.
- **Responsive Design:** Completely optimized for both desktop and mobile devices.

---

## 🚀 Installation & Setup

Follow these steps to run the AI Travel Planner on your local machine:

### 1. Clone the Repository
If you haven't already, navigate to your desired directory and clone/download this repository.

### 2. Set Up the Virtual Environment
Navigate to the root directory of the project (`AI_Trip_planner`) and ensure your virtual environment is set up.

If you don't have a virtual environment yet, create one:
```bash
python -m venv .venv
```

Activate the virtual environment:
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies
Install all the required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
You will need your API keys (like Groq) to enable the AI functionality.
Create a `.env` file in the root directory (or use the existing one) and add your keys:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application
Start the FastAPI backend server using Uvicorn. The server must be running to process requests and serve the custom UI.
```bash
uvicorn main:app --reload
```

### 6. Open in Browser
Once the server indicates `Application startup complete`, open your favorite web browser and go to:
[http://localhost:8000/app](http://localhost:8000/app)

---

## 🛠️ Architecture

- **Backend:** `FastAPI` serves both the API endpoints (`/query`) and the static frontend UI (`/app`).
- **AI Agent:** A sophisticated graph builder (`agent.agentic_workflow.GraphBuilder`) manages the conversational flow and information retrieval.
- **Frontend:** Vanilla HTML5, CSS3, and JavaScript ES6 located in the `/static` directory. Uses `marked.js` to parse AI markdown responses into beautiful HTML structures.

---

*Enjoy planning your next adventure!* 🌟
