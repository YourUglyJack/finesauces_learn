from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('-name', )
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse("listings:product_list_by_category", args=[self.slug])

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)

    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    shu = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('shu', )

    def get_absolute_url(self):
        return reverse("listings:product_detail",
                       args=[self.category.slug, self.slug])  # pylint: disable=no-member

    def get_average_review_score(self):
        avg_score = 0
        if self.reviews.count() > 0:  # type: ignore # pylint: disable=no-member
            total_score = sum(review.rating for review in self.reviews.all())  # type: ignore # pylint: disable=no-member
            avg_score = total_score / self.reviews.count()  # type: ignore # pylint: disable=no-member
        return avg_score


class Review(models.Model):
    product = models.ForeignKey(Product,
                                related_name='reviews',
                                on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(5)])
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )
