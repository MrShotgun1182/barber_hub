from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barbers', '0002_alter_workinghoursmodel_unique_together'),
        ('booking', '0002_remove_appointmentmodel_price_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='appointmentmodel',
            index=models.Index(
                fields=['barber', 'date', 'status'],
                name='appt_barber_date_status_idx',
            ),
        ),
    ]