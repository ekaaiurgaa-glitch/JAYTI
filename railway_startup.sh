#!/bin/bash
# Railway Startup Script for JAYTI Birthday App
# Handles database migrations, static files, and user creation

set -e  # Exit on error

echo "========================================"
echo "  JAYTI RAILWAY DEPLOYMENT STARTUP"
echo "========================================"

# Set Python path
PYTHON=/opt/venv/bin/python

echo ""
echo "📦 Step 1: Collecting static files..."
$PYTHON manage.py collectstatic --noinput --clear 2>&1 || {
    echo "⚠️  Static collection warning (non-fatal)"
}

echo ""
echo "🗄️  Step 2: Running database migrations..."
$PYTHON manage.py migrate --noinput 2>&1 || {
    echo "❌ Migration failed! Attempting to diagnose..."
    $PYTHON manage.py showmigrations 2>&1 || echo "Cannot show migrations"
    exit 1
}

echo ""
echo "✅ Step 3: Verifying database connection..."
$PYTHON -c "
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('SELECT COUNT(*) FROM auth_user;')
    count = cursor.fetchone()[0]
    print(f'   Database connected. Users in database: {count}')
" 2>&1 || echo "⚠️  Could not verify user count"

echo ""
echo "👤 Step 4: Creating initial user (if needed)..."
$PYTHON manage.py create_initial_user 2>&1 || {
    echo "⚠️  User creation warning (may already exist)"
}

echo ""
echo "🔧 Step 5: Running deployment diagnostics..."
$PYTHON manage.py railway_debug 2>&1 || {
    echo "⚠️  Debug command not available (OK if new deployment)"
}

echo ""
echo "========================================"
echo "  STARTING GUNICORN SERVER"
echo "========================================"
echo "Port: $PORT"
echo "Workers: 2"
echo ""

# Start Gunicorn
exec $PYTHON -m gunicorn jaytipargal.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --threads 2 \
    --worker-class gthread \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance
