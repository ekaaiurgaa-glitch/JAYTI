#!/bin/bash
# Railway Startup Script for JAYTI Birthday App
# This runs at DEPLOY time, not build time

set -e

echo "========================================"
echo "  JAYTI RAILWAY DEPLOYMENT STARTUP"
echo "========================================"

# Find Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Python not found!"
    exit 1
fi

echo "Python: $PYTHON"
$PYTHON --version

echo ""
echo "📦 Collecting static files..."
$PYTHON manage.py collectstatic --noinput || echo "Static warning (non-fatal)"

echo ""
echo "🗄️ Running database migrations..."
$PYTHON manage.py migrate --noinput || {
    echo "Migration failed!"
    exit 1
}

echo ""
echo "👤 Creating initial user..."
$PYTHON manage.py create_initial_user || echo "User creation skipped"

echo ""
echo "========================================"
echo "  STARTING SERVER"
echo "========================================"

exec $PYTHON -m gunicorn jaytipargal.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --timeout 120
