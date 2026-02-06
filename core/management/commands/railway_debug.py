"""
Railway Deployment Debug Command
Helps diagnose common deployment issues on Railway.app
"""

import os
import sys
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection, OperationalError, ProgrammingError
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Debug Railway deployment issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Attempt to fix common issues automatically',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('=' * 60))
        self.stdout.write(self.style.MIGRATE_HEADING('RAILWAY DEPLOYMENT DEBUG'))
        self.stdout.write(self.style.MIGRATE_HEADING('=' * 60))
        
        issues_found = []
        
        # 1. Check Environment Variables
        self.stdout.write('\n')
        self.stdout.write(self.style.HTTP_INFO('1. ENVIRONMENT VARIABLES'))
        self.stdout.write('-' * 40)
        
        critical_vars = ['SECRET_KEY', 'DATABASE_URL', 'DEBUG']
        for var in critical_vars:
            value = os.environ.get(var, 'NOT SET')
            if var == 'SECRET_KEY' and value != 'NOT SET':
                value = f"{value[:10]}..." if len(value) > 10 else "SET"
            elif var == 'DATABASE_URL' and value != 'NOT SET':
                # Mask password in DATABASE_URL
                value = value.split('@')[1] if '@' in value else 'SET (masked)'
            status = '✅' if value != 'NOT SET' else '❌'
            self.stdout.write(f"{status} {var}: {value}")
        
        # 2. Check Database Connection
        self.stdout.write('\n')
        self.stdout.write(self.style.HTTP_INFO('2. DATABASE CONNECTION'))
        self.stdout.write('-' * 40)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                self.stdout.write(self.style.SUCCESS(f'✅ Connected to PostgreSQL'))
                self.stdout.write(f'   Version: {version[:50]}...')
                
                # Check if tables exist
                cursor.execute("""
                    SELECT COUNT(*) FROM information_schema.tables 
                    WHERE table_schema = 'public';
                """)
                table_count = cursor.fetchone()[0]
                self.stdout.write(f'   Tables: {table_count}')
                
                if table_count == 0:
                    issues_found.append('No database tables - migrations needed')
                    self.stdout.write(self.style.ERROR('❌ No tables found! Run migrations.'))
                    
        except OperationalError as e:
            issues_found.append(f'Database connection failed: {e}')
            self.stdout.write(self.style.ERROR(f'❌ Connection failed: {e}'))
        except Exception as e:
            issues_found.append(f'Database error: {e}')
            self.stdout.write(self.style.ERROR(f'❌ Error: {e}'))
        
        # 3. Check Migrations
        self.stdout.write('\n')
        self.stdout.write(self.style.HTTP_INFO('3. MIGRATIONS STATUS'))
        self.stdout.write('-' * 40)
        
        try:
            from django.db.migrations.executor import MigrationExecutor
            executor = MigrationExecutor(connection)
            plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
            
            if plan:
                self.stdout.write(self.style.WARNING(f'⚠️  {len(plan)} pending migrations:'))
                for migration in plan:
                    self.stdout.write(f'   - {migration[0].app_label}.{migration[0].name}')
                issues_found.append(f'{len(plan)} pending migrations')
            else:
                self.stdout.write(self.style.SUCCESS('✅ All migrations applied'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Cannot check migrations: {e}'))
        
        # 4. Check Static Files
        self.stdout.write('\n')
        self.stdout.write(self.style.HTTP_INFO('4. STATIC FILES'))
        self.stdout.write('-' * 40)
        
        self.stdout.write(f'STATIC_URL: {settings.STATIC_URL}')
        self.stdout.write(f'STATIC_ROOT: {settings.STATIC_ROOT}')
        self.stdout.write(f'STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}')
        
        # Check if whitenoise is installed
        try:
            import whitenoise
            self.stdout.write(self.style.SUCCESS(f'✅ WhiteNoise installed (v{whitenoise.__version__})'))
        except ImportError:
            issues_found.append('WhiteNoise not installed')
            self.stdout.write(self.style.ERROR('❌ WhiteNoise not installed'))
        
        # Check static root exists
        if os.path.exists(settings.STATIC_ROOT):
            static_files = []
            for root, dirs, files in os.walk(settings.STATIC_ROOT):
                static_files.extend(files)
                if len(static_files) > 20:
                    break
            self.stdout.write(self.style.SUCCESS(f'✅ STATIC_ROOT exists ({len(static_files)}+ files)'))
        else:
            issues_found.append('STATIC_ROOT does not exist')
            self.stdout.write(self.style.ERROR(f'❌ STATIC_ROOT not found: {settings.STATIC_ROOT}'))
        
        # 5. Check Django Settings
        self.stdout.write('\n')
        self.stdout.write(self.style.HTTP_INFO('5. DJANGO SETTINGS'))
        self.stdout.write('-' * 40)
        
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        self.stdout.write(f'ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        
        # Check middleware
        has_whitenoise = any('whitenoise' in str(m).lower() for m in settings.MIDDLEWARE)
        if has_whitenoise:
            self.stdout.write(self.style.SUCCESS('✅ WhiteNoise middleware configured'))
        else:
            issues_found.append('WhiteNoise middleware missing')
            self.stdout.write(self.style.ERROR('❌ WhiteNoise middleware not found'))
        
        # 6. Check Installed Apps
        self.stdout.write('\n')
        self.stdout.write(self.style.HTTP_INFO('6. INSTALLED APPS'))
        self.stdout.write('-' * 40)
        
        required_apps = ['core', 'crispy_forms', 'crispy_tailwind']
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                self.stdout.write(self.style.SUCCESS(f'✅ {app}'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ {app} - MISSING'))
                issues_found.append(f'{app} not in INSTALLED_APPS')
        
        # 7. Check Templates
        self.stdout.write('\n')
        self.stdout.write(self.style.HTTP_INFO('7. TEMPLATES'))
        self.stdout.write('-' * 40)
        
        template_dirs = []
        for engine in settings.TEMPLATES:
            template_dirs.extend(engine.get('DIRS', []))
        
        self.stdout.write(f'Template directories: {len(template_dirs)}')
        for td in template_dirs:
            if os.path.exists(td):
                count = len([f for f in os.listdir(td) if f.endswith('.html')])
                self.stdout.write(self.style.SUCCESS(f'✅ {td} ({count} templates)'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ {td} (not found)'))
        
        # 8. Attempt fixes if requested
        if options['fix'] and issues_found:
            self.stdout.write('\n')
            self.stdout.write(self.style.MIGRATE_HEADING('=' * 60))
            self.stdout.write(self.style.MIGRATE_HEADING('ATTEMPTING FIXES'))
            self.stdout.write(self.style.MIGRATE_HEADING('=' * 60))
            
            for issue in issues_found:
                self.stdout.write(f'\nFixing: {issue}')
                
                if 'migrations' in issue.lower():
                    try:
                        self.stdout.write('Running migrations...')
                        call_command('migrate', verbosity=1)
                        self.stdout.write(self.style.SUCCESS('✅ Migrations completed'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'❌ Migration failed: {e}'))
                
                elif 'static' in issue.lower():
                    try:
                        self.stdout.write('Collecting static files...')
                        call_command('collectstatic', '--noinput', verbosity=1)
                        self.stdout.write(self.style.SUCCESS('✅ Static files collected'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'❌ Static collection failed: {e}'))
        
        # Summary
        self.stdout.write('\n')
        self.stdout.write(self.style.MIGRATE_HEADING('=' * 60))
        if issues_found:
            self.stdout.write(self.style.ERROR(f'ISSUES FOUND: {len(issues_found)}'))
            for issue in issues_found:
                self.stdout.write(self.style.ERROR(f'  • {issue}'))
            if not options['fix']:
                self.stdout.write('\nRun with --fix to attempt automatic fixes')
        else:
            self.stdout.write(self.style.SUCCESS('✅ ALL CHECKS PASSED'))
        self.stdout.write(self.style.MIGRATE_HEADING('=' * 60))
