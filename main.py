import cv2
import re
import pytesseract
from langdetect import detect, detect_langs
from PIL import Image
import numpy as np
# Đặt đường dẫn tới Tesseract executable (nếu cần thiết, chỉ áp dụng cho Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ACER\Downloads\Thuctap\tesseract.exe'
def detect_language(text):
    try:
        langs = detect_langs(text)
        if langs:
            return [lang.lang for lang in langs]
        return None
    except:
        return None


def cropImage(img,contours):
    pickers = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w *h
        #Chỉ lấy khung lớn
        if(area>100000): 
           pickers.append([x,y,w,h])
    
    pickers = np.array(pickers) #chuyển về numpy để xử lý
    #khởi tạo các giá trị (mặc định là khung đầu)
    x = pickers[0][0]
    y = pickers[0][1]
    w= pickers[0][2]
    h = pickers[0][3]

    #Tìm x,y,w,h cho case nhiều khung trong hình
    if (pickers.shape[0]>1):
        for i in range(pickers.shape[0]):
            if (x > pickers[i][0]):
                x = pickers[i][0]
            if (y> pickers[i][1]):
                y = pickers[i][1]
            w += pickers[i][2]
            h += pickers[i][3]
    # Cắt hình ảnh theo khung hình chữ nhật
    cropped_img = img[y:y+h, x:x+w]
    pickers_list = tuple(map(tuple, pickers))
    return cropped_img, pickers_list

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
    # largest_contour = max(contours, key=cv2.contourArea)
    # Tìm khung hình chữ nhật bao quanh đường viền lớn nhất
    # x, y, w, h = cv2.boundingRect(largest_contour)
    # Cắt hình ảnh theo khung hình chữ nhật
    # cropped_img = img[y:y+h, x:x+w]
    
    # Cắt ảnh và lấy các contours trong ảnh đã cắt
    cropped_img, picked_contours = cropImage(img,contours)

    # Hiển thị kích thước của ảnh gốc
    height, width, _ = cropped_img.shape
    
    # Định nghĩa vùng cần cắt (bỏ phần dư ở phía dưới)
    # Giả sử bạn muốn cắt 100 pixel từ phía dưới, bạn có thể điều chỉnh giá trị này
    new_height = height - 150
    cropped_img_new = cropped_img[:new_height, :]
    
    # Lưu hình ảnh 
    output_path = 'cropped_image.png'
    cv2.imwrite(output_path, cropped_img_new)


    # Nhận diện văn bản sơ bộ để phát hiện ngôn ngữ
    preliminary_text = pytesseract.image_to_string(cropped_img_new, lang='eng')
    
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
    
    for contour in picked_contours:
        x, y, w, h = contour
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
    cv2.imshow('Detected Characters', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # cv2.imwrite('cropped_image.png', cropped_contour_img)
    
    return detected_text, ocr_langs_str

#Xử lý đoạn detected_text 
def formatText(detected_text):
    string = ''.join(detected_text) #Chuyển sang string
    ban_list = ['(Choose 1 answer)\n',"|","(Choose 1 answer)"] #List ký tự cần xóa
    answer_list = ['\nA','\nB','\nC','\nD'] #List đáp án

    for char in ban_list:
        if char in string:
            if char in string:
                string = string.replace(char, '') #xóa ký tự
    
    for char in answer_list:
        if char in string:
            if ('.' not in string[string.index(char)+2]):
                string = string.replace(string[string.index(char)+2],' ') #format đáp án

    if '\n\n' in string:
        string = string.replace('\n\n','\n') #Tránh cách 2 dòng

    return string.strip()

# Hàm xuất file txt
def writeTxt(text):
    with open("./text3.txt", "w",encoding="utf-8" ) as f: f.write(text)

############## Main ################  
# Đường dẫn tới hình ảnh cần xử lý
image_path = 'nhung_dang_hinh/3.jpg'
# image_path = 'processed_images/3_new.jpg'

# Nhận diện văn bản từ hình ảnh
detected_text, detected_languages = extract_text_from_image(image_path)
formatted_text = formatText(detected_text)

#Ghi kết quả vào file txt
writeTxt(formatted_text)

#In ra màn hình
print("Detected text:", detected_text)
print("\nDetected languages:", detected_languages)
print("\nCleaned text:",formatted_text)



