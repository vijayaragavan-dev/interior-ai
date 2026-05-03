import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os
import requests
import base64


HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"


def get_hf_api_key():
    from dotenv import load_dotenv
    load_dotenv()
    return os.getenv('HUGGINGFACE_API_KEY')


COLOR_VALUES = {
    'purple luxury': (139, 92, 246),
    'grey modern': (107, 114, 128),
    'mint green': (110, 231, 183),
    'navy blue': (30, 58, 95),
    'terracotta': (224, 122, 95),
    'sage green': (156, 175, 136),
    'mustard yellow': (228, 180, 79),
    'blush pink': (244, 172, 183),
    'teal': (45, 139, 139),
    'charcoal': (55, 65, 81)
}


def load_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    return img


def apply_color_theme(image_path, color, output_path):
    img = load_image(image_path)
    h, w = img.shape[:2]
    
    color_key = color.lower()
    if color_key not in COLOR_VALUES:
        color_key = 'grey modern'
    
    b, g, r = COLOR_VALUES[color_key]
    
    overlay = np.zeros((h, w, 3), dtype=np.uint8)
    overlay[:] = (b, g, r)
    
    mask = np.zeros((h, w), dtype=np.uint8)
    
    height, width = h, w
    region_height = int(height * 0.6)
    region_top = int(height * 0.15)
    mask[region_top:region_top + region_height, :] = 255
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (51, 51))
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (31, 31), 0)
    
    alpha = 0.35
    
    blended = img.copy()
    for y in range(h):
        for x in range(w):
            if mask[y, x] > 0:
                weight = mask[y, x] / 255.0 * alpha
                blended[y, x] = (
                    int(img[y, x, 0] * (1 - weight) + overlay[y, x, 0] * weight),
                    int(img[y, x, 1] * (1 - weight) + overlay[y, x, 1] * weight),
                    int(img[y, x, 2] * (1 - weight) + overlay[y, x, 2] * weight)
                )
    
    cv2.imwrite(output_path, blended)
    return output_path


def adjust_brightness_contrast(image_path, output_path):
    img = load_image(image_path)
    
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    enhanced = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    
    brightness = 1.05
    enhanced = np.clip(enhanced * brightness, 0, 255).astype(np.uint8)
    
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * 0.1
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    
    sigma = 0.5
    final = cv2.addWeighted(enhanced, 1 - sigma, sharpened, sigma, 0)
    
    cv2.imwrite(output_path, final)
    return output_path


def highlight_wall_region(image_path, output_path):
    img = load_image(image_path)
    h, w = img.shape[:2]
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    edges = cv2.Canny(gray, 50, 150)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
    
    wall_mask = np.zeros((h, w), dtype=np.uint8)
    
    if lines is not None:
        vertical_lines = []
        horizontal_lines = []
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            
            if abs(angle) < 20:
                vertical_lines.append(line[0])
            elif abs(angle - 90) < 20:
                horizontal_lines.append(line[0])
        
        wall_region = np.zeros((h, w), dtype=np.uint8)
        
        top_region = int(h * 0.1)
        bottom_region = int(h * 0.85)
        wall_region[top_region:bottom_region, :] = 255
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
        wall_mask = cv2.morphologyEx(wall_region, cv2.MORPH_CLOSE, kernel)
    
    wall_mask = cv2.GaussianBlur(wall_mask, (15, 15), 0)
    
    wall_mask_3ch = cv2.merge([wall_mask, wall_mask, wall_mask])
    
    highlight = img.copy()
    highlight = np.clip(highlight * 1.1, 0, 255).astype(np.uint8)
    
    result = np.where(wall_mask_3ch > 127, highlight, img)
    
    cv2.imwrite(output_path, result)
    return output_path


def detect_room_features(image_path):
    img = load_image(image_path)
    h, w = img.shape[:2]
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    edges = cv2.Canny(gray, 50, 150)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=50, maxLineGap=10)
    
    features = {
        'has_windows': False,
        'has_doors': False,
        'has_shelves': False,
        'empty_walls': ['left', 'right', 'back'],
        'room_dimensions': {'width': w, 'height': h}
    }
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            
            if length > w * 0.3:
                if abs(y1 - y2) < 50:
                    features['has_windows'] = True
                    if 'left' in features['empty_walls']:
                        features['empty_walls'].remove('left')
            
            if length > h * 0.6 and abs(x1 - x2) < 50:
                features['has_doors'] = True
    
    edges_dilated = cv2.dilate(edges, None, iterations=2)
    contours, _ = cv2.findContours(edges_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 500 < area < 5000:
            x, y, cw, ch = cv2.boundingRect(cnt)
            if ch > cw * 2:
                features['has_shelves'] = True
                if 'back' in features['empty_walls']:
                    features['empty_walls'].remove('back')
                break
    
    return features


def apply_style_effects(image_path, style, output_path):
    img = load_image(image_path)
    
    if style.lower() == 'modern':
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * 0.15
        img = cv2.filter2D(img, -1, kernel)
        
    elif style.lower() == 'luxury':
        img = np.clip(img * 1.1, 0, 255).astype(np.uint8)
        bilateral = cv2.bilateralFilter(img, 9, 75, 75)
        img = cv2.addWeighted(img, 0.7, bilateral, 0.3, 0)
        
    elif style.lower() == 'minimal':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
    elif style.lower() == 'scandinavian':
        img = np.clip(img * 1.05 + 10, 0, 255).astype(np.uint8)
        
    elif style.lower() == 'industrial':
        img = cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)
    
    cv2.imwrite(output_path, img)
    return output_path


def process_room_image(image_path, color, style, output_path):
    temp_files = []
    
    temp_color = output_path.replace('.png', '_color.png')
    apply_color_theme(image_path, color, temp_color)
    temp_files.append(temp_color)
    
    temp_style = output_path.replace('.png', '_style.png')
    apply_style_effects(temp_color, style, temp_style)
    temp_files.append(temp_style)
    
    temp_brightness = output_path.replace('.png', '_bright.png')
    adjust_brightness_contrast(temp_style, temp_brightness)
    temp_files.append(temp_brightness)
    
    temp_wall = output_path.replace('.png', '_wall.png')
    highlight_wall_region(temp_brightness, temp_wall)
    temp_files.append(temp_wall)
    
    import shutil
    shutil.move(temp_wall, output_path)
    
    for temp_file in temp_files[:-1]:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    return output_path


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def decode_base64_to_image(base64_string, output_path):
    image_data = base64.b64decode(base64_string)
    with open(output_path, "wb") as f:
        f.write(image_data)
    return output_path


def generate_ai_design(image_path, color, style, output_path):
    api_key = get_hf_api_key()
    
    if not api_key:
        print("No HuggingFace API key found, using local processing")
        return process_room_image(image_path, color, style, output_path)
    
    prompt = (
        f"Interior of a small Indian room with brown tile flooring, "
        f"{color} accent wall, modern {style} design, "
        f"realistic lighting, practical furniture layout, "
        f"high quality photo, interior design visualization"
    )
    
    negative_prompt = (
        "blurry, low quality, distorted, cartoon, anime, "
        "abstract, text, watermark, signature"
    )
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": negative_prompt,
            "guidance_scale": 7.5,
            "num_inference_steps": 30
        }
    }
    
    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            image_data = response.content
            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"AI design generated successfully")
            return output_path
        else:
            print(f"HuggingFace API error: {response.status_code}, falling back to local processing")
            return process_room_image(image_path, color, style, output_path)
            
    except requests.exceptions.Timeout:
        print("API timeout, falling back to local processing")
        return process_room_image(image_path, color, style, output_path)
    except Exception as e:
        print(f"AI generation failed: {str(e)}, falling back to local processing")
        return process_room_image(image_path, color, style, output_path)