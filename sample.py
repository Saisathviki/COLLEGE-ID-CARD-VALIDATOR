# from PIL import Image, ImageDraw, ImageFont, ImageFilter
# from faker import Faker
# import random, os

# # Setup
# fake = Faker()
# photo_dir = "photos"
# template_dir = "templates"
# output_base = "generated_ids"
# categories = ["genuine", "suspicious", "fake"]

# # Create output directories
# for category in categories:
#     os.makedirs(os.path.join(output_base, category), exist_ok=True)

# photo_files = sorted([f for f in os.listdir(photo_dir) if f.lower().endswith((".jpg", ".jpeg"))])
# template_files = sorted([f for f in os.listdir(template_dir) if f.lower().endswith((".jpg", ".jpeg"))])

# font_path = "C:\\Windows\\Fonts\\arial.ttf"
# font_path_comic = "C:\\Windows\\Fonts\\comic.ttf"  # For suspicious font style

# font_large = ImageFont.truetype(font_path, 34)
# font_medium = ImageFont.truetype(font_path, 28)
# font_suspicious = ImageFont.truetype(font_path_comic, 26)

# courses = ["CSD", "CSM", "CSBS", "ECE", "EEE", "IT", "CIVIL"]
# college_name = "VelTech Engineering College"

# def generate_roll():
#     return "22D21A" + str(random.randint(1000, 9999)).zfill(4)

# def fake_name():
#     return random.choice(["Elon Musk", "Mickey Mouse", "Naruto Uzumaki", "Iron Man", "Donald Duck"])

# def fake_course():
#     return random.choice(["Spy", "Wizard", "Time Travel", "Magic", "Dancing"])

# def fake_roll():
#     return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=10))

# # Your exact per-template layouts for genuine cards
# template_layouts = {
#     "template1.jpg": {
#         "orientation": "portrait",
#         "photo": (54, 230),
#         "text_start": (97, 542),
#         "line_gap": 40
#     },
#     "template2.jpg": {
#         "orientation": "landscape",
#         "photo": (127, 263),
#         "text_start": (470, 276),
#         "line_gap": 40
#     },
#     "template3.jpg": {
#         "orientation": "portrait",
#         "photo": (180, 224),
#         "text_start": (100, 547),
#         "line_gap": 40
#     },
#     "template4.jpg": {
#         "orientation": "landscape",
#         "photo": (79, 227),
#         "text_start": (405, 294),
#         "line_gap": 40
#     },
#     "template5.jpg": {
#         "orientation": "portrait",
#         "photo": (113, 198),
#         "text_start": (449, 392),
#         "line_gap": 40
#     }
# }

# def generate_id(i, category):
#     template_name = template_files[i % len(template_files)]
#     layout = template_layouts.get(template_name, template_layouts["template1.jpg"])

#     template_path = os.path.join(template_dir, template_name)
#     template = Image.open(template_path).convert("RGB")
#     draw = ImageDraw.Draw(template)

#     photo_size = (250, 250)

#     # Genuine
#     if category == "genuine":
#         name = fake.name().upper()
#         roll_no = generate_roll()
#         course = random.choice(courses)
#         font_name = font_large
#         font_info = font_medium

#         photo_path = os.path.join(photo_dir, photo_files[i % len(photo_files)])
#         student_photo = Image.open(photo_path).resize(photo_size)

#     # Suspicious
#     elif category == "suspicious":
#         name = fake.name().capitalize()
#         base_roll = generate_roll()[:-1]
#         roll_no = base_roll + random.choice("ABC")
#         course = random.choice(courses)
#         font_name = font_suspicious
#         font_info = font_suspicious

#         photo_path = os.path.join(photo_dir, photo_files[i % len(photo_files)])
#         student_photo = Image.open(photo_path).resize(photo_size)
#         student_photo = student_photo.filter(ImageFilter.GaussianBlur(radius=4))  # ✅ Blur applied properly

#     # Fake
#     else:
#         name = fake_name()
#         roll_no = fake_roll()
#         course = fake_course()
#         font_name = font_large
#         font_info = font_medium

#         student_photo = Image.new("RGB", photo_size, (
#             random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

#     # Paste photo
#     template.paste(student_photo, layout["photo"])

#     # Draw text
#     x, y = layout["text_start"]
#     draw.text((x, y), name, font=font_name, fill="black")
#     draw.text((x, y + layout["line_gap"]), f"Course    : {course}", font=font_info, fill="black")
#     draw.text((x, y + 2 * layout["line_gap"]), f"Roll No   : {roll_no}", font=font_info, fill="black")
#     draw.text((x, y + 3 * layout["line_gap"]), college_name, font=font_info, fill="black")

#     # Save
#     save_path = os.path.join(output_base, category, f"{category}_id_{i+1:03}.jpg")
#     template.save(save_path)

# # Generate 50 IDs per category
# for category in categories:
#     for i in range(50):
#         generate_id(i, category)

# print("✅ All IDs (genuine, suspicious, fake) generated with correct blur and layout!")
# from PIL import Image, ImageDraw, ImageFont, ImageFilter
# from faker import Faker
# import random, os
# import json

# # Setup
# fake = Faker()
# photo_dir = "photos"
# template_dir = "templates"
# output_base = "generated_ids"
# categories = ["genuine", "suspicious", "fake"]

# # Create output directories
# for category in categories:
#     os.makedirs(os.path.join(output_base, category), exist_ok=True)

# photo_files = sorted([f for f in os.listdir(photo_dir) if f.lower().endswith((".jpg", ".jpeg"))])
# template_files = sorted([f for f in os.listdir(template_dir) if f.lower().endswith((".jpg", ".jpeg"))])

# font_path = "C:\\Windows\\Fonts\\arial.ttf"
# font_path_comic = "C:\\Windows\\Fonts\\comic.ttf"  # For suspicious font style

# font_large = ImageFont.truetype(font_path, 34)
# font_medium = ImageFont.truetype(font_path, 28)
# font_suspicious = ImageFont.truetype(font_path_comic, 26)

# courses = ["CSD", "CSM", "CSBS", "ECE", "EEE", "IT", "CIVIL"]

# # Load approved college names
# with open("approved_colleges.json", "r") as f:
#     approved_colleges = json.load(f)

# def generate_roll():
#     return "22D21A" + str(random.randint(1000, 9999)).zfill(4)

# def fake_name():
#     return random.choice(["Elon Musk", "Mickey Mouse", "Naruto Uzumaki", "Iron Man", "Donald Duck"])

# def fake_course():
#     return random.choice(["Spy", "Wizard", "Time Travel", "Magic", "Dancing"])

# def fake_roll():
#     return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=10))

# # Your exact per-template layouts for genuine cards
# template_layouts = {
#     "template1.jpg": {"orientation": "portrait", "photo": (54, 230), "text_start": (97, 542), "line_gap": 40},
#     "template2.jpg": {"orientation": "landscape", "photo": (127, 263), "text_start": (470, 276), "line_gap": 40},
#     "template3.jpg": {"orientation": "portrait", "photo": (180, 224), "text_start": (100, 547), "line_gap": 40},
#     "template4.jpg": {"orientation": "landscape", "photo": (79, 227), "text_start": (405, 294), "line_gap": 40},
#     "template5.jpg": {"orientation": "portrait", "photo": (113, 198), "text_start": (449, 392), "line_gap": 40}
# }

# def generate_id(i, category):
#     template_name = template_files[i % len(template_files)]
#     layout = template_layouts.get(template_name, template_layouts["template1.jpg"])

#     template_path = os.path.join(template_dir, template_name)
#     template = Image.open(template_path).convert("RGB")
#     draw = ImageDraw.Draw(template)

#     photo_size = (250, 250)

#     # Genuine
#     if category == "genuine":
#         name = fake.name().upper()
#         roll_no = generate_roll()
#         course = random.choice(courses)
#         font_name = font_large
#         font_info = font_medium
#         college = approved_colleges[i % len(approved_colleges)]  # Unique college name

#         photo_path = os.path.join(photo_dir, photo_files[i % len(photo_files)])
#         student_photo = Image.open(photo_path).resize(photo_size)

#     # Suspicious
#     elif category == "suspicious":
#         name = fake.name().capitalize()
#         base_roll = generate_roll()[:-1]
#         roll_no = base_roll + random.choice("ABC")
#         course = random.choice(courses)
#         font_name = font_suspicious
#         font_info = font_suspicious
#         college = approved_colleges[i % len(approved_colleges)]  # Unique college name

#         photo_path = os.path.join(photo_dir, photo_files[i % len(photo_files)])
#         student_photo = Image.open(photo_path).resize(photo_size)
#         student_photo = student_photo.filter(ImageFilter.GaussianBlur(radius=4))  # ✅ Blur applied properly

#     # Fake
#     else:
#         name = fake_name()
#         roll_no = fake_roll()
#         course = fake_course()
#         font_name = font_large
#         font_info = font_medium
#         college = approved_colleges[i % len(approved_colleges)]  # Unique college name

#         student_photo = Image.new("RGB", photo_size, (
#             random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

#     # Paste photo
#     template.paste(student_photo, layout["photo"])

#     # Draw text
#     x, y = layout["text_start"]
#     draw.text((x, y), name, font=font_name, fill="black")
#     draw.text((x, y + layout["line_gap"]), f"Course    : {course}", font=font_info, fill="black")
#     draw.text((x, y + 2 * layout["line_gap"]), f"Roll No   : {roll_no}", font=font_info, fill="black")
#     draw.text((x, y + 3 * layout["line_gap"]), college, font=font_info, fill="black")

#     # Save
#     save_path = os.path.join(output_base, category, f"{category}_id_{i+1:03}.jpg")
#     template.save(save_path)

# # Generate 50 IDs per category
# for category in categories:
#     for i in range(50):
#         generate_id(i, category)

# print("✅ All IDs generated with unique approved college names!")
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from faker import Faker
import random, os
import json

# Setup
fake = Faker()
photo_dir = "photos"
template_dir = "templates"
output_base = "generated_ids"
categories = ["genuine", "suspicious", "fake"]

# Create output directories
for category in categories:
    os.makedirs(os.path.join(output_base, category), exist_ok=True)

photo_files = sorted([f for f in os.listdir(photo_dir) if f.lower().endswith((".jpg", ".jpeg"))])
template_files = sorted([f for f in os.listdir(template_dir) if f.lower().endswith((".jpg", ".jpeg"))])

font_path = "C:\\Windows\\Fonts\\arial.ttf"
font_path_comic = "C:\\Windows\\Fonts\\comic.ttf"  # For suspicious font style

font_large = ImageFont.truetype(font_path, 34)
font_medium = ImageFont.truetype(font_path, 28)
font_suspicious = ImageFont.truetype(font_path_comic, 26)

courses = ["CSD", "CSM", "CSBS", "ECE", "EEE", "IT", "CIVIL"]

# Load approved college names
with open("approved_colleges.json", "r") as f:
    approved_colleges = json.load(f)

def generate_roll():
    return "22D21A" + str(random.randint(1000, 9999)).zfill(4)

def fake_name():
    return random.choice(["Elon Musk", "Mickey Mouse", "Naruto Uzumaki", "Iron Man", "Donald Duck"])

def fake_course():
    return random.choice(["Spy", "Wizard", "Time Travel", "Magic", "Dancing"])

def fake_roll():
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=10))

# Your exact per-template layouts for genuine cards
template_layouts = {
    "template1.jpg": {"orientation": "portrait", "photo": (54, 230), "text_start": (97, 542), "line_gap": 40},
    "template2.jpg": {"orientation": "landscape", "photo": (127, 263), "text_start": (470, 276), "line_gap": 40},
    "template3.jpg": {"orientation": "portrait", "photo": (180, 224), "text_start": (100, 547), "line_gap": 40},
    "template4.jpg": {"orientation": "landscape", "photo": (79, 227), "text_start": (405, 294), "line_gap": 40},
    "template5.jpg": {"orientation": "portrait", "photo": (113, 198), "text_start": (449, 392), "line_gap": 40}
}

def generate_id(i, category):
    template_name = template_files[i % len(template_files)]
    layout = template_layouts.get(template_name, template_layouts["template1.jpg"])

    template_path = os.path.join(template_dir, template_name)
    template = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(template)

    photo_size = (250, 250)

    # Genuine
    if category == "genuine":
        name = fake.name().upper()
        roll_no = generate_roll()
        course = random.choice(courses)
        font_name = font_large
        font_info = font_medium
        college = approved_colleges[i % len(approved_colleges)]  # Unique college name

        photo_path = os.path.join(photo_dir, photo_files[i % len(photo_files)])
        student_photo = Image.open(photo_path).resize(photo_size)

    # Suspicious: Crop, screenshot, poor OCR, faker names
    elif category == "suspicious":
        name = fake.name().capitalize()  # Use faker names
        base_roll = generate_roll()[:-1]
        roll_no = base_roll + random.choice("ABC")
        
        # Simulate poor OCR for 20% of IDs (every 5th ID)
        if i % 5 == 0:
            name += str(random.randint(100, 999))  # Add noise for poor OCR
            roll_no += str(random.randint(10, 99))
            course = random.choice(courses) + str(random.randint(1, 9))
        else:
            course = random.choice(courses)
        
        font_name = font_suspicious
        font_info = font_suspicious
        college = approved_colleges[i % len(approved_colleges)]  # Unique college name

        photo_path = os.path.join(photo_dir, photo_files[i % len(photo_files)])
        student_photo = Image.open(photo_path).resize((int(photo_size[0] * 0.7), int(photo_size[1] * 0.7)))  # Crop to 70%
        student_photo = student_photo.filter(ImageFilter.GaussianBlur(radius=4))  # Blur face
        
        # Simulate screenshot for 20% of IDs (every 5th ID offset by 1)
        if i % 5 == 1:
            draw_grid = ImageDraw.Draw(template)
            for x in range(0, template.width, 20):
                for y in range(0, template.height, 20):
                    draw_grid.point((x, y), fill="gray")

    # Fake
    else:
        name = fake_name()
        roll_no = fake_roll()
        course = fake_course()
        font_name = font_large
        font_info = font_medium
        college = approved_colleges[i % len(approved_colleges)]  # Unique college name

        student_photo = Image.new("RGB", photo_size, (
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # Paste photo
    if category in ["genuine", "suspicious"]:
        template.paste(student_photo, (layout["photo"][0], layout["photo"][1], layout["photo"][0] + student_photo.width, layout["photo"][1] + student_photo.height))

    # Draw text (corrected font=font_info)
    x, y = layout["text_start"]
    draw.text((x, y), name, font=font_name, fill="black")
    draw.text((x, y + layout["line_gap"]), f"Course    : {course}", font=font_info, fill="black")
    draw.text((x, y + 2 * layout["line_gap"]), f"Roll No   : {roll_no}", font=font_info, fill="black")  # Fixed here
    draw.text((x, y + 3 * layout["line_gap"]), college, font=font_info, fill="black")

    # Save
    save_path = os.path.join(output_base, category, f"{category}_id_{i+1:03}.jpg")
    template.save(save_path)

# Generate 50 IDs per category
for category in categories:
    for i in range(50):
        generate_id(i, category)

print("✅ All IDs generated with unique approved college names, cropped/blurred suspicious IDs, screenshots, and poor OCR!")