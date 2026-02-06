#!/bin/bash
# Railway Startup Script with Debugging
# This script runs when Railway deploys your app

# Don't exit on error - we want to see all errors
set +e

echo "=========================================="
echo "  RAILWAY DEPLOYMENT STARTUP SCRIPT"
echo "=========================================="

# Use virtual environment Python
PYTHON=/opt/venv/bin/python
PIP=/opt/venv/bin/pip

# Debug: Print environment info
echo ""
echo "📋 Environment Info:"
echo "  Python Version: $($PYTHON --version 2>&1)"
echo "  Working Directory: $(pwd)"
echo "  PATH: $PATH"
echo "  PORT: ${PORT:-'not set'}"

# Debug: Check for critical files
echo ""
echo "📁 Checking Critical Files:"
if [ -f "manage.py" ]; then
    echo "  ✓ manage.py found"
else
    echo "  ✗ manage.py NOT FOUND!"
    ls -la
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
    echo "  ✓ SECRET_KEY is set (length: ${#SECRET_KEY})"
else
    echo "  ⚠ SECRET_KEY is NOT set"
fi

if [ -n "$DATABASE_URL" ]; then
    echo "  ✓ DATABASE_URL is set"
else
    echo "  ⚠ DATABASE_URL is NOT set"
fi

if [ -n "$GEMINI_API_KEY" ]; then
    echo "  ✓ GEMINI_API_KEY is set"
else
    echo "  ⚠ GEMINI_API_KEY is NOT set"
fi

# Test Django import first
echo ""
echo "🐍 Testing Django Import..."
$PYTHON -c "import django; print(f'  ✓ Django {django.get_version()} imported')" 2>&1
if [ $? -ne 0 ]; then
    echo "  ✗ Django import failed!"
    exit 1
fi

# Test settings import
echo ""
echo "⚙️  Testing Settings Import..."
$PYTHON -c "import jaytipargal.settings; print('  ✓ Settings imported')" 2>&1
if [ $? -ne 0 ]; then
    echo "  ✗ Settings import failed!"
    $PYTHON -c "import jaytipargal.settings" 2>&1
    exit 1
fi

# Run Railway Debugger
echo ""
echo "🔍 Running Railway Deployment Debugger..."
$PYTHON manage.py railway_debug 2>&1
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Deployment checks failed! See errors above."
    exit 1
fi

# Collect static files
echo ""
echo "📦 Collecting Static Files..."
$PYTHON manage.py collectstatic --noinput --clear 2>&1
if [ $? -ne 0 ]; then
    echo "⚠ Static collection had issues, continuing..."
fi

# Run migrations
echo ""
echo "🗄️  Running Database Migrations..."
$PYTHON manage.py migrate --noinput 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Migration failed!"
    exit 1
fi

# Create initial user if needed
echo ""
echo "👤 Creating Initial User..."
$PYTHON manage.py create_initial_user 2>&1
if [ $? -ne 0 ]; then
    echo "⚠ Initial user creation had issues, continuing..."
fi

# Final startup message
echo ""
echo "=========================================="
echo "  ✅ STARTUP COMPLETE - LAUNCHING APP"
echo "=========================================="
echo ""

# Ensure PORT is set (Railway should set this automatically)
if [ -z "$PORT" ]; then
    echo "⚠️  PORT not set, using default 8080"
    PORT=8080
fi

echo "🌐 Starting Gunicorn on port $PORT"

# Start Gunicorn with logging
exec $PYTHON -m gunicorn jaytipargal.wsgi:application \
    --bind "0.0.0.0:$PORT" \
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
