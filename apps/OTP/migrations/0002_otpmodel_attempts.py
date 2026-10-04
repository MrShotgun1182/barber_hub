from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OTP', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpmodel',
            name='attempts',
            field=models.PositiveSmallIntegerField(
                default=0, verbose_name='تعداد تلاش ناموفق'
            ),
        ),
    ]