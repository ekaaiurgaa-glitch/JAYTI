#!/bin/bash
set -e

echo "========================================"
echo "  JAYTI DEPLOYMENT STARTUP"
echo "========================================"

PYTHON=python3
if ! command -v $PYTHON &> /dev/null; then
    PYTHON=python
fi

cd /app 2>/dev/null || cd /workspace 2>/dev/null || true

echo "→ Installing dependencies..."
pip install -r requirements.txt -q

echo "→ Collecting static files..."
$PYTHON manage.py collectstatic --noinput --verbosity=0 2>/dev/null || true

echo "→ Running migrations..."
$PYTHON manage.py migrate --noinput --verbosity=1

echo "→ Creating superuser..."
$PYTHON manage.py create_initial_user 2>/dev/null || true

echo "→ Starting server..."
exec $PYTHON -m gunicorn jaytipargal.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --timeout 120
