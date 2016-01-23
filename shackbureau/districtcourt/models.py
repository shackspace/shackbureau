from django.db import models
from django.conf import settings

class Debitor(models.Model):
    class Meta:
        ordering = ('-created', )

    debitor_id = models.IntegerField(
        unique=True,
        help_text="Debitor ID")

    comment = models.TextField(
        blank=True,
        null=True)

    districtcourt = models.CharField(
        choices=(('reutlingen', 'Amtsgericht Reutlingen'), ),
        max_length=10,
        default="reutlingen",)

    date_of_receipt = models.DateField()

    record_token = models.CharField(
        max_length=255,
        help_text="Aktenzeichen")

    name = models.CharField(
        max_length=255,)

    debt_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,)

    due_date = models.DateField()

    is_done = models.BooleanField(
        default=False,)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def __str__(self):
        return "{}, {} [ID: {}]".format(self.name,
                                        self.record_token,
                                        self.debitor_id)

    def save(self, *args, **kwargs):
        if not self.debitor_id:
            self.debitor_id = (Debitor.objects.aggregate(models.Max('debitor_id'))
                               .get('debitor_id__max') or 0) + 1

        return super().save(*args, **kwargs)


