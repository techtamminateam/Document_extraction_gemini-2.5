# api_server.py

import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse

from pipeline import main

# Utils mapping imports
from utils.data_points import (
    cyber_data_points,
    general_liability_data_points,
    business_owner_data_points,
    comercial_auto_data_points
)
from utils.queryy import (
    prompt_template_cyber,
    prompt_template_general,
    prompt_template_commercial_auto,
    prompt_template_general_liability,
    prompt_template_property,
    prompt_template_business_owner
)

app = FastAPI(title="Document Extraction API", version="1.0")


# ---------------- BUSINESS → TEMPLATE MAPS ----------------
prompt_map = {
    "cyber": prompt_template_cyber,
    "general": prompt_template_general,
    "comercial_auto": prompt_template_commercial_auto,
    "general_liability": prompt_template_general_liability,
    "property": prompt_template_property,
    "business_owner": prompt_template_business_owner,
    "package": prompt_template_business_owner
}

data_points_map = {
    "cyber": cyber_data_points,
    "general": business_owner_data_points,
    "comercial_auto": comercial_auto_data_points,
    "general_liability": general_liability_data_points,
    "property": cyber_data_points,
    "business_owner": business_owner_data_points,
    "package": business_owner_data_points
}


# ---------------- Extract Endpoint ----------------
@app.post("/extract")
async def extract_document(
    file: UploadFile = File(...),
    business: str = Form(...)
):
    try:
        if business not in data_points_map:
            return JSONResponse(
                {"error": f"Invalid business type: {business}"},
                status_code=400
            )

        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        # Call your pipeline
        result = main(temp_path, business, data_points_map, prompt_map)

        return {"status": "success", "data": result}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.get("/")
def home():
    return {"message": "API is running!"}
