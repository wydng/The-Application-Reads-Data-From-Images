import cv2
import re
import pytesseract
from langdetect import detect, detect_langs
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ACER\Downloads\Thuctap\tesseract.exe'

def detect_language(text):
    try:
        langs = detect_langs(text)
        if langs:
            return [lang.lang for lang in langs]
        return None
    except:
        return None

def extract_text_from_image(image_path, target_chars='ABCD'):
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
    detected_lang_codes = detect_language(preliminary_text)
    if detected_lang_codes:
        lang_dict = {
            'vi': 'vie',
            'en': 'eng',
            'zh-cn': 'chi_sim',
            'zh-tw': 'chi_tra',
            'ja': 'jpn',
            'ko': 'kor'
        }
        # Tạo danh sách các ngôn ngữ OCR từ các mã ngôn ngữ phát hiện được
        ocr_langs = [lang_dict.get(code, 'eng') for code in detected_lang_codes]
        ocr_langs_str = '+'.join(ocr_langs)
    else:
        ocr_langs_str = 'eng'  # Mặc định sử dụng tiếng Anh nếu không phát hiện được
    
    detected_text = []
    
    for contour in contours:
        # Tìm khung hình chữ nhật bao quanh đường viền
        x, y, w, h = cv2.boundingRect(contour)
        
        # Cắt hình ảnh theo khung hình chữ nhật
        cropped_contour_img = img[y:y+h, x:x+w]
        
        # Sử dụng pytesseract để nhận diện văn bản từ hình ảnh đã cắt
        text = pytesseract.image_to_string(cropped_contour_img, lang=ocr_langs_str)
        
        # Kiểm tra nếu văn bản chứa bất kỳ ký tự nào trong target_chars
        if any(char in text for char in target_chars):
            detected_text.append(text.strip())
            
            # Vẽ khung hình chữ nhật xung quanh các ký tự được phát hiện
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Hiển thị hình ảnh với các khung chữ nhật đã được vẽ (tùy chọn)
    # cv2.imshow('Detected Characters', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return detected_text, ocr_langs_str

# Đường dẫn tới hình ảnh cần xử lý
image_path = 'nhung_dang_hinh/1.jpg'
#image_folder = r'C:\Users\ACER\Downloads\Tool-to-separate-text-from-images-main\processed_images'

# Nhận diện văn bản từ hình ảnh
detected_text, detected_languages = extract_text_from_image(image_path)
print("Detected text:", detected_text)
print("Detected languages:", detected_languages)

#Xử lý đoạn detected_text 
def remove_extra_characters(text_list):
    cleaned_text_list = []
    for text in text_list:
        # Loại bỏ cụm từ
        text = re.sub(r'^FUOVERFLOW\.COM \|', '', text)
        text = re.sub(r'\(Choose 1 answer\)', '', text)
        
        # Loại bỏ các ký tự thừa
        #text = re.sub(r"[^\w\s()\-+?.:[]]", "", text)
        
        # Loại bỏ ký tự thừa
        text = re.sub(r"^\|", "", text)
        
        # Thay thế nhiều khoảng trắng bằng một khoảng trắng
        #text = re.sub(r"\s+", " ", text)  
        # Thêm vào danh sách đã làm sạch
        cleaned_text_list.append(text.strip())
    return cleaned_text_list

cleaned_text = remove_extra_characters(detected_text)
#biến danh sách các câu trả lời thành một chuỗi duy nhất mà mỗi câu trả lời được đặt trên một dòng riêng.
formatted_text = "\n".join(cleaned_text)
print("Cleaned text:", formatted_text)
#print("Answer: A")

