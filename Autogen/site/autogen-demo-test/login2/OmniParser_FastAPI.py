from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, Response
import torch
from PIL import Image
import io
import base64
from utils import check_ocr_box, get_yolo_model, get_caption_model_processor, get_som_labeled_img
from typing import Optional
import argparse

import os
import uuid
from datetime import datetime

# Add at the top with other imports
OUTPUT_DIR = "output_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI(
    title="OmniParser API",
    description="API for GUI screen parsing tool"
)

# Initialize models and configurations
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Model paths
ICON_DETECT_MODEL = "weights/icon_detect_v1_5/model_v1_5.pt"
ICON_CAPTION_MODEL = "florence2"

# Initialize models globally
yolo_model = get_yolo_model(model_path=ICON_DETECT_MODEL)
if ICON_CAPTION_MODEL == 'florence2':
    caption_model_processor = get_caption_model_processor(
        model_name="florence2", 
        model_name_or_path="weights/icon_caption_florence"
    )
elif ICON_CAPTION_MODEL == 'blip2':
    caption_model_processor = get_caption_model_processor(
        model_name="blip2", 
        model_name_or_path="weights/icon_caption_blip2"
    )

@app.post("/process_image/")
async def process_image(
    file: UploadFile = File(...),
    box_threshold: float = 0.05,
    iou_threshold: float = 0.1,
    use_paddleocr: bool = False,
    imgsz: int = 1920,
    icon_process_batch_size: int = 64
):
    try:
        # Read and save the uploaded image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image_save_path = 'imgs/saved_image_demo.png'
        image.save(image_save_path)

        # Calculate box overlay ratio
        box_overlay_ratio = image.size[0] / 3200
        draw_bbox_config = {
            'text_scale': 0.8 * box_overlay_ratio,
            'text_thickness': max(int(2 * box_overlay_ratio), 1),
            'text_padding': max(int(3 * box_overlay_ratio), 1),
            'thickness': max(int(3 * box_overlay_ratio), 1),
        }

        # Process OCR
        ocr_bbox_rslt, is_goal_filtered = check_ocr_box(
            image_save_path,
            display_img=False,
            output_bb_format='xyxy',
            goal_filtering=None,
            easyocr_args={'paragraph': False, 'text_threshold': 0.9},
            use_paddleocr=use_paddleocr
        )
        text, ocr_bbox = ocr_bbox_rslt

        # Get labeled image and parsing results
        dino_labled_img, label_coordinates, parsed_content_list = get_som_labeled_img(
            image_save_path,
            yolo_model,
            BOX_TRESHOLD=box_threshold,
            output_coord_in_ratio=True,
            ocr_bbox=ocr_bbox,
            draw_bbox_config=draw_bbox_config,
            caption_model_processor=caption_model_processor,
            ocr_text=text,
            iou_threshold=iou_threshold,
            imgsz=imgsz,
            batch_size=icon_process_batch_size
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        output_filename = f"processed_{timestamp}_{unique_id}.png"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        output_image = Image.open(io.BytesIO(base64.b64decode(dino_labled_img)))
        output_image.save(output_path)

        # Format parsed content
        parsed_content = '\n'.join([
            f'type: {x["type"]}, content: {x["content"]}, interactivity: {x["interactivity"]}' 
            for x in parsed_content_list
        ])

        return JSONResponse(content={
            "image_path": output_path,
            "parsed_content": parsed_content,
            "label_coordinates": label_coordinates
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10440)