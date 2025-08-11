import json
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)
# DEĞİŞİKLİK: Veri dosyasının yolu kalıcı depolama alanını gösterecek şekilde güncellendi.
# OpenShift'te bu dizine bir Persistent Volume Claim (PVC) bağlayacağız.
DATA_DIR = '/data'
DATA_FILE = os.path.join(DATA_DIR, 'data.json')

# Başlangıçta /data dizininin var olduğundan emin ol
os.makedirs(DATA_DIR, exist_ok=True)

# DEĞİŞTİ: Başlangıç veri yapısı güncellendi
if not os.path.exists(DATA_FILE):
    # Not: contribution_types'ı başlangıçta boş bırakmak daha esnek olabilir.
    initial_data = {"users": {}, "contribution_types": ["Soda", "Çay", "Kahve"]}
    with open(DATA_FILE, 'w') as f:
        json.dump(initial_data, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# NOT: Bu route'u artık kullanmayacağız çünkü frontend ayrı bir konteynerde olacak.
# Ama test veya doğrudan erişim için kalabilir.
@app.route('/')
def index():
    return "Soda Counter Backend API çalışıyor."

# DEĞİŞTİ: Artık tüm veriyi (kullanıcılar ve türler) döndürüyor
@app.route('/api/data', methods=['GET'])
def get_data():
    data = load_data()
    return jsonify(data)

# DEĞİŞTİ: Yeni veri yapısına göre güncellendi (data['users'])
@app.route('/api/add_person', methods=['POST'])
def add_person():
    req_data = request.json
    kisi = req_data.get('kisi')
    if not kisi: return jsonify({'error': 'Kişi adı zorunludur'}), 400
    data = load_data()
    if kisi in data['users']: return jsonify({'error': 'Bu kişi zaten mevcut'}), 409
    data['users'][kisi] = {}
    save_data(data)
    return jsonify({'success': True, 'data': data})

# DEĞİŞTİ: Yeni veri yapısına göre güncellendi (data['users'])
@app.route('/api/delete_person', methods=['POST'])
def delete_person():
    req_data = request.json
    kisi = req_data.get('kisi')
    if not kisi: return jsonify({'error': 'Kişi belirtilmedi'}), 400
    data = load_data()
    if kisi in data['users']:
        del data['users'][kisi]
        save_data(data)
        return jsonify({'success': True, 'data': data})
    return jsonify({'error': 'Silinecek kişi bulunamadı'}), 404

# DEĞİŞTİ: Yeni veri yapısına göre güncellendi (data['users'])
@app.route('/api/add_penalty', methods=['POST'])
def add_penalty():
    req_data = request.json
    kisi = req_data.get('kisi')
    icecek = req_data.get('icecek')
    quantity = int(req_data.get('quantity', 1))
    if not kisi or not icecek: return jsonify({'error': 'Kişi ve katkı payı seçilmelidir'}), 400
    data = load_data()
    if kisi not in data['users']: return jsonify({'error': 'Kişi bulunamadı'}), 404
    data['users'][kisi][icecek] = data['users'][kisi].get(icecek, 0) + quantity
    save_data(data)
    return jsonify({'success': True, 'data': data})

# DEĞİŞTİ: Yeni veri yapısına göre güncellendi (data['users'])
@app.route('/api/pay_penalty', methods=['POST'])
def pay_penalty():
    req_data = request.json
    kisi = req_data.get('kisi')
    icecek = req_data.get('icecek')
    quantity = int(req_data.get('quantity', 1))
    if not kisi or not icecek: return jsonify({'error': 'Kişi ve katkı payı seçilmelidir'}), 400
    data = load_data()
    if kisi in data['users'] and icecek in data['users'][kisi]:
        current_amount = data['users'][kisi][icecek]
        data['users'][kisi][icecek] = max(0, current_amount - quantity)
        if data['users'][kisi][icecek] == 0:
            del data['users'][kisi][icecek]
        save_data(data)
        return jsonify({'success': True, 'data': data})
    return jsonify({'error': 'Ödenecek katkı payı bulunamadı'}), 404

# --- YENİ FONKSİYONLAR ---
@app.route('/api/add_type', methods=['POST'])
def add_type():
    req_data = request.json
    type_name = req_data.get('type_name')
    if not type_name: return jsonify({'error': 'Tür adı zorunludur'}), 400
    data = load_data()
    if type_name in data['contribution_types']: return jsonify({'error': 'Bu tür zaten mevcut'}), 409
    data['contribution_types'].append(type_name)
    save_data(data)
    return jsonify({'success': True, 'data': data})

@app.route('/api/delete_type', methods=['POST'])
def delete_type():
    req_data = request.json
    type_name = req_data.get('type_name')
    if not type_name: return jsonify({'error': 'Tür adı belirtilmedi'}), 400
    data = load_data()
    if type_name in data['contribution_types']:
        data['contribution_types'].remove(type_name)
        # Bu türü kullanan kişilerden de temizlemek iyi bir pratik olabilir, ama şimdilik basit tutalım.
        save_data(data)
        return jsonify({'success': True, 'data': data})
    return jsonify({'error': 'Silinecek tür bulunamadı'}), 404


if __name__ == '__main__':
    # DEĞİŞİKLİK: OpenShift için port genellikle 8080 olarak ayarlanır. Debug kapatılır.
    app.run(host='0.0.0.0', port=8080, debug=False)
