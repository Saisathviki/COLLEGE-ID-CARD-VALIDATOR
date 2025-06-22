import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import urllib.request
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure output directories exist
def ensure_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        return False

# Cropping function
def crop_image(input_path, output_path, crop_type):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = cv2.imread(input_path)
        if img is None:
            logger.error(f"Failed to load image: {input_path}")
            return False
        h, w = img.shape[:2]
        if crop_type == "top_15":
            img = img[int(h*0.15):, :]
        elif crop_type == "bottom_15":
            img = img[:int(h*0.85), :]
        elif crop_type == "left_10":
            img = img[:, int(w*0.1):]
        success = cv2.imwrite(output_path, img)
        logger.info(f"Saved cropped image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

# Screenshot simulation function
def simulate_screenshot(input_path, output_path, crop_type, border_thickness=5):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = cv2.imread(input_path)
        if img is None:
            logger.error(f"Failed to load image: {input_path}")
            return False
        h, w = img.shape[:2]
        img_with_border = cv2.copyMakeBorder(img, border_thickness, border_thickness,
                                             border_thickness, border_thickness,
                                             cv2.BORDER_CONSTANT, value=[0, 0, 0])
        if crop_type == "bottom_20":
            img_with_border = img_with_border[:int(h*0.8)+border_thickness, :]
        elif crop_type == "right_15":
            img_with_border = img_with_border[:, :int(w*0.85)+border_thickness]
        elif crop_type == "top_15":
            img_with_border = img_with_border[int(h*0.15)+border_thickness:, :]
        success = cv2.imwrite(output_path, img_with_border)
        logger.info(f"Saved screenshot image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

# Degradation function
def degrade_image(input_path, output_path, resize_dim=(480, 320), brightness_factor=0.9, jpeg_quality=60):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = cv2.imread(input_path)
        if img is None:
            logger.error(f"Failed to load image: {input_path}")
            return False
        img = cv2.resize(img, resize_dim)
        img = cv2.convertScaleAbs(img, alpha=brightness_factor, beta=0)
        noise = np.random.normal(0, 5, img.shape).astype(np.uint8)
        img = cv2.add(img, noise)
        success = cv2.imwrite(output_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
        logger.info(f"Saved degraded image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

# Poor OCR functions
def apply_blur(input_path, output_path, blur_radius=2):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = cv2.imread(input_path)
        if img is None:
            logger.error(f"Failed to load image: {input_path}")
            return False
        img = cv2.GaussianBlur(img, (blur_radius * 2 + 1, blur_radius * 2 + 1), 0)
        success = cv2.imwrite(output_path, img)
        logger.info(f"Saved blurred image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

def apply_low_contrast(input_path, output_path, contrast_factor=0.3):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = cv2.imread(input_path)
        if img is None:
            logger.error(f"Failed to load image: {input_path}")
            return False
        img = cv2.convertScaleAbs(img, alpha=contrast_factor, beta=0)
        success = cv2.imwrite(output_path, img)
        logger.info(f"Saved low contrast image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

# Fake Template functions
def apply_incorrect_font(input_path, output_path):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = Image.open(input_path).convert("RGBA")
        h, w = img.size
        draw = ImageDraw.Draw(img)
        overlay = Image.new("RGBA", (h, w), (255, 255, 0, 100))
        draw = ImageDraw.Draw(overlay)
        try:
            font = ImageFont.truetype("comic.ttf", 50)
        except:
            font = ImageFont.load_default()
        draw.text((w // 4, h // 4), "FAKE", fill=(255, 0, 0, 255), font=font)
        college_name_bbox = (50, 20, 300, 80)
        draw.rectangle(college_name_bbox, fill=(0, 0, 0, 200))
        draw.text((50, 30), "www.fakeuniversity.com", fill=(255, 255, 255, 255), font=font)
        for _ in range(20):
            x, y = np.random.randint(0, w), np.random.randint(0, h)
            draw.ellipse((x-10, y-10, x+10, y+10), fill=(0, 255, 0, 150))
        img = Image.alpha_composite(img, overlay)
        temp_path = "temp_fake.png"
        img.save(temp_path, "PNG")
        img_bgr = cv2.imread(temp_path)
        success = cv2.imwrite(output_path, img_bgr)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        logger.info(f"Saved incorrect font image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

def apply_missing_field(input_path, output_path):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = Image.open(input_path).convert("RGBA")
        h, w = img.size
        draw = ImageDraw.Draw(img)
        overlay = Image.new("RGBA", (h, w), (128, 0, 128, 100))
        draw = ImageDraw.Draw(overlay)
        roll_number_bbox = (50, 60, 200, 80)
        draw.rectangle(roll_number_bbox, fill=(255, 255, 255, 255))
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()
        draw.text((50, 60), "INVALID", fill=(255, 0, 0, 255), font=font)
        draw.text((w // 5, h // 5), "FAKE ID", fill=(0, 255, 255, 255), font=font)
        img = Image.alpha_composite(img, overlay)
        temp_path = "temp_fake.png"
        img.save(temp_path, "PNG")
        img_bgr = cv2.imread(temp_path)
        success = cv2.imwrite(output_path, img_bgr)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        logger.info(f"Saved missing field image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

def apply_wrong_logo(input_path, output_path):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = Image.open(input_path).convert("RGBA")
        h, w = img.size
        draw = ImageDraw.Draw(img)
        overlay = Image.new("RGBA", (h, w), (0, 255, 0, 100))
        draw = ImageDraw.Draw(overlay)
        logo_url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png"
        logo_path = "temp_logo.png"
        try:
            urllib.request.urlretrieve(logo_url, logo_path)
            logo = Image.open(logo_path).convert("RGBA").resize((50, 50))
        except:
            logo = Image.new("RGBA", (50, 50), (0, 0, 255, 255))
        logo_bbox = (10, 10, 60, 60)
        img.paste(logo, logo_bbox[:2], logo)
        if os.path.exists(logo_path):
            os.remove(logo_path)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        draw.text((w // 3, h // 3), "FAKE LOGO", fill=(255, 255, 255, 255), font=font)
        img = Image.alpha_composite(img, overlay)
        temp_path = "temp_fake.png"
        img.save(temp_path, "PNG")
        img_bgr = cv2.imread(temp_path)
        success = cv2.imwrite(output_path, img_bgr)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        logger.info(f"Saved wrong logo image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

def apply_mismatched_colors(input_path, output_path):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = Image.open(input_path).convert("RGBA")
        h, w = img.size
        draw = ImageDraw.Draw(img)
        overlay = Image.new("RGBA", (h, w), (255, 105, 180, 100))
        draw = ImageDraw.Draw(overlay)
        for y in range(h):
            color = (int(255 * (y/h)), 105, 180, 100)
            draw.line((0, y, w, y), fill=color)
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except:
            font = ImageFont.load_default()
        draw.text((w // 4, h // 4), "FAKE COLORS", fill=(0, 0, 0, 255), font=font)
        img = Image.alpha_composite(img, overlay)
        temp_path = "temp_fake.png"
        img.save(temp_path, "PNG")
        img_bgr = cv2.imread(temp_path)
        success = cv2.imwrite(output_path, img_bgr)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        logger.info(f"Saved mismatched colors image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

def apply_incorrect_layout(input_path, output_path):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = Image.open(input_path).convert("RGBA")
        h, w = img.size
        draw = ImageDraw.Draw(img)
        overlay = Image.new("RGBA", (h, w), (0, 0, 255, 100))
        draw = ImageDraw.Draw(overlay)
        face_bbox = (10, 70, 60, 120)
        face = img.crop(face_bbox)
        draw.rectangle(face_bbox, fill=(255, 255, 255, 255))
        img.paste(face, (10, h - 50))
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()
        draw.text((w // 5, h // 5), "WRONG LAYOUT", fill=(255, 255, 0, 255), font=font)
        img = Image.alpha_composite(img, overlay)
        temp_path = "temp_fake.png"
        img.save(temp_path, "PNG")
        img_bgr = cv2.imread(temp_path)
        success = cv2.imwrite(output_path, img_bgr)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        logger.info(f"Saved incorrect layout image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

def apply_fake_barcode(input_path, output_path):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = Image.open(input_path).convert("RGBA")
        h, w = img.size
        draw = ImageDraw.Draw(img)
        overlay = Image.new("RGBA", (h, w), (255, 165, 0, 100))
        draw = ImageDraw.Draw(overlay)
        qr_size = 50
        qr_code = np.random.randint(0, 2, (qr_size, qr_size), dtype=np.uint8) * 255
        qr_code = cv2.resize(qr_code, (50, 50), interpolation=cv2.INTER_NEAREST)
        qr_code = cv2.cvtColor(qr_code, cv2.COLOR_GRAY2BGR)
        qr_code_pil = Image.fromarray(qr_code).convert("RGBA")
        barcode_bbox = (w-60, h-60, w-10, h-10)
        img.paste(qr_code_pil, barcode_bbox[:2])
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        draw.text((w // 3, h // 3), "FAKE BARCODE", fill=(0, 255, 255, 255), font=font)
        img = Image.alpha_composite(img, overlay)
        temp_path = "temp_fake.png"
        img.save(temp_path, "PNG")
        img_bgr = cv2.imread(temp_path)
        success = cv2.imwrite(output_path, img_bgr)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        logger.info(f"Saved fake barcode image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

def apply_obvious_fake(input_path, output_path):
    if not os.path.exists(input_path):
        logger.error(f"Input image not found: {input_path}")
        return False
    try:
        img = Image.open(input_path).convert("RGBA")
        h, w = img.size
        draw = ImageDraw.Draw(img)
        overlay = Image.new("RGBA", (h, w), (255, 0, 0, 100))
        draw = ImageDraw.Draw(overlay)
        for _ in range(30):
            x, y = np.random.randint(0, w), np.random.randint(0, h)
            draw.ellipse((x-15, y-15, x+15, y+15), fill=(255, 255, 255, 150))
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        fake_website = "www.fakeidgenerator.com"
        text_bbox = draw.textbbox((0, 0), fake_website, font=font)
        text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        text_position = ((w - text_w) // 2, (h - text_h) // 2)
        draw.text(text_position, fake_website, fill=(255, 255, 255, 255), font=font)
        draw.text((w // 4, h // 4), "FAKE", fill=(0, 255, 255, 255), font=font)
        img = Image.alpha_composite(img, overlay)
        temp_path = "temp_fake.png"
        img.save(temp_path, "PNG")
        img_bgr = cv2.imread(temp_path)
        success = cv2.imwrite(output_path, img_bgr)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        logger.info(f"Saved obviously fake image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error processing {input_path}: {e}")
        return False

# Non-ID image generation
def generate_non_id(output_path, index):
    try:
        # Placeholder: Black image with text
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(img, f"Non-ID Image {index}", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        # Optional: Download meme (uncomment and provide valid URLs)
        # meme_urls = [
        #     "https://example.com/meme1.jpg",
        #     "https://example.com/meme2.jpg",
        #     # Add 6 more URLs
        # ]
        # if index <= len(meme_urls):
        #     urllib.request.urlretrieve(meme_urls[index-1], output_path)
        #     img = cv2.imread(output_path)
        #     if img is None:
        #         raise Exception("Failed to download meme")
        success = cv2.imwrite(output_path, img)
        logger.info(f"Saved non-ID image to {output_path}: {success}")
        return success
    except Exception as e:
        logger.error(f"Error generating non-ID image {output_path}: {e}")
        return False

# Create output directories
ensure_directory("tests/sample_inputs/suspicious")
ensure_directory("tests/sample_inputs/fake")

# Apply cropping to 3 cropped images
crop_image("tests/sample_inputs/genuine/clear_id1.jpg",
           "tests/sample_inputs/suspicious/cropped_id_amritha.jpg", "top_15")
crop_image("tests/sample_inputs/genuine/clear_id2.jpg",
           "tests/sample_inputs/suspicious/cropped_id_pune.jpg", "bottom_15")
crop_image("tests/sample_inputs/genuine/clear_id3.jpg",
           "tests/sample_inputs/suspicious/cropped_id_srm.jpg", "left_10")

# Apply screenshot effects to 3 screenshot images
simulate_screenshot("tests/sample_inputs/genuine/clear_id4.jpg",
                    "tests/sample_inputs/suspicious/screenshot_id_manipal.jpg", "bottom_20")
simulate_screenshot("tests/sample_inputs/genuine/clear_id5.jpg",
                    "tests/sample_inputs/suspicious/screenshot_id_thapar.jpg", "right_15")
simulate_screenshot("tests/sample_inputs/genuine/clear_id6.jpg",
                    "tests/sample_inputs/suspicious/screenshot_id_jadavpur.jpg", "top_15")

# Degrade selected cropped/screenshot images
degrade_image("tests/sample_inputs/suspicious/cropped_id_amritha.jpg",
              "tests/sample_inputs/suspicious/cropped_id_amritha_low.jpg")
degrade_image("tests/sample_inputs/suspicious/cropped_id_srm.jpg",
              "tests/sample_inputs/suspicious/cropped_id_srm_low.jpg")
degrade_image("tests/sample_inputs/suspicious/screenshot_id_jadavpur.jpg",
              "tests/sample_inputs/suspicious/screenshot_id_jadavpur_low.jpg")

# Generate 2 poor OCR images
apply_blur("tests/sample_inputs/genuine/clear_id7.jpg",
           "tests/sample_inputs/suspicious/poor_ocr_1.jpg")
apply_low_contrast("tests/sample_inputs/genuine/clear_id8.jpg",
                  "tests/sample_inputs/suspicious/poor_ocr_2.jpg")
apply_blur("tests/sample_inputs/suspicious/poor_ocr_5.jpg",
           "tests/sample_inputs/suspicious/poor_ocr_5.jpg")
# Generate 7 fake template images
apply_incorrect_font("tests/sample_inputs/genuine/clear_id1.jpg",
                     "tests/sample_inputs/fake/fake_template_1.jpg")
apply_missing_field("tests/sample_inputs/genuine/clear_id2.jpg",
                    "tests/sample_inputs/fake/fake_template_2.jpg")
apply_wrong_logo("tests/sample_inputs/genuine/clear_id3.jpg",
                 "tests/sample_inputs/fake/fake_template_3.jpg")
apply_mismatched_colors("tests/sample_inputs/genuine/clear_id4.jpg",
                        "tests/sample_inputs/fake/fake_template_4.jpg")
apply_incorrect_layout("tests/sample_inputs/genuine/clear_id5.jpg",
                       "tests/sample_inputs/fake/fake_template_5.jpg")
apply_fake_barcode("tests/sample_inputs/genuine/clear_id6.jpg",
                   "tests/sample_inputs/fake/fake_template_6.jpg")
apply_obvious_fake("tests/sample_inputs/genuine/clear_id7.jpg",
                   "tests/sample_inputs/fake/fake_template_7.jpg")

