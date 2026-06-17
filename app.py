from flask import Flask, request, jsonify, render_template
from chatbot import load_data, get_response

app = Flask(__name__)

# Tải dữ liệu một lần khi khởi động
data = load_data()

# ── Route chính ───────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# ── Route xử lý tin nhắn ─────────────────────────────────────
@app.route('/chat', methods=['POST'])
def chat():
    body    = request.get_json(silent=True) or {}
    message = body.get('message', '').strip()

    if not message:
        return jsonify({'response': 'Bạn chưa nhập câu hỏi. Thử hỏi về giá cà phê hoặc thực đơn nhé! ☕'})

    result = get_response(message, data)
    return jsonify({'response': result['response']})

# ── Route lấy danh sách gợi ý nhanh ─────────────────────────
@app.route('/suggestions', methods=['GET'])
def suggestions():
    tips = [
        'Xem menu', 'Giá cà phê sữa', 'Giá trà đào',
        'Uống gì buổi sáng', 'Trời nóng uống gì',
        'Thành phần cà phê', 'Giờ mở cửa', 'Đặt hàng online'
    ]
    return jsonify({'suggestions': tips})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
