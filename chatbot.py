import json
import re
import random
import unicodedata

# ── Tải dữ liệu ──────────────────────────────────────────────
def load_data(path='data.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ── Tiền xử lý văn bản ───────────────────────────────────────
def normalize(text):
    """Chuyển về chữ thường, bỏ dấu câu, chuẩn hóa khoảng trắng."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def remove_accents(text):
    """Bỏ dấu tiếng Việt để so sánh gần đúng."""
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))

# ── Tính điểm khớp giữa input và pattern ─────────────────────
def match_score(user_input, pattern):
    u = normalize(user_input)
    p = normalize(pattern)
    score = 0
    # Khớp hoàn toàn
    if u == p:
        return 100
    # Chuỗi con chính xác
    if p in u or u in p:
        score += 10
    # So sánh không dấu
    u_nd = remove_accents(u)
    p_nd = remove_accents(p)
    if p_nd in u_nd or u_nd in p_nd:
        score += 6
    # Đếm từ chung
    u_words = set(u.split())
    p_words = set(p.split())
    common  = u_words & p_words
    if common:
        score += len(common) * 2
        # Thưởng nếu tỉ lệ từ khớp cao
        ratio = len(common) / max(len(p_words), 1)
        score += int(ratio * 5)
    # So sánh từ không dấu
    u_nd_words = set(u_nd.split())
    p_nd_words = set(p_nd.split())
    common_nd  = u_nd_words & p_nd_words
    if common_nd:
        score += len(common_nd)
    return score

# ── Tìm intent phù hợp nhất ──────────────────────────────────
def find_intent(user_input, data):
    best_intent = None
    best_score  = 0

    for intent in data['intents']:
        if intent['tag'] == 'khong_hieu':
            continue
        for pattern in intent['patterns']:
            s = match_score(user_input, pattern)
            if s > best_score:
                best_score  = s
                best_intent = intent

    # Ngưỡng tối thiểu để chấp nhận
    if best_score < 3:
        for intent in data['intents']:
            if intent['tag'] == 'khong_hieu':
                return intent, 0

    return best_intent, best_score

# ── Sinh câu trả lời ─────────────────────────────────────────
def get_response(user_input, data):
    intent, score = find_intent(user_input, data)
    response = random.choice(intent['responses'])
    return {
        'response': response,
        'intent':   intent['tag'],
        'score':    score
    }
