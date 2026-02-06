# Generated manually - Initial migration for diary app

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
            name='DiaryEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('entry_date', models.DateField()),
                ('content', models.TextField(blank=True)),
                ('content_html', models.TextField(blank=True)),
                ('input_method', models.CharField(choices=[('type', 'Typing'), ('voice', 'Voice'), ('stylus', 'Stylus/Handwriting')], default='type', max_length=10)),
                ('voice_transcript', models.TextField(blank=True)),
                ('voice_duration', models.IntegerField(blank=True, null=True)),
                ('handwriting_strokes', models.JSONField(blank=True, null=True)),
                ('handwriting_ocr_text', models.TextField(blank=True)),
                ('handwriting_image', models.ImageField(blank=True, null=True, upload_to='diary/handwriting/')),
                ('mood', models.IntegerField(blank=True, choices=[(1, '😔 Struggling'), (2, '😕 Difficult'), (3, '😐 Neutral'), (4, '🙂 Good'), (5, '😊 Great')], null=True)),
                ('mood_note', models.CharField(blank=True, max_length=200)),
                ('prompt_used', models.CharField(blank=True, max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diary_entries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
