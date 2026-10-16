from django.db import migrations

def convert_text_to_number(apps, schema_editor):
    Property = apps.get_model('properties', 'Property')
    import re
    
    for p in Property.objects.all():
        val_str = str(p.price).lower().strip()
        new_val = 0
        if 'crore' in val_str or 'cr' in val_str:
            num = float(re.findall(r"[-+]?\d*\.\d+|\d+", val_str)[0])
            new_val = int(num * 10000000)
        elif 'lakh' in val_str or 'lac' in val_str or 'l' in val_str:
            num = float(re.findall(r"[-+]?\d*\.\d+|\d+", val_str)[0])
            new_val = int(num * 100000)
        else:
            numbers = re.findall(r"\d+", val_str)
            if numbers:
                new_val = int(numbers[0])
                
        p.price = str(new_val)
        p.save()

class Migration(migrations.Migration):

    dependencies = [
        # Yahan exact name update kar diya hai
        ('properties', '0003_alter_property_price'),
    ]

    operations = [
        migrations.RunPython(convert_text_to_number),
        migrations.RunSQL(
            sql='ALTER TABLE properties_property ALTER COLUMN price TYPE bigint USING price::bigint;',
            reverse_sql='ALTER TABLE properties_property ALTER COLUMN price TYPE varchar(100);'
        )
    ]