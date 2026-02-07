#!/bin/bash
# Railway Startup Script for JAYTI Birthday App
# Runs at DEPLOY time (not build time)

set -e  # Exit on error

echo "========================================"
echo "  JAYTI RAILWAY DEPLOYMENT STARTUP"
echo "========================================"

# Detect Python path (works with Railway's Python setup)
if [ -d "/opt/venv" ]; then
    PYTHON=/opt/venv/bin/python
elif [ -f "/app/.venv/bin/python" ]; then
    PYTHON=/app/.venv/bin/python
elif command -v python3 &> /dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

echo "Using Python: $PYTHON"
$PYTHON --version

echo ""
echo "📦 Step 1: Collecting static files..."
$PYTHON manage.py collectstatic --noinput --clear 2>&1 || {
    echo "⚠️  Static collection warning (non-fatal)"
}

echo ""
echo "🗄️  Step 2: Running database migrations..."
$PYTHON manage.py migrate --noinput 2>&1 || {
    echo "❌ Migration failed!"
    exit 1
}

echo ""
echo "👤 Step 3: Creating initial user..."
$PYTHON manage.py create_initial_user 2>&1 || {
    echo "⚠️  User creation warning (may already exist)"
}

echo ""
echo "========================================"
echo "  STARTING GUNICORN SERVER"
echo "========================================"

# Start Gunicorn
exec $PYTHON -m gunicorn jaytipargal.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
