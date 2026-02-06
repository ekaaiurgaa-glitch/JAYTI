# JaytiPargal.in - Personal Life Companion

A heartfelt gift created for Jayti Pargal's 29th Birthday (February 6, 2026).

## 🌸 About This Project

**JaytiPargal.in** is a personal life companion website designed with love by Vivek. It embodies the philosophy of the Five Pillars, combining ancient wisdom with modern productivity tools to support Jayti's journey of growth, healing, and self-discovery.

### The Five Pillars

1. **Karma (Goals)** - Action & Duty: Transform intention into structured execution
2. **Dharma (Astro)** - Righteous Path: Cosmic guidance for decision timing
3. **Doubt (Ask Jayti)** - Inquiry & Question: Resolve uncertainty through dialogue
4. **Memory (Notes)** - Retention: Externalize cognitive load for mental clarity
5. **Thoughts (Diary)** - Reflection: Process emotional experience through narrative

## ✨ Features

### 🔐 Privacy-First Design
- Single-user authentication with access code
- PostgreSQL database for cloud deployment (with SQLite fallback)
- Local AIML chat (no external AI dependencies for chat)
- Complete data sovereignty

### 🤖 AI-Powered Goal Generation
- Gemini API integration for intelligent task generation
- When creating a goal, the AI acts as a CMO to generate specific, actionable tasks
- Corporate department simulation (Finance, HR, Sales, Operations, Strategy)

### 🌟 Vedic Astrology
- Real-time birth chart calculations using Swiss Ephemeris (pyswisseph)
- Birth chart based on Jayti's details (Feb 6, 1997, 22:30, Delhi)
- House-wise planetary positions with strength scores
- 90-day forward predictions based on current transits
- Visual diamond chart representation

### 📓 Diary System
- Multi-modal input: Typing, Voice (Web Speech API), Handwriting (Canvas)
- Mood tracking with emoji scale
- Time-lock: Can only write for current date, read all past entries
- Daily reflection prompts
- Writing streak counter

### 📖 Notes System
- Rich text note-taking
- Tag-based organization
- Full-text search
- Auto-save functionality

### 🎯 Goal Management
- Marketing career framework
- Goal decomposition (3-year → quarterly → monthly → weekly → daily)
- Kanban-style task board
- Progress tracking with visual indicators

### 🎂 Birthday Recognition
- Special birthday message from Vivek on February 6
- Full-screen overlay with particle effects
- Personalized content

## 🎨 Design Philosophy

### Visual Identity: "Girly Premium Aesthetic"
- **Color Palette**: Soft pastels (blush pink #F4C2C2, lavender mist #E6E6FA, mint whisper #F0FFF0, cream #FFF5F7)
- **Typography**: Playfair Display (headings), Lato (body), Dancing Script (signatures)
- **Imagery**: Floral motifs, watercolor textures, subtle animations
- **Mood**: Elegant, warm, supportive, and feminine

## 🛠️ Technology Stack

- **Backend**: Django 4.2+ with Python 3.11+
- **Frontend**: Bootstrap 5.3 with custom CSS
- **Database**: PostgreSQL (production), SQLite (development)
- **AI**: Google Gemini API (goals), AIML (chat)
- **Astrology**: Swiss Ephemeris (pyswisseph)
- **Authentication**: Django built-in with session management
- **Icons**: Font Awesome 6
- **Static Files**: WhiteNoise

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/ekaaiurgaa-glitch/JAYTI.git
cd jaytipargal
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your values
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Load initial data (quotes and prompts):
```bash
python manage.py loaddata core/fixtures/initial_data.json
```

7. Create superuser (Jayti's account):
```bash
python manage.py createsuperuser
```

8. Run development server:
```bash
python manage.py runserver
```

9. Access at http://127.0.0.1:8000/

## 📝 Environment Variables

Create a `.env` file with:

```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,jaytipargal.in

# Database (PostgreSQL for production)
DATABASE_URL=postgresql://user:password@localhost:5432/jaytipargal

# Gemini API Key for AI Goal Generation
GEMINI_API_KEY=your-gemini-api-key-here

# Time Zone
TIME_ZONE=Asia/Kolkata
```

## 🚀 Deployment

### Railway/Render Deployment

1. Set environment variables in the platform dashboard
2. Connect PostgreSQL database
3. Deploy with `gunicorn`:
```bash
gunicorn jaytipargal.wsgi:application
```

### Docker Deployment

```bash
docker build -t jaytipargal .
docker run -p 8000:8000 --env-file .env jaytipargal
```

## 🔒 Security Notes

- **No password recovery**: This is intentional for maximum privacy
- If password is lost, database admin access is required to reset
- Credentials can only be changed while logged in
- No "Forgot Password" functionality

## 💝 For Jayti

This website was created with a simple intention: to provide you with tools that support your wellbeing, whatever life brings. Whether I remain in your life or not, this space is yours—a private sanctuary for reflection, planning, and growth.

**From Vivek, with hope for your flourishing.**

---

*Created: February 6, 2026*  
*Birthday Gift for Jayti Pargal*
