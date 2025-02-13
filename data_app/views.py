import pandas as pd
import json
from django.http import JsonResponse
from data_app.models import ExcelData  # Replace with your actual model name

def import_excel_view(request):
    try:
        file_path = "excel_files/Monthly Portfolio of Schemes (1).xlsx"  # Ensure this path is correct
        # Load data from Excel, skipping the first 3 rows
        df = pd.read_excel(file_path, skiprows=3)
        
        # Fill NaN values with None for JSON compatibility
        df = df.where(pd.notnull(df), None)
        
        # Convert DataFrame to JSON records
        data_json = df.to_dict(orient="records")
        
        # Store each record as a JSON object in the database
        for record in data_json:
            ExcelData.objects.create(data=json.dumps(record))
        
        return JsonResponse({"status": "success", "message": "Excel data imported and stored as JSON!"} )
    
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


import pandas as pd
import json
from django.http import JsonResponse
from data_app.models import ExcelData  # Replace with your actual model name

def import_and_display_excel_view(request):
    try:
        file_path = "excel_files/Monthly Portfolio of Schemes (1).xlsx"  # Ensure this path is correct

        # Check if data already exists in the database to prevent duplication
        if ExcelData.objects.exists():
            data_list = [json.loads(record.data) for record in ExcelData.objects.all()]
            return JsonResponse({"status": "success", "message": "Data already exists!", "data": data_list}, safe=False)

        # Load data from Excel, skipping the first 3 rows
        df = pd.read_excel(file_path, skiprows=3)

        # Fill NaN values with None for JSON compatibility
        df = df.where(pd.notnull(df), None)

        # Convert DataFrame to JSON records
        data_json = df.to_dict(orient="records")

        # Store each record as a JSON object in the database
        for record in data_json:
            ExcelData.objects.create(data=json.dumps(record))

        # Return all stored data as a response
        data_list = [json.loads(record.data) for record in ExcelData.objects.all()]
        return JsonResponse({"status": "success", "message": "Excel data imported and stored as JSON!", "data": data_list}, safe=False)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
