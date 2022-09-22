from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    rating = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ], default=1)
    review = models.CharField(max_length=250)
    
    created_at = models.DateTimeField(auto_now_add=True)

    court = models.ForeignKey("courts.Court", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")