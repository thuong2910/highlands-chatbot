# ☕ Highlands Coffee Chatbot

Chatbot dựa trên luật (Rule-based Chatbot) trả lời các câu hỏi trong lĩnh vực đồ uống. Chatbot tiếp nhận câu hỏi của người dùng bằng tiếng Việt (có hỗ trợ một phần tiếng Việt không dấu và tiếng Anh), nhận diện ý định (intent) dựa trên từ khóa, và trả lời dựa trên cơ sở tri thức được xây dựng sẵn về menu, giá, thành phần và thông tin cửa hàng của Highlands Coffee.

## Tính năng chính

- 💬 Trả lời các câu hỏi về **menu, giá cả, thành phần** của đồ uống (cà phê, trà, trà sữa, freeze...)
- ☀️ Gợi ý đồ uống theo **thời điểm trong ngày** (buổi sáng, làm việc/học bài, buổi tối) và theo **thời tiết** (trời nóng)
- 🏬 Trả lời thông tin chung về cửa hàng: giờ mở cửa, địa chỉ/chi nhánh, đặt hàng online
- 🔤 Xử lý câu hỏi **gõ không dấu** tiếng Việt (vd: "gia ca phe sua")
- 💡 Gợi ý nhanh (quick chips) và giao diện chat trực quan, có hiệu ứng typing indicator
- 🌐 Hỗ trợ một phần câu hỏi bằng **tiếng Anh** cho các chủ đề phổ biến (chào hỏi, giá, giờ mở cửa, địa chỉ...)

## Kiến trúc hệ thống

Hệ thống được tổ chức theo các lớp xử lý tuần tự, dữ liệu đi từ người dùng qua giao diện, backend, bộ xử lý chatbot, cơ sở tri thức rồi trả ngược lại giao diện:

```
                Người dùng
                    │
                    ▼
        Giao diện Web (HTML/CSS/JavaScript)  ──▶  Tương tác trực quan qua HTML/CSS/JS
                    │
                    ▼
            Backend Flask (Python)            ──▶  Xử lý logic và định tuyến dữ liệu
                    │
                    ▼
             Bộ xử lý Chatbot
                    │
                    ▼
             Knowledge Base                   ──▶  Cơ sở tri thức JSON được truy xuất liên tục
                    │
                    ▼
              Câu trả lời
                    │
                    ▼
             Giao diện Web
```

- **Giao diện Web**: thu thập câu hỏi của người dùng, gửi request và hiển thị câu trả lời.
- **Backend Flask**: tiếp nhận request từ giao diện, định tuyến (`/`, `/chat`, `/suggestions`) và gọi bộ xử lý chatbot.
- **Bộ xử lý Chatbot** (`chatbot.py`): tiền xử lý văn bản, tính điểm khớp, nhận diện intent.
- **Knowledge Base** (`data.json`): lưu toàn bộ intent, pattern và response, được bộ xử lý chatbot truy xuất liên tục để tìm câu trả lời phù hợp.
- Kết quả được trả ngược qua Backend lên Giao diện Web để hiển thị cho người dùng.

Toàn bộ giao tiếp giữa Giao diện và Backend diễn ra **bất đồng bộ (AJAX/Fetch API)**, không cần tải lại trang.

## Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Backend | Python 3, Flask |
| Frontend | HTML, CSS, JavaScript  |
| Cơ sở tri thức | JSON |
| Xử lý ngôn ngữ | Rule-based matching  |
| Triển khai | Gunicorn (qua `Procfile`) |

## Cấu trúc thư mục

```
HighlandsCoffeeChatbot/
├── app.py              # Flask routing (/, /chat, /suggestions)
├── chatbot.py          # Xử lý logic NLP: tiền xử lý, tính điểm khớp, nhận diện intent
├── data.json           # Cơ sở tri thức: intents, patterns, responses
├── requirements.txt    # Danh sách thư viện cần cài
├── Procfile            # Cấu hình chạy bằng Gunicorn khi deploy
└── templates/
    └── index.html      # Giao diện người dùng (chat UI)
```

## Cài đặt & chạy thử

### Yêu cầu

- Python 3.9+
- pip

### Bước 1 — Clone repository

```bash
git clone https://github.com/thuong2910/highlands-chatbot.git
cd highlands-chatbot
```

### Bước 2 — Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 4 — Chạy ứng dụng

```bash
python app.py
```

Mặc định ứng dụng chạy tại: **http://127.0.0.1:5000**

## Triển khai (Deploy)

Dự án đã có sẵn `Procfile` để chạy bằng Gunicorn — phù hợp deploy lên các nền tảng PaaS như Render, Railway hoặc Heroku:

```
web: gunicorn app:app
```

Ứng dụng tự đọc cổng từ biến môi trường `PORT` (mặc định `5000` khi chạy local).

## API

| Method | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/` | Trả về giao diện chat (`index.html`) |
| `POST` | `/chat` | Nhận `{ "message": "..." }`, trả về `{ "response": "..." }` |
| `GET` | `/suggestions` | Trả về danh sách gợi ý nhanh (quick chips) |

Ví dụ gọi `/chat`:

```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "giá cà phê sữa"}'
```

## Đánh giá độ chính xác

Kết quả kiểm thử với 30 câu hỏi thuộc các chủ đề khác nhau:

| Nhóm câu hỏi | Số câu kiểm thử | Trả lời đúng | Tỉ lệ |
|---|---|---|---|
| Giá sản phẩm | 10 | 9 | 90% |
| Thành phần & công dụng | 6 | 5 | 83% |
| Gợi ý đồ uống | 6 | 6 | 100% |
| Thông tin cửa hàng | 5 | 5 | 100% |
| Câu hỏi không dấu | 3 | 2 | 67% |
| **Tổng** | **30** | **27** | **90%** |

## Hạn chế

- Chỉ xử lý tốt các câu hỏi nằm trong phạm vi dữ liệu đã định nghĩa trong `data.json`
- Chưa xử lý tốt câu hỏi phức tạp, kết hợp nhiều ý trong một câu
- Là hệ thống rule-based — chưa có khả năng tự học từ hội thoại thực tế
- Khả năng hiểu ngôn ngữ tự nhiên còn hạn chế so với các mô hình NLP hiện đại (chưa dùng machine learning/embedding)
- Phạm vi dữ liệu chưa bao quát toàn bộ thực đơn thực tế của Highlands Coffee

## Hướng phát triển

- Mở rộng cơ sở tri thức: thêm sản phẩm, khuyến mãi, thông tin chi tiết hơn
- Tích hợp chức năng đặt hàng trực tuyến ngay trong hội thoại
- Chuyển dữ liệu từ JSON sang hệ quản trị CSDL (MySQL/MongoDB) khi quy mô lớn hơn
- Áp dụng các kỹ thuật NLP/ML hiện đại (TF-IDF, embedding, mô hình phân loại) để nhận diện intent chính xác hơn, thay cho so khớp từ khóa thủ công
- Triển khai trên các nền tảng phổ biến: Facebook Messenger, Zalo, ứng dụng di động
- Tích hợp các mô hình ngôn ngữ lớn (LLM) để hội thoại tự nhiên hơn

