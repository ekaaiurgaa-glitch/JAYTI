# Generated manually - Initial migration for goals app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role_category', models.CharField(choices=[('digital_marketing', 'Digital Marketing'), ('brand_management', 'Brand Management'), ('content_strategy', 'Content Strategy'), ('market_research', 'Market Research'), ('product_marketing', 'Product Marketing'), ('social_media', 'Social Media'), ('seo_sem', 'SEO/SEM'), ('marketing_analytics', 'Marketing Analytics')], max_length=50)),
                ('experience_level', models.CharField(choices=[('entry', 'Entry Level'), ('mid', 'Mid Level'), ('senior', 'Senior Level'), ('leadership', 'Leadership')], max_length=20)),
                ('time_horizon', models.CharField(choices=[('1year', '1 Year'), ('3year', '3 Years'), ('5year', '5 Years'), ('10year', '10 Years')], max_length=10)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('target_date', models.DateField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('paused', 'Paused'), ('archived', 'Archived')], default='active', max_length=20)),
                ('completion_percentage', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('department', models.CharField(choices=[('strategy', 'Strategy'), ('content', 'Content'), ('digital', 'Digital'), ('brand', 'Brand'), ('events', 'Events'), ('partnerships', 'Partnerships'), ('analytics', 'Analytics'), ('crm', 'CRM')], default='strategy', max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('target_date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('blocked', 'Blocked')], default='pending', max_length=20)),
                ('completion_percentage', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='goals.goal')),
            ],
        ),
    ]
