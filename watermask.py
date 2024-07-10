import os
import numpy as np
import cv2

# # path_image = 'nhung_dang_hinh/10.jpg'
# # img = cv2.imread(path_image)

# # # alpha = 2.596594846224838
# # alpha = 1.99
# # # alpha=2.8
# # beta = -179

# # new_img = alpha * img + beta
# # new_img = np.clip(new_img, 0, 255).astype(np.uint8)
# # cv2.imwrite("remove.png", new_img)
#===============================================================

# Directory containing the images
folder_path = 'ACC101'

# Parameters for brightness and contrast adjustment
alpha = 1.99
beta = -179

# Ensure the output directory exists
output_folder = 'ACC101_processed_images'
os.makedirs(output_folder, exist_ok=True)

# Process each image in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Construct the full path to the image
        img_path = os.path.join(folder_path, filename)
        
        # Read the image
        img = cv2.imread(img_path)
        
        # Adjust the image
        new_img = alpha * img + beta
        new_img = np.clip(new_img, 0, 255).astype(np.uint8)
        
        # Construct the new filename
        base, ext = os.path.splitext(filename)
        new_filename = f"{base}_new{ext}"
        new_img_path = os.path.join(output_folder, new_filename)
        
        # Save the new image
        cv2.imwrite(new_img_path, new_img)

print("Processing complete.")


import cv2

# Đọc hình ảnh từ tệp
image_path = '/mnt/data/cropped_image_new.png'
img = cv2.imread(image_path)

# Hiển thị kích thước của ảnh gốc
height, width, _ = img.shape
print(f'Original Dimensions: {width}x{height}')

# Định nghĩa vùng cần cắt (bỏ phần dư ở phía dưới)
# Giả sử bạn muốn cắt 100 pixel từ phía dưới, bạn có thể điều chỉnh giá trị này
new_height = height - 100
cropped_img = img[:new_height, :]

# Hiển thị kích thước của ảnh đã được cắt
new_height, new_width, _ = cropped_img.shape
print(f'Cropped Dimensions: {new_width}x{new_height}')

# Lưu hình ảnh đã được cắt vào tệp mới
output_path = '/mnt/data/cropped_image_trimmed.png'
cv2.imwrite(output_path, cropped_img)

# Hiển thị ảnh đã được cắt (tùy chọn)
cv2.imshow('Cropped Image', cropped_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

