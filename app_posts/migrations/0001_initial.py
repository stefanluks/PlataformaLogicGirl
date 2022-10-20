# Generated by Django 4.0.4 on 2022-10-19 23:27

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('classe', models.CharField(blank=True, choices=[('0', 'Autor'), ('1', 'Editor'), ('2', 'Gerente')], max_length=20, null=True, verbose_name='Classe do Usuario')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Publicacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150, verbose_name='Título da publicação')),
                ('resumo', models.TextField(blank=True, max_length=500, null=True, verbose_name='Resumo da publicação')),
                ('conteudo', models.TextField(blank=True, max_length=10000, null=True, verbose_name='Conteúdo [ HTML + Bootstrap ]')),
                ('tipo', models.CharField(blank=True, choices=[('0', 'POST'), ('1', 'JOGO')], default=('0', 'POST'), max_length=5, null=True, verbose_name='Tipo da Publicação')),
                ('status', models.CharField(blank=True, choices=[('0', 'salvo'), ('1', 'revisão'), ('2', 'revisado'), ('3', 'publicado')], default=('0', 'salvo'), max_length=15, null=True, verbose_name='Status da Publicação')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_posts.usuario')),
            ],
            options={
                'verbose_name': 'Publicação',
                'verbose_name_plural': 'Publicações',
            },
        ),
    ]
