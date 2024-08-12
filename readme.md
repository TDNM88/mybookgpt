# AI Book Writer

AI Book Writer là một ứng dụng Streamlit cho phép bạn tạo ra nội dung sách dựa trên các yêu cầu cụ thể. Ứng dụng kết hợp sức mạnh của OpenAI GPT-4o mini và Groq API để tạo ra nội dung chi tiết và không bị giới hạn về độ dài.

## Tính năng chính
- Tạo outline sách dựa trên chủ đề và yêu cầu.
- Viết nội dung chi tiết cho từng chương.
- Kết hợp và mở rộng nội dung sách không giới hạn độ dài.
- Lưu và tải lại metadata của dự án để tiếp tục công việc.
- Xuất nội dung sách thành các định dạng khác nhau (TXT, DOCX, PDF).

## Cài đặt
1. Clone repo về máy của bạn:
   ```bash
   git clone https://github.com/yourusername/ai-book-writer.git
   cd ai-book-writer
   ```

2. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

3. Chạy ứng dụng:
   ```bash
   streamlit run main.py
   ```

## Cấu hình
Bạn có thể cấu hình API key và các cài đặt khác trong tệp `.streamlit/secrets.toml` hoặc bằng cách sử dụng các biến môi trường.

## Triển khai
Bạn có thể triển khai ứng dụng này trên Heroku, AWS, hoặc bất kỳ nền tảng nào hỗ trợ Python và Streamlit. Hãy đảm bảo rằng bạn đã cấu hình `Procfile` và `requirements.txt`.

## Đóng góp
Vui lòng mở các pull request hoặc issue nếu bạn có ý tưởng cải thiện ứng dụng.

## Giấy phép
Dự án này được cấp phép dưới giấy phép MIT. Xem thêm tại [LICENSE](LICENSE).
