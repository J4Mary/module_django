from datetime import datetime

from django.db import models

from store import settings

USER_MODEL = settings.AUTH_USER_MODEL


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(TimeStampModel):
    name = models.CharField(max_length=80)
    description = models.TextField()
    price = models.IntegerField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='product_images/')
    available = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.available = 0
        self.save()


class Purchase(TimeStampModel):
    buyer = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)
    is_active = models.NullBooleanField(default=True)

    def get_time_diff(self):
        now = datetime.timestamp(datetime.now())
        created_at = datetime.timestamp(self.created_at)
        return now - created_at


class Refund(TimeStampModel):

    IN_CONSIDERING = 1
    DECLINED = 2
    APPROVED = 3

    STATUSES = (
        (IN_CONSIDERING, 'NEW'),
        (DECLINED, 'DECLINED'),
        (APPROVED, 'APPROVED')
    )

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(choices=STATUSES)
