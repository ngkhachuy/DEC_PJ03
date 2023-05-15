# DEC_PJ04_TIKI.VN

## DESCRIPTION

1. Lấy **toàn bộ** sản phẩm trên các danh mục của trang tiki.vn. Dữ liệu lấy về sẽ lưu trong MongoDB
2. Tạo một bản sao lưu data gửi cho Coach để có thể Restore dữ liệu trên một hệ thống MongoDB khác
3. Trích xuất các trường thông tin sau và lưu vào MySQL để cho team khác sử dụng:
    1. Product name: Tên sản phẩm 
    2. Short description: Mô tả ngắn của sản phẩm
    3. Description: Mô tả chi tiết sản phẩm, clean dữ liệu, lọc bỏ những tag html thừa trong mô tả
    4. URL: Link sản phẩm
    5. Rating: Đánh giá trung bình về sản phẩm
    6. Số lượng bán
    7. Giá sản phẩm
    8. Category ID: ID của danh mục sản phẩm
4. Thống kê:
    1. Mỗi category (bao gồm cả sub-category) có bao nhiêu sản phẩm
    2. Tạo biểu đồ thống kê xuất xứ của các sản phẩm. Ví dụ từ biểu đồ có thể biết: Có bao nhiêu sản phẩm xuất xứ từ Trung Quốc. Từ đó so sánh tỉ lệ xuất xứ của các sản phẩm
    3. Top 10 sản phẩm được bán nhiều nhất, có rating cao nhất và giá thấp nhất
5. Lấy tất cả sản phẩm mà có “thành phần” trong mô tả. Lưu các thông tin dưới dạng CSV: product_id, ingredient.
Lưu ý, chỉ trích chọn ra thông tin miêu tả “Thành phần” trong Description, những thông tin khác không lấy và Thời gian truy vấn ra các sản phẩm có “Thành phần” trong Description phải nhanh nhất có thể
6. Download **toàn bộ** ảnh ở “base_url” của mỗi sản phẩm về lưu trong ổ cứng (mỗi sản phẩm có từ 3-5 ảnh). Format tên ảnh: productID_number. Ví dụ tên ảnh thứ nhất của sản phẩm 180001095 sẽ là 180001095_1.png
7. Đưa ra idea cho leader về việc mình có thể làm gì tiếp theo với những dữ liệu này

## SOURCE

1. `get_categories.py` : Get all categories in TIKI
2. `normalize_categories` : Insert to Mysql and Normalize list of categories
3. `get_product_API.py` : Get products by API
4. `get_product.py` : Get products by Selenium and urllib3
5. `transfer_products.py` : Transfer products's data from MongoDB to MySQL
6. `download_images.py` : Download images of product
7. `COMMON.py` : Common function
8. `logging.log` : Log file of getting products
9. `logging_download_images.log` : log file of downloading images

10. `/data/DONE_CATEGORIES`
11. `/data/DONE_PRODUCT`