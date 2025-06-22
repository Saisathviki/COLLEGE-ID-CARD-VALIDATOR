import base64
import json
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from schemas import ValidateIDRequest, ValidateIDResponse
import onnxruntime as ort
from ocr_validator import validate_id_card
from template_matcher import check_template
from decision import decide_label
from PIL import Image
import io
import numpy as np
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="College ID Validator")

@app.get("/")
def read_root():
    return {"message": "🎉 AI ID Card Validator is running!"}

def load_model():
    try:
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "model", "image_model.onnx"))
        session = ort.InferenceSession(model_path)
        logger.info("✅ ONNX Model loaded successfully")
        return session
    except Exception as e:
        logger.error(f"❌ Error loading ONNX model: {e}")
        raise RuntimeError(f"❌ Error loading ONNX model: {e}")

def load_json(path):
    try:
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), path)), "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"❌ Error loading {path}: {e}")
        raise RuntimeError(f"❌ Error loading {path}: {e}")

model_session = load_model()
config = load_json("config.json")
approved_colleges = load_json("approved_colleges.json")
class_names = config.get("class_names", ["genuine", "fake", "suspicious"])

def preprocess_image(pil_image):
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    img = pil_image.resize((224, 224), Image.Resampling.LANCZOS)
    img_array = np.array(img).astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img_array = (img_array - mean) / std
    img_array = np.transpose(img_array, (2, 0, 1))
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
    return img_array

def classify_image_onnx(pil_image, session, class_names):
    input_name = session.get_inputs()[0].name
    img_array = preprocess_image(pil_image)
    outputs = session.run(None, {input_name: img_array})
    scores = outputs[0][0]
    exp_scores = np.exp(scores - np.max(scores))
    probs = exp_scores / exp_scores.sum()
    pred_idx = np.argmax(probs)
    return class_names[pred_idx], float(probs[pred_idx])

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/version")
async def version():
    return {"version": "1.0.0"}

@app.post("/validate-id", response_model=ValidateIDResponse, response_model_exclude_none=True)
async def validate_id(request: ValidateIDRequest, background_tasks: BackgroundTasks):
    try:
        image_bytes = base64.b64decode(request.image_base64)
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image encoding or image data")

    try:
        validation_label, validation_score = classify_image_onnx(pil_image, model_session, class_names)
        ocr_result = validate_id_card(image_bytes, approved_colleges, config["ocr_min_fields"])
        template_match = check_template(image_bytes)
        label, status, reason = decide_label(validation_score, ocr_result, template_match, config["validation_threshold"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ValidateIDResponse(
        user_id=request.user_id,
        validation_score=validation_score,
        label=label,
        status=status,
        reason=reason,
        threshold=config["validation_threshold"]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
