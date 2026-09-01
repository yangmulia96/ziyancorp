import os
import re
import json
import random
import socket
import urllib.request
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"C:\Users\arija\ziyancorp\narasi_kilat_pwa")
STATIC_DIR = BASE_DIR / "static"
FEEDBACK_FILE = BASE_DIR / "community_feedback.json"

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

def clean_product_name(text):
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'[^\w\s\d%]', ' ', text)
    words = text.split()
    if len(words) > 7:
        return ' '.join(words[:7])
    return ' '.join(words) if words else "produk pilihan ini"

# ----------------- NICHE SEMANTIC DETECTOR -----------------
def detect_product_category(text):
    t = text.lower()
    if any(k in t for k in ["baju", "gamis", "tunik", "dress", "hijab", "kemeja", "kaos", "celana", "rok", "outfit", "jaket", "hoodie", "blouse", "kulot"]):
        return "fashion"
    elif any(k in t for k in ["serum", "cream", "krim", "sunscreen", "toner", "lipstik", "cushion", "bedak", "facial", "glow", "jerawat", "skincare", "parfum", "body lotion"]):
        return "skincare"
    elif any(k in t for k in ["sepatu", "sandal", "sneakers", "heels", "flatshoes", "boots", "loafers", "wedges"]):
        return "shoes"
    elif any(k in t for k in ["hp", "case", "casing", "charger", "tws", "headset", "earphone", "powerbank", "kabel", "holder", "smartwatch", "gadget", "tripod"]):
        return "gadget"
    elif any(k in t for k in ["wajan", "panci", "blender", "spatula", "sapu", "rak", "botol", "tumbler", "dapur", "rumah", "organizer", "bantal", "sprei"]):
        return "home"
    elif any(k in t for k in ["snack", "keripik", "sambal", "kopi", "madu", "teh", "makanan", "minuman", "cokelat", "baso aci", "herbal"]):
        return "food"
    return "general"

# ----------------- RICH 10-HOOK & 8-STRATEGY DYNAMIC MATRIX ENGINE -----------------

NICHE_VOCAB = {
    "fashion": {
        "benefits": ["cuttingannya bikin kelihatan jenjang dan ramping", "bahannya jatuh, flowy, dan super adem no gerah", "fittingnya pas banget di badan gak bikin begah", "jahitannya super rapi sekelas butik mall", "bikin look auto elegan dan anggun seharian"],
        "pain_points": ["sering beli baju online tapi pas dateng bahannya panas dan kaku", "bingung cari outfit yang nyaman buat daily tapi tetap rapi", "kecewa sama baju yang gampang kusut dan jahitannya gampang lepas"],
        "proofs": ["udah ribet repeat order karena se-nyaman itu", "kancing dan detail potongannya beneran mewah", "dipakai gerak aktif seharian tetap sejuk"]
    },
    "skincare": {
        "benefits": ["teksturnya seringan air langsung meresap tanpa lengket", "bikin kulit auto plumpy, lembap, dan glowing sehat", "skin barrier makin kuat tanpa bikin iritasi", "no whitecast dan aman banget buat kulit sensitif", "bikin flek dan bekas jerawat makin tersamarkan"],
        "pain_points": ["capek gonta-ganti skincare tapi wajah malah kusam dan bruntusan", "mager pakai sunscreen yang bikin muka dempul dan abu-abu", "insecure sama tekstur kulit yang kering dan kasar"],
        "proofs": ["formula dermatologis yang udah lulus uji BPOM", "banyak beauty creator yang approve hasilnya", "pemakaian seminggu udah kelihatan bedanya"]
    },
    "shoes": {
        "benefits": ["bantalannya super empuk kayak nginjak awan anti lecet", "solnya karet anti slip aman di lantai basah", "bobotnya ringan banget gak bikin kaki pegal", "desainnya stylish gampang dicocokin ke outfit apa aja", "kokoh dan awet dipakai jalan seharian"],
        "pain_points": ["kaki sering lecet dan pegal pas pakai sepatu seharian", "sol gampang licin dan jebol pas musim hujan", "model sepatu keren tapi dipakai setengah jam udah bikin tersiksa"],
        "proofs": ["ribuan orang udah buktiin empuknya buat commute", "jahitan lemnya rapi dan kuat banget", "nyaman dipakai jalan 10.000 langkah"]
    },
    "gadget": {
        "benefits": ["daya tahannya badak dan materialnya super presisi", "suaranya jernih dengan bass bulat no delay", "pengisian dayanya ngebut dan gak bikin device panas", "desain minimalis modern yang gampang dibawa kemana-mana", "proteksi maksimal dari benturan dan jatuh"],
        "pain_points": ["sering apes beli aksesoris abal-abal tapi seminggu udah rusak", "suara headset kresek-kresek pas diajak gaming atau meeting", "baterai gampang drop dan kabel cepet putus"],
        "proofs": ["chipset cerdas dengan kompatibilitas universal", "material anti-scratch yang beneran kokoh", "ribuan review bintang lima membuktikan"]
    },
    "home": {
        "benefits": ["bikin pekerjaan rumah jadi 3 kali lebih cepat dan praktis", "material food grade yang kokoh dan gampang dibersihkan", "hemat tempat dan bikin ruangan kelihatan estetik rapi", "awet tahan panas gak gampang penyok atau retak"],
        "pain_points": ["dapur berantakan dan ribet nyiapin printilan masak", "alat rumah tangga cepat rusak dan susah dicuci", "ruangan sempit karena barang-barang gak tertata rapi"],
        "proofs": ["ibu-ibu cerdas udah pada beralih ke sini", "finishing rapi dan kokoh menahan beban", "solusi praktis buat rumah minimalis"]
    },
    "food": {
        "benefits": ["rasanya gurih mantap nagih gak bikin enek", "bumbunya medok meresap sampai ke dalam", "kemasan higienis ziplock kedap udara tetap renyah", "bahan alami pilihan tanpa pengawet berlebih"],
        "pain_points": ["sering beli cemilan tapi bumbunya hambar dan alot", "pengen ngemil enak tapi takut bumbu kimia menyengat", "makanan cepet mlempem pas baru dibuka"],
        "proofs": ["sekali coba dijamin susah berhenti ngunyah", "best seller yang selalu sold out ribuan pcs", "favorit keluarga buat nemenin santai"]
    },
    "general": {
        "benefits": ["kualitas bahan terjamin dan awet pemakaian jangka panjang", "desain praktis multifungsi bikin hidup makin simpel", "kualitas premium dengan mutu yang jauh di atas ekspektasi", "finishing rapi dan detailnya beneran premium"],
        "pain_points": ["capek buang uang buat barang yang kualitasnya zonk", "bingung cari produk yang beneran terbukti bagus dan awet", "butuh solusi praktis yang teruji dan berkualitas premium"],
        "proofs": ["ribuan pembeli udah kasih ulasan bintang 5", "seller terpercaya dengan pengiriman super cepat", "garansi kepuasan yang bikin hati tenang"]
    }
}

CTA_LIST = [
    "Biar gak kehabisan varian favoritmu, langsung tap keranjang kuning di pojok kiri bawah sekarang juga!",
    "Jangan tunggu sampai stoknya ludes ya, buruan amankan produk incaranmu di keranjang kuning sekarang!",
    "Mumpung barangnya ready dan siap kirim, yuk langsung checkout di keranjang kuning sekarang juga!",
    "Biar penampilan makin stylish dan rapi seharian, langsung serbu keranjang kuning sebelum kehabisan!",
    "Yang mau samaan dan ngerasain kenyamanannya, yuk langsung klik keranjang kuning di bawah sekarang!"
]

def generate_dynamic_naskah_matrix(product_raw, hook_type="auto", strategy="AIDA", duration=10, category="auto"):
    prod = clean_product_name(product_raw)
    cat = detect_product_category(product_raw) if category == "auto" or not category else category
    vocab = NICHE_VOCAB.get(cat, NICHE_VOCAB["general"])
    
    b1 = random.choice(vocab["benefits"])
    b2 = random.choice([b for b in vocab["benefits"] if b != b1] or vocab["benefits"])
    p1 = random.choice(vocab["pain_points"])
    pr1 = random.choice(vocab["proofs"])
    cta1 = random.choice(CTA_LIST)
    cta2 = random.choice([c for c in CTA_LIST if c != cta1] or CTA_LIST)
    cta3 = random.choice([c for c in CTA_LIST if c not in [cta1, cta2]] or CTA_LIST)
    cta4 = random.choice([c for c in CTA_LIST if c not in [cta1, cta2, cta3]] or CTA_LIST)

    # 10 HOOK GENERATOR TEMPLATES
    hooks = {
        "warning": [
            f"Jangan pernah beli {prod} ini sebelum kamu tahu kalau {b1}!",
            f"Tolong jangan skip kalau kamu gak mau nyesel buang duit buat {prod} abal-abal!"
        ],
        "pain": [
            f"Pernah gak sih ngerasa {p1}? Tenang, akhirnya nemu solusinya!",
            f"Stop buang uang dan waktu! Kalau kamu sering ngalamin {p1}, wajib tonton ini sampai habis."
        ],
        "shock": [
            f"Jujur pas unboxing {prod} ini, aku beneran speechless sama kualitas detailnya!",
            f"Plot twist ter-epic bulan ini! Akhirnya nemu {prod} dengan estetika se-mewah ini!"
        ],
        "secret": [
            f"Pantesan toko sebelah ketar-ketir, ternyata rahasia {prod} ini karena {b1}!",
            f"Aku sebenernya mau simpan rahasia ini sendiri, tapi {prod} ini beneran terlalu bagus buat gak di-spill!"
        ],
        "fomo": [
            f"Bocoran info penting! Varian favorit {prod} ini sisa kuotanya tinggal sedikit banget!",
            f"Kabar gawat buat yang lagi incer {prod} viral ini! Stok batch produksinya makin menipis parah!"
        ],
        "story": [
            f"Kemarin pas lagi kumpul, tiba-tiba temen-temenku pada salfok nanyain {prod} yang aku bawa...",
            f"Awalnya cuma iseng checkout {prod} ini karena penasaran, eh taunya malah jadi barang paling kepakai tiap hari!"
        ],
        "debunk": [
            f"Banyak yang ngira {prod} se-estetik ini susah dicari, padahal rahasianya ada di sini...",
            f"Siapa bilang barang berkualitas itu susah dicari? Coba liat {prod} yang satu ini!"
        ],
        "niche": [
            f"Khusus buat kamu yang pengen tampil percaya diri dan elegan seharian, sini merapat!",
            f"Panggilan buat pejuang sat-set yang butuh {prod} praktis dan anti ribet!"
        ],
        "battle": [
            f"Battle jujur! Brand ternama mall vs {prod} viral keranjang kuning, kira-kira menang mana?",
            f"Gak nyangka kualitas {prod} ini berani diadu sama brand mahal ternama!"
        ],
        "transform": [
            f"Perbedaan sebelum dan sesudah pakai {prod} ini beneran nyata banget!",
            f"Definisi upgrade hidup jadi lebih simpel dan nyaman semenjak ada {prod} ini!"
        ]
    }

    # Selected hooks pool
    if hook_type in hooks:
        h_pool = hooks[hook_type]
    else:
        # Auto mix 4 distinct hooks
        h_types = list(hooks.keys())
        random.shuffle(h_types)
        h_pool = [random.choice(hooks[ht]) for ht in h_types[:4]]

    # 4 VARIASI NASKAH UNIK DENGAN SUDUT PANDANG BERBEDA
    v1_hook = h_pool[0] if len(h_pool) > 0 else f"Lagi cari {prod} yang terbukti kualitasnya?"
    v2_hook = h_pool[1] if len(h_pool) > 1 else random.choice(hooks["shock"])
    v3_hook = h_pool[2] if len(h_pool) > 2 else random.choice(hooks["secret"])
    v4_hook = h_pool[3] if len(h_pool) > 3 else random.choice(hooks["story"])

    # VARIATION 1: High Energy / Direct Conversion (Hook A + Benefit + CTA)
    var_1 = f"{v1_hook} Kenalin {prod} yang lagi hits ini. Gak cuma {b1}, tapi {b2}. Ditambah lagi {pr1}. {cta1}"

    # VARIATION 2: Pain-Point & Solution / Empathy (Hook B + Problem Relief + Value + CTA)
    var_2 = f"{v2_hook} {prod} ini hadir jadi jawaban buat kamu. Rasain sendiri gimana {b1} dengan kualitas yang gak main-main. {cta2}"

    # VARIATION 3: Storytelling & Social Proof / Aspirational (Hook C + Review Jujur + Fitur + CTA)
    var_3 = f"{v3_hook} Pas dicoba, beneran juara banget karena {b2}. Nyesel banget kalau gak tahu dari dulu. {cta3}"

    # VARIATION 4: Value Stacking & Urgensi / Smart Shopper (Hook D + Daily Benefit + Flash Sale + CTA)
    var_4 = f"{v4_hook} Kapan lagi dapet {prod} yang {b1} dan beneran awet dipakai? {cta4}"

    return {
        "category_detected": cat,
        "variasi_1": var_1,
        "variasi_2": var_2,
        "variasi_3": var_3,
        "variasi_4": var_4,
        "hook_types_used": [
            "Hook Tajam & Benefit Fokus",
            "Hook Solutif & Penawar Masalah",
            "Hook Storytelling & Rekomendasi Tulus",
            "Hook Urgensi & Nilai Hemat"
        ]
    }

# ----------------- UGC FASHION STUDIO ENGINE -----------------
def generate_ugc_studio_package(product_raw, num_scenes=2, model_style="Hijab Casual Modern", setting="Aesthetic Cafe Outdoor"):
    prod = clean_product_name(product_raw)
    num_scenes = int(num_scenes) if str(num_scenes).isdigit() else 2
    num_scenes = max(1, min(3, num_scenes))
    
    analysis = f"Pakaian '{prod}' memiliki keunggulan visual pada cutting yang flowy, material ringan berkualitas, serta fitting yang pas di badan untuk gaya {model_style}."
    strategy = f"Menarik perhatian dalam 3 detik pertama dengan gerakan jalan model natural di {setting}, memperlihatkan jatuhnya bahan kain saat bergerak, dan menutup dengan ajakan belanja (CTA) keranjang kuning."

    scenes = []
    if num_scenes == 1:
        scenes.append({
            "scene_num": 1,
            "duration": "10 Detik",
            "title": "Scene 1: Flash Review & Direct Hook",
            "goal": "Menarik perhatian seketika, pamer flow bahan pakaian, dan ajakan checkout langsung.",
            "visual": f"Model {model_style} berjalan santai ke arah kamera di {setting}, tersenyum ramah, merapikan sedikit bagian depan {prod}, lalu menunjukkan flow kain yang anggun.",
            "camera": "Eye-level handheld, slow push-in mengikuti langkah model, vertical 9:16 framing.",
            "lighting": "Natural soft daylight dengan warm cinematic glow.",
            "background": f"{setting} dengan bokeh lembut di latar belakang.",
            "vo": f"Outfit senyaman ini beneran bikin percaya diri seharian! {prod} kualitas juara, yuk tap keranjang kuning sekarang mumpung stok masih ready!",
            "omni_prompt": f"UGC TikTok video recorded on iPhone 15 Pro, vertical 9:16, photorealistic. A gorgeous {model_style} wearing {prod} walking gracefully towards camera in {setting}. Realistic soft fabric movement and flow as she turns and smiles naturally at camera. Eye level handheld camera tracking with slow push in. Soft warm natural daylight, authentic influencer lifestyle aesthetic, crisp 4k 60fps."
        })
    elif num_scenes == 2:
        scenes.append({
            "scene_num": 1,
            "duration": "10 Detik",
            "title": "Scene 1: Hook Visual & First Impression",
            "goal": "Menghentikan jempol penonton dalam 3 detik pertama dan menunjukkan look keseluruhan pakaian.",
            "visual": f"Model {model_style} berjalan percaya diri di {setting}, melirik ke kamera dengan senyum natural, memperlihatkan siluet anggun {prod} dari tampak depan dan samping.",
            "camera": "Medium full body shot, handheld follow tracking, slow pull-out.",
            "lighting": "Bright natural morning daylight, soft golden rim light.",
            "background": f"{setting} bersih dan estetik.",
            "vo": f"Akhirnya nemu outfit yang bikin look kelihatan anggun tapi tetap adem! {prod} ini beneran langsung jadi favorit aku.",
            "omni_prompt": f"Scene 1 UGC fashion video, vertical 9:16, photorealistic. A beautiful {model_style} wearing {prod} walking gracefully in {setting}. She smiles naturally at camera, smooth body movement, realistic fabric physics floating with the breeze. Medium shot with gentle handheld camera motion, soft natural sunlight, crisp 4k."
        })
        scenes.append({
            "scene_num": 2,
            "duration": "10 Detik",
            "title": "Scene 2: Detail Jahitan, Bahan & Strong CTA",
            "goal": "Memperlihatkan detail tekstur kain, kerapian jahitan, dan mengajak checkout di keranjang kuning.",
            "visual": f"Kamera mendekat (close-up), model menyentuh lembut tekstur bahan {prod}, memperlihatkan detail kerah dan lengan, lalu berputar 180 derajat dan tersenyum menunjuk ke arah keranjang kuning.",
            "camera": "Close-up detail shot to medium orbit shot, smooth handheld transition.",
            "lighting": "Diffused softbox/sunlight menonjolkan tekstur serat kain.",
            "background": f"Konsisten dengan Scene 1 ({setting}).",
            "vo": f"Jahitannya rapi, bahannya jatuh dan super adem. Yang mau samaan, langsung tap keranjang kuning sekarang ya mumpung promo!",
            "omni_prompt": f"Scene 2 continuous UGC video, vertical 9:16, photorealistic. Same {model_style} wearing the same {prod} in {setting}. Camera does a smooth close-up tracking shot showing fabric texture, clean stitches, and sleeve details. She gently touches the fabric, spins 180 degrees, and points warmly towards bottom left. Natural lighting, seamless transition from scene 1, 4k 60fps."
        })
    else:
        scenes.append({
            "scene_num": 1,
            "duration": "10 Detik",
            "title": "Scene 1: Hook & Try-On Reveal",
            "goal": "Hook penasaran OOTD dan penampilan pertama yang memikat.",
            "visual": f"Model {model_style} melangkah ke dalam frame di {setting}, memperlihatkan fitting {prod} dari depan dengan percaya diri.",
            "camera": "Full body eye level shot, slow push in.",
            "lighting": "Natural daylight warm ambient.",
            "background": f"{setting}.",
            "vo": f"Spill outfit yang lagi sering banget aku pakai belakangan ini! {prod} yang bikin look auto rapi dan elegan.",
            "omni_prompt": f"Scene 1 UGC fashion video, 9:16 vertical, photorealistic. {model_style} model stepping into frame wearing {prod} in {setting}. Full body eye level view, natural fabric draping, soft warm daylight, authentic TikTok influencer style."
        })
        scenes.append({
            "scene_num": 2,
            "duration": "10 Detik",
            "title": "Scene 2: Fabric Flow & 360 Spin",
            "goal": "Menunjukkan bagaimana bahan bergerak dan tampak dari segala sisi.",
            "visual": f"Model berputar 360 derajat perlahan, menunjukkan potongan belakang dan flow kain {prod} saat melambai terkena angin.",
            "camera": "Medium tracking orbit shot 360 degrees.",
            "lighting": "Golden hour soft rim light.",
            "background": f"{setting}.",
            "vo": f"Kelihatan kan flow bahannya seringan apa? Dipakai gerak seharian tetap nyaman, gak bikin gerah sama sekali.",
            "omni_prompt": f"Scene 2 continuous video, 9:16 vertical, photorealistic. Same {model_style} model wearing same {prod} in {setting}. She does a slow graceful 360 degree spin showing back cutting and fabric movement. Dynamic orbit camera movement, warm lighting, 4k."
        })
        scenes.append({
            "scene_num": 3,
            "duration": "10 Detik",
            "title": "Scene 3: Detail Close-up & Strong CTA",
            "goal": "Menyorot detail kerah/kancing dan mengunci konversi penjualan.",
            "visual": f"Close-up tangan model merapikan kerah dan bahan {prod}, lalu tersenyum manis ke kamera sambil mengajak checkout.",
            "camera": "Close-up to medium handheld shot.",
            "lighting": "Soft focus portrait lighting.",
            "background": f"{setting}.",
            "vo": f"Jahitan dan detailnya se-mewah ini dengan finishing rapi! Yuk buruan amankan di keranjang kuning sekarang juga sebelum kehabisan!",
            "omni_prompt": f"Scene 3 continuous video, 9:16 vertical, photorealistic. Close-up shot of {model_style} model touching the sleeve and collar details of {prod} in {setting}. She smiles cheerfully at camera and gestures to bottom left corner. Crisp 4k, natural daylight, authentic creator look."
        })

    image_prompt = f"Professional fashion catalog portrait photo, 9:16 vertical. A beautiful {model_style} model wearing {prod}, standing posing in {setting}. High fashion editorial styling, authentic natural skin texture, realistic fabric folds and rich colors, soft diffused daylight, shot on Hasselblad 85mm lens, f/1.8, 8k resolution, cinematic masterpiece."

    return {
        "status": "success",
        "product_analysis": analysis,
        "promo_strategy": strategy,
        "scenes": scenes,
        "image_model_prompt": image_prompt
    }

def save_community_feedback(name, contact, rating, category, message):
    feedback_list = []
    if FEEDBACK_FILE.exists():
        try:
            feedback_list = json.loads(FEEDBACK_FILE.read_text(encoding="utf-8"))
        except Exception:
            feedback_list = []
    
    new_entry = {
        "id": len(feedback_list) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name or "Anonim",
        "contact": contact or "-",
        "rating": rating or 5,
        "category": category or "Saran Fitur",
        "message": message
    }
    feedback_list.append(new_entry)
    FEEDBACK_FILE.write_text(json.dumps(feedback_list, indent=2, ensure_ascii=False), encoding="utf-8")
    return new_entry

class AppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.path = "/static/index.html"
        elif not self.path.startswith("/static/"):
            if (STATIC_DIR / self.path.lstrip("/")).exists():
                self.path = "/static" + self.path
        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        
        if self.path == "/api/generate":
            try:
                data = json.loads(body)
                product_input = data.get("product_input", "")
                hook_type = data.get("hook_type", "auto")
                strategy = data.get("strategy", "AIDA (Penjualan Kilat)")
                duration = data.get("duration", 10)
                category = data.get("category", "auto")
                
                result = generate_dynamic_naskah_matrix(product_input, hook_type, strategy, duration, category)
                result["status"] = "success"
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

        elif self.path == "/api/ugc-studio":
            try:
                data = json.loads(body)
                product_input = data.get("product_input", "Gamis / Pakaian Fashion")
                num_scenes = data.get("num_scenes", 2)
                model_style = data.get("model_style", "Hijab Casual Modern")
                setting = data.get("setting", "Aesthetic Cafe Outdoor")

                pkg = generate_ugc_studio_package(product_input, num_scenes, model_style, setting)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(pkg).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

        elif self.path == "/api/feedback":
            try:
                data = json.loads(body)
                name = data.get("name", "")
                contact = data.get("contact", "")
                rating = data.get("rating", 5)
                category = data.get("category", "Saran Fitur")
                message = data.get("message", "")

                if not message.strip():
                    raise ValueError("Pesan saran tidak boleh kosong")

                saved = save_community_feedback(name, contact, rating, category, message)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "data": saved}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def run_server(port=8899):
    local_ip = get_local_ip()
    server_address = ("0.0.0.0", port)
    httpd = ThreadingHTTPServer(server_address, AppHandler)
    print(f"\n=======================================================")
    print(f"[+] NarasiKilat v15 AI Matrix Studio Server Aktif!")
    print(f"[+] Buka di Komputer   : http://localhost:{port}")
    print(f"[+] Buka di HP Android : http://{local_ip}:{port}")
    print(f"=======================================================\n")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
