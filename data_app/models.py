from django.db import models
import json

class ExcelData(models.Model):
    data = models.TextField()  # Use TextField instead of JSONField
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure data is saved as a JSON string
        if isinstance(self.data, dict):
            self.data = json.dumps(self.data)
        super().save(*args, **kwargs)
