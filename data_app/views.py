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


from django.shortcuts import render
from django.db.models import Count
from data_app.models import ExcelData
import json

def top_industries_view(request):
    # Query to get the count of each industry
    industry_counts = (
        ExcelData.objects.values("data")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Extract industry names and counts
    industries = {}
    for record in industry_counts:
        data = json.loads(record["data"])  # Convert JSON string back to dict
        industry = data.get("Industry/Rating")
        if industry:
            industries[industry] = industries.get(industry, 0) + 1

    # Sort industries by count and get the top 5
    sorted_industries = sorted(industries.items(), key=lambda x: x[1], reverse=True)[:5]

    # Prepare data for the pie chart
    labels = [industry for industry, _ in sorted_industries]
    counts = [count for _, count in sorted_industries]

    return render(request, "chart.html", {"labels": labels, "counts": counts})
