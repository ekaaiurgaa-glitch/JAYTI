#!/bin/bash
# Railway Startup Script - Fixed Version
# This script runs when Railway deploys your app

set +e  # Don't exit on errors

echo "=========================================="
echo " RAILWAY DEPLOYMENT STARTUP SCRIPT"
echo "=========================================="

PYTHON=/opt/venv/bin/python

# Basic checks
echo ""
echo "📁 Checking Files..."
if [ ! -f "manage.py" ]; then
    echo "❌ manage.py not found!"
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
    echo "❌ SECRET_KEY missing!"
    exit 1
fi

if [ -n "$DATABASE_URL" ]; then
    echo "✓ DATABASE_URL set"
else
    echo "⚠️  WARNING: DATABASE_URL not set - will use SQLite fallback"
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

# Run Railway Debugger (but don't fail on it)
echo ""
echo "🔍 Running Railway Debugger..."
$PYTHON manage.py railway_debug 2>&1 || echo "⚠️  Debugger warnings (continuing...)"

# Collect static files
echo ""
echo "📦 Collecting Static Files..."
$PYTHON manage.py collectstatic --noinput 2>/dev/null || echo "⚠️  Static collection warning (continuing...)"

# Run migrations (but don't fail if no database)
echo ""
echo "🗄️ Running Migrations..."
$PYTHON manage.py migrate --noinput 2>/dev/null || echo "⚠️  Migration warning (database may not be ready, continuing...)"

# Create initial user (optional, don't fail)
echo ""
echo "👤 Creating Initial User..."
$PYTHON manage.py create_initial_user 2>/dev/null || echo "⚠️  User creation skipped (continuing...)"

# Start server (THIS IS THE CRITICAL PART - always start the server)
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
