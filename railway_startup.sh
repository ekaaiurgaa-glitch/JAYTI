#!/bin/bash
# Railway Startup Script - Root Directory Version
# This script runs from the repository root where manage.py is located

set +e  # Don't exit on errors

echo "=========================================="
echo " RAILWAY DEPLOYMENT STARTUP"
echo "=========================================="
echo "Working directory: $(pwd)"
echo "Listing files:"
ls -la

PYTHON=/opt/venv/bin/python

# Basic checks
echo ""
echo "📁 Checking Files..."
if [ ! -f "manage.py" ]; then
    echo "❌ manage.py not found in $(pwd)!"
    echo "Searching for manage.py..."
    find / -name "manage.py" -type f 2>/dev/null | head -5
    exit 1
fi
echo "✓ manage.py found"

echo "✓ Python: $($PYTHON --version 2>&1)"

# Check environment variables
echo ""
echo "🔐 Environment Check:"
if [ -n "$SECRET_KEY" ]; then
    echo "✓ SECRET_KEY set"
else
    echo "⚠️  WARNING: SECRET_KEY not set"
fi

if [ -n "$DATABASE_URL" ]; then
    echo "✓ DATABASE_URL set"
else
    echo "⚠️  WARNING: DATABASE_URL not set"
fi

if [ -n "$GEMINI_API_KEY" ]; then
    echo "✓ GEMINI_API_KEY set"
else
    echo "⚠️  WARNING: GEMINI_API_KEY not set"
fi

# Test Django imports
echo ""
echo "🐍 Testing Django..."
$PYTHON -c "import django; print(f'✓ Django {django.get_version()}')" || {
    echo "❌ Django import failed"
    exit 1
}

$PYTHON -c "import jaytipargal.settings; print('✓ Settings loaded')" || {
    echo "❌ Settings import failed"
    exit 1
}

# Collect static files
echo ""
echo "📦 Collecting Static Files..."
$PYTHON manage.py collectstatic --noinput 2>&1 || echo "⚠️  Static collection warning"

# Run migrations
echo ""
echo "🗄️ Running Migrations..."
$PYTHON manage.py migrate --noinput 2>&1 || echo "⚠️  Migration warning"

# Create initial user
echo ""
echo "👤 Creating Initial User..."
$PYTHON manage.py create_initial_user 2>&1 || echo "⚠️  User creation skipped"

# Start server
echo ""
echo "=========================================="
echo " 🚀 STARTING GUNICORN ON PORT ${PORT:-8080}"
echo "=========================================="

if [ -z "$PORT" ]; then
    PORT=8080
fi

# Use exec to replace shell with gunicorn
exec $PYTHON -m gunicorn jaytipargal.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --threads 4 \
    --worker-class gthread \
    --timeout 120 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
