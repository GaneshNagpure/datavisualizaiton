import pandas as pd
import json
from django.core.management.base import BaseCommand
from data_app.models import ExcelData  # Replace with your model name

class Command(BaseCommand):
    help = "Import data from Excel to the Django database and store as JSON."

    def handle(self, *args, **kwargs):
        file_path = "excel_files/Monthly Portfolio of Schemes (1).xlsx"
        
        # Load data from Excel, skipping first 3 rows
        df = pd.read_excel(file_path, skiprows=3)
        
        # Fill NaN with None to prepare for JSON conversion
        df = df.where(pd.notnull(df), None)
        
        # Convert to JSON format from row 4 onward
        data_json = df.to_dict(orient="records")
        
        # Store each line as a JSON object in the database
        for record in data_json:
            data_object = ExcelData(data=json.dumps(record))
            data_object.save()
        
        self.stdout.write(self.style.SUCCESS("Data successfully imported and stored as JSON!"))
