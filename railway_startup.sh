#!/bin/bash
# Railway Startup Script with Debugging
# This script runs when Railway deploys your app

set -e  # Exit on error

echo "=========================================="
echo "  RAILWAY DEPLOYMENT STARTUP SCRIPT"
echo "=========================================="

# Debug: Print environment info
echo ""
echo "📋 Environment Info:"
echo "  Python Version: $(python --version)"
echo "  Working Directory: $(pwd)"
echo "  PATH: $PATH"

# Debug: Check for critical files
echo ""
echo "📁 Checking Critical Files:"
if [ -f "manage.py" ]; then
    echo "  ✓ manage.py found"
else
    echo "  ✗ manage.py NOT FOUND!"
    exit 1
fi

if [ -f "requirements.txt" ]; then
    echo "  ✓ requirements.txt found"
else
    echo "  ✗ requirements.txt NOT FOUND!"
    exit 1
fi

# Debug: Check environment variables
echo ""
echo "🔐 Checking Environment Variables:"
if [ -n "$SECRET_KEY" ]; then
    echo "  ✓ SECRET_KEY is set"
else
    echo "  ⚠ SECRET_KEY is NOT set (will use default)"
fi

if [ -n "$DATABASE_URL" ]; then
    echo "  ✓ DATABASE_URL is set"
else
    echo "  ⚠ DATABASE_URL is NOT set (will use SQLite)"
fi

if [ -n "$GEMINI_API_KEY" ]; then
    echo "  ✓ GEMINI_API_KEY is set"
else
    echo "  ⚠ GEMINI_API_KEY is NOT set (AI chat will not work)"
fi

# Run Railway Debugger
echo ""
echo "🔍 Running Railway Deployment Debugger..."
python manage.py railway_debug || {
    echo ""
    echo "❌ Deployment checks failed! See errors above."
    exit 1
}

# Collect static files
echo ""
echo "📦 Collecting Static Files..."
python manage.py collectstatic --noinput --clear || {
    echo "⚠ Static collection had issues, continuing..."
}

# Run migrations
echo ""
echo "🗄️  Running Database Migrations..."
python manage.py migrate --noinput || {
    echo "❌ Migration failed!"
    exit 1
}

# Create initial user if needed
echo ""
echo "👤 Creating Initial User..."
python manage.py create_initial_user || {
    echo "⚠ Initial user creation had issues, continuing..."
}

# Final startup message
echo ""
echo "=========================================="
echo "  ✅ STARTUP COMPLETE - LAUNCHING APP"
echo "=========================================="
echo ""

# Start Gunicorn with logging
exec gunicorn jaytipargal.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --worker-class gthread \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --preload
