# Generated by Django 4.1.7 on 2023-03-16 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0002_alter_review_parent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Created datetime"
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="shop.product",
                verbose_name="Product",
            ),
        ),
        migrations.AlterField(
            model_name="productshot",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="shop.product",
                verbose_name="Product",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Created datetime"
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="name",
            field=models.CharField(max_length=30, verbose_name="Username"),
        ),
        migrations.AlterField(
            model_name="review",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="shop.review",
                verbose_name="Parent",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="shop.product",
                verbose_name="Product",
            ),
        ),
    ]
