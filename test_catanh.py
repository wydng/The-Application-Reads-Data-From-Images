import cv2
import pytesseract
from PIL import Image
from langdetect import detect

# Đặt đường dẫn tới Tesseract executable (nếu cần thiết, chỉ áp dụng cho Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ACER\Downloads\Thuctap\tesseract.exe'

def detect_language(text):
    try:
        return detect(text)
    except:
        return None

def extract_text_from_image(image_path, lang='eng'):
    # Đọc hình ảnh
    img = cv2.imread(image_path)
    
    # Chuyển đổi hình ảnh sang grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Áp dụng ngưỡng để nhị phân hóa hình ảnh
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Tìm các đường viền trong hình ảnh
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Giả sử khung hình chữ nhật chứa nội dung chính là đường viền lớn nhất
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Tìm khung hình chữ nhật bao quanh đường viền lớn nhất
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Cắt hình ảnh theo khung hình chữ nhật
    cropped_img = img[y:y+h, x:x+w]
    
    # Lưu hình ảnh đã cắt (nếu cần)
    cv2.imwrite('cropped_image.png', cropped_img)
    
    # Nhận diện văn bản sơ bộ để phát hiện ngôn ngữ
    preliminary_text = pytesseract.image_to_string(cropped_img, lang='eng')
    
    # Phát hiện ngôn ngữ
    detected_lang_code = detect_language(preliminary_text)
    if detected_lang_code:
        lang_dict = {
            'vi': 'vie',
            'en': 'eng',
            'zh-cn': 'chi_sim',
            'zh-tw': 'chi_tra',
            'ja': 'jpn',
            'ko': 'kor'
        }
        ocr_lang = lang_dict.get(detected_lang_code, 'eng')
    else:
        ocr_lang = 'eng'  # Mặc định sử dụng tiếng Anh nếu không phát hiện được
    
    # Sử dụng pytesseract để nhận diện văn bản từ hình ảnh đã cắt với ngôn ngữ được phát hiện
    text = pytesseract.image_to_string(cropped_img, lang=ocr_lang)
    
    return text, ocr_lang

# Đường dẫn tới hình ảnh cần xử lý
image_path = 'nhung_dang_hinh/10.jpg'

# Nhận diện văn bản từ hình ảnh với phát hiện ngôn ngữ tự động
detected_text, detected_language = extract_text_from_image(image_path)
print("Detected text:", detected_text)
print("Detected language:", detected_language)
