# from fastapi import FastAPI, HTTPException, File, UploadFile
# from pydantic import BaseModel
# from typing import List, Dict
# import json

# app = FastAPI()

# # Define the models
# class Annotation(BaseModel):
#     id: int
#     image_id: int
#     category_id: int
#     segmentation: List
#     area: float
#     bbox: List[float]
#     iscrowd: int
#     attributes: Dict

# class DataRequest(BaseModel):
#     annotations: List[Annotation]

# # Function to compute the desired statistics
# @app.post("/process-annotations")
# async def process_annotations(file: UploadFile = File(...)):
#     try:
#         data = json.loads(await file.read())
#         data_request = DataRequest(**data)
#     except json.JSONDecodeError:
#         raise HTTPException(status_code=400, detail="Invalid JSON format")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error decoding JSON: {e}")

#     # Count total annotations
#     total_annotations = len(data_request.annotations)

#     # Get distinct image ids with annotations
#     annotated_images = set(anno.image_id for anno in data_request.annotations)
#     total_annotated_images = len(annotated_images)

#     #Find repeated images
#     image_counts = {}
#     for anno in data_request.annotations:
#         image_counts[anno.image_id] = image_counts.get(anno.image_id, 0) + 1
#     repeated_images = {image_id: count for image_id, count in image_counts.items() if count > 1}
#     total_repeated_images = len(repeated_images)
    
#     return {
#         "total_annotations": total_annotations,
#         "total_annotated_images": total_annotated_images,
#         "repeated_images": repeated_images, "total_repeated_images":total_repeated_images
#     }


from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import json

# Define the models
class Annotation(BaseModel):
    id: int
    image_id: int
    category_id: int
    segmentation: List
    area: float
    bbox: List[float]
    iscrowd: int
    attributes: Dict

class DataRequest(BaseModel):
    annotations: List[Annotation]

# Create the FastAPI app instance
app = FastAPI()

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")


# Allow CORS for all origins or specify allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this to specific origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Function to compute the desired statistics
@app.post("/process-annotations")
async def process_annotations(file: UploadFile = File(...)):
    try:
        data = json.loads(await file.read())
        data_request = DataRequest(**data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error decoding JSON: {e}")

    # Count total annotations
    total_annotations = len(data_request.annotations)

    # Get distinct image ids with annotations
    annotated_images = set(anno.image_id for anno in data_request.annotations)
    total_annotated_images = len(annotated_images)

    #Find repeated images
    image_counts = {}
    for anno in data_request.annotations:
        image_counts[anno.image_id] = image_counts.get(anno.image_id, 0) + 1
    repeated_images = {image_id: count for image_id, count in image_counts.items() if count > 1}
    total_repeated_images = len(repeated_images)
    
    return {
        "total_annotations": total_annotations,
        "total_annotated_images": total_annotated_images,
        "repeated_images": repeated_images, "total_repeated_images": total_repeated_images
    }

#Default route
@app.get("/")
async def root():
    return {"message": "Welcome to the Annotation Statistics API!"}

