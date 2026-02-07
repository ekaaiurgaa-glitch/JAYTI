#!/bin/bash
# Railway Startup Script for JAYTI Birthday App

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
echo "📦 Installing dependencies..."
pip install -r requirements.txt 2>&1 | tail -3

echo ""
echo "📦 Collecting static files..."
$PYTHON manage.py collectstatic --noinput 2>&1 || echo "Static warning"

echo ""
echo "🗄️ Checking migrations..."
$PYTHON manage.py showmigrations 2>&1 || echo "Could not show migrations"

echo ""
echo "🗄️ Running database migrations..."
$PYTHON manage.py migrate --noinput 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  Migration failed, trying with --run-syncdb..."
    $PYTHON manage.py migrate --run-syncdb --noinput 2>&1
fi

echo ""
echo "🗄️ Creating missing tables..."
$PYTHON manage.py migrate --fake-initial --noinput 2>&1 || echo "Fake initial skipped"

echo ""
echo "👤 Creating initial user..."
$PYTHON manage.py create_initial_user 2>&1 || echo "User exists"

echo ""
echo "========================================"
echo "  STARTING SERVER on port $PORT"
echo "========================================"

exec $PYTHON -m gunicorn jaytipargal.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --timeout 120 \
    --log-level info
