// Vercel serverless: /api/generate
// Matrix engine — generate 4 variasi naskah tanpa API key (lokal).

function cleanProductName(text) {
  text = text.replace(/https?:\/\/\S+/g, '');
  text = text.replace(/[^\w\s\d%]/g, ' ');
  const words = text.split(/\s+/).filter(Boolean);
  if (words.length > 7) words.length = 7;
  return words.join(' ') || 'produk pilihan ini';
}

function detectCategory(text) {
  const t = text.toLowerCase();
  if (/(baju|gamis|tunik|dress|hijab|kemeja|kaos|celana|rok|outfit|jaket|hoodie|blouse|kulot)/.test(t)) return 'fashion';
  if (/(serum|cream|krim|sunscreen|toner|lipstik|cushion|bedak|facial|glow|jerawat|skincare|parfum|body\s*lotion)/.test(t)) return 'skincare';
  if (/(sepatu|sandal|sneakers|heels|flatshoes|boots|loafers|wedges)/.test(t)) return 'shoes';
  if (/(hp|case|casing|charger|tws|headset|earphone|powerbank|kabel|holder|smartwatch|gadget|tripod)/.test(t)) return 'gadget';
  if (/(wajan|panci|blender|spatula|sapu|rak|botol|tumbler|dapur|rumah|organizer|bantal|sprei)/.test(t)) return 'home';
  if (/(snack|keripik|sambal|kopi|madu|teh|makanan|minuman|cokelat|baso\s*aci|herbal)/.test(t)) return 'food';
  return 'general';
}

const NICHE_VOCAB = {
  fashion: {
    benefits: ['cuttingannya bikin kelihatan jenjang dan ramping','bahannya jatuh, flowy, dan super adem no gerah','fittingnya pas banget di badan gak bikin begah','jahitannya super rapi sekelas butik mall','bikin look auto elegan dan anggun seharian'],
    pain_points: ['sering beli baju online tapi pas dateng bahannya panas dan kaku','bingung cari outfit yang nyaman buat daily tapi tetap rapi','kecewa sama baju yang gampang kusut dan jahitannya gampang lepas'],
    proofs: ['udah ribet repeat order karena se-nyaman itu','kancing dan detail potongannya beneran mewah','dipakai gerak aktif seharian tetap sejuk'],
  },
  skincare: {
    benefits: ['teksturnya seringan air langsung meresap tanpa lengket','bikin kulit auto plumpy, lembap, dan glowing sehat','skin barrier makin kuat tanpa bikin iritasi','no whitecast dan aman banget buat kulit sensitif','bikin flek dan bekas jerawat makin tersamarkan'],
    pain_points: ['capek gonta-ganti skincare tapi wajah malah kusam dan bruntusan','mager pakai sunscreen yang bikin muka dempul dan abu-abu','insecure sama tekstur kulit yang kering dan kasar'],
    proofs: ['formula dermatologis yang udah lulus uji BPOM','banyak beauty creator yang approve hasilnya','pemakaian seminggu udah kelihatan bedanya'],
  },
  shoes: {
    benefits: ['bantalannya super empuk kayak nginjak awan anti lecet','solnya karet anti slip aman di lantai basah','bobotnya ringan banget gak bikin kaki pegal','desainnya stylish gampang dicocokin ke outfit apa aja','kokoh dan awet dipakai jalan seharian'],
    pain_points: ['kaki sering lecet dan pegal pas pakai sepatu seharian','sol gampang licin dan jebol pas musim hujan','model sepatu keren tapi dipakai setengah jam udah bikin tersiksa'],
    proofs: ['ribuan orang udah buktiin empuknya buat commute','jahitan lemnya rapi dan kuat banget','nyaman dipakai jalan 10.000 langkah'],
  },
  gadget: {
    benefits: ['daya tahannya badak dan materialnya super presisi','suaranya jernih dengan bass bulat no delay','pengisian dayanya ngebut dan gak bikin device panas','desain minimalis modern yang gampang dibawa kemana-mana','proteksi maksimal dari benturan dan jatuh'],
    pain_points: ['sering apes beli aksesoris abal-abal tapi seminggu udah rusak','suara headset kresek-kresek pas diajak gaming atau meeting','baterai gampang drop dan kabel cepet putus'],
    proofs: ['chipset cerdas dengan kompatibilitas universal','material anti-scratch yang beneran kokoh','ribuan review bintang lima membuktikan'],
  },
  home: {
    benefits: ['bikin pekerjaan rumah jadi 3 kali lebih cepat dan praktis','material food grade yang kokoh dan gampang dibersihkan','hemat tempat dan bikin ruangan kelihatan estetik rapi','awet tahan panas gak gampang penyok atau retak'],
    pain_points: ['dapur berantakan dan ribet nyiapin printilan masak','alat rumah tangga cepat rusak dan susah dicuci','ruangan sempit karena barang-barang gak tertata rapi'],
    proofs: ['ibu-ibu cerdas udah pada beralih ke sini','finishing rapi dan kokoh menahan beban','solusi praktis buat rumah minimalis'],
  },
  food: {
    benefits: ['rasanya gurih mantap nagih gak bikin enek','bumbunya medok meresap sampai ke dalam','kemasan higienis ziplock kedap udara tetap renyah','bahan alami pilihan tanpa pengawet berlebih'],
    pain_points: ['sering beli cemilan tapi bumbunya hambar dan alot','pengen ngemil enak tapi takut bumbu kimia menyengat','makanan cepet mlempem pas baru dibuka'],
    proofs: ['sekali coba dijamin susah berhenti ngunyah','best seller yang selalu sold out ribuan pcs','favorit keluarga buat nemenin santai'],
  },
  general: {
    benefits: ['kualitas bahan terjamin dan awet pemakaian jangka panjang','desain praktis multifungsi bikin hidup makin simpel','kualitas premium dengan mutu yang jauh di atas ekspektasi','finishing rapi dan detailnya beneran premium'],
    pain_points: ['capek buang uang buat barang yang kualitasnya zonk','bingung cari produk yang beneran terbukti bagus dan awet','butuh solusi praktis yang teruji dan berkualitas premium'],
    proofs: ['ribuan pembeli udah kasih ulasan bintang 5','seller terpercaya dengan pengiriman super cepat','garansi kepuasan yang bikin hati tenang'],
  },
};

const CTA_LIST = [
  'Biar gak kehabisan varian favoritmu, langsung tap keranjang kuning di pojok kiri bawah sekarang juga!',
  'Jangan tunggu sampai stoknya ludes ya, buruan amankan produk incaranmu di keranjang kuning sekarang!',
  'Mumpung barangnya ready dan siap kirim, yuk langsung checkout di keranjang kuning sekarang juga!',
  'Biar penampilan makin stylish dan rapi seharian, langsung serbu keranjang kuning sebelum kehabisan!',
  'Yang mau samaan dan ngerasain kenyamanannya, yuk langsung klik keranjang kuning di bawah sekarang!',
];

const HOOKS = {
  warning: (p, b) => [
    `Jangan pernah beli ${p} ini sebelum kamu tahu kalau ${b}!`,
    `Tolong jangan skip kalau kamu gak mau nyesel buang duit buat ${p} abal-abal!`,
  ],
  pain: (p, pn) => [
    `Pernah gak sih ngerasa ${pn}? Tenang, akhirnya nemu solusinya!`,
    `Stop buang uang dan waktu! Kalau kamu sering ngalamin ${pn}, wajib tonton ini sampai habis.`,
  ],
  shock: (p, b) => [
    `Jujur pas unboxing ${p} ini, aku beneran speechless sama kualitas detailnya!`,
    `Plot twist ter-epic bulan ini! Akhirnya nemu ${p} dengan estetika se-mewah ini!`,
  ],
  secret: (p, b) => [
    `Pantesan toko sebelah ketar-ketir, ternyata rahasia ${p} ini karena ${b}!`,
    `Aku sebenernya mau simpan rahasia ini sendiri, tapi ${p} ini beneran terlalu bagus buat gak di-spill!`,
  ],
  fomo: (p) => [
    `Bocoran info penting! Varian favorit ${p} ini sisa kuotanya tinggal sedikit banget!`,
    `Kabar gawat buat yang lagi incer ${p} viral ini! Stok batch produksinya makin menipis parah!`,
  ],
  story: (p) => [
    `Kemarin pas lagi kumpul, tiba-tiba temen-temenku pada salfok nanyain ${p} yang aku bawa...`,
    `Awalnya cuma iseng checkout ${p} ini karena penasaran, eh taunya malah jadi barang paling kepakai tiap hari!`,
  ],
  debunk: (p) => [
    `Banyak yang ngira ${p} se-estetik ini susah dicari, padahal rahasianya ada di sini...`,
    `Siapa bilang barang berkualitas itu susah dicari? Coba liat ${p} yang satu ini!`,
  ],
  niche: (p) => [
    `Khusus buat kamu yang pengen tampil percaya diri dan elegan seharian, sini merapat!`,
    `Panggilan buat pejuang sat-set yang butuh ${p} praktis dan anti ribet!`,
  ],
  battle: (p) => [
    `Battle jujur! Brand ternama mall vs ${p} viral keranjang kuning, kira-kira menang mana?`,
    `Gak nyangka kualitas ${p} ini berani diadu sama brand mahal ternama!`,
  ],
  transform: (p) => [
    `Perbedaan sebelum dan sesudah pakai ${p} ini beneran nyata banget!`,
    `Definisi upgrade hidup jadi lebih simpel dan nyaman semenjak ada ${p} ini!`,
  ],
};

function pickRandom(arr, exclude) {
  const filtered = exclude ? arr.filter(x => x !== exclude) : arr;
  return filtered[Math.floor(Math.random() * filtered.length)];
}

function generate({ product_input, hook_type = 'auto', strategy = 'AIDA', duration = 10, category = 'auto' }) {
  const prod = cleanProductName(product_input || '');
  const cat = (category && category !== 'auto') ? category : detectCategory(product_input || '');
  const vocab = NICHE_VOCAB[cat] || NICHE_VOCAB.general;

  const b1 = pickRandom(vocab.benefits);
  const b2 = pickRandom(vocab.benefits, b1) || b1;
  const p1 = pickRandom(vocab.pain_points);
  const pr1 = pickRandom(vocab.proofs);
  const ctas = [pickRandom(CTA_LIST)];
  for (let i = 1; i < 4; i++) ctas.push(pickRandom(CTA_LIST, ctas[ctas.length - 1]));

  // Build hook pool
  const types = Object.keys(HOOKS);
  let hPool;
  if (HOOKS[hook_type]) {
    hPool = HOOKS[hook_type](prod, b1);
  } else {
    // auto: shuffle 4 distinct hook types
    const shuffled = [...types].sort(() => Math.random() - 0.5);
    hPool = shuffled.slice(0, 4).map(t => HOOKS[t](prod, b1)[0]);
  }
  while (hPool.length < 4) hPool.push(`Lagi cari ${prod} yang terbukti kualitasnya?`);

  const v1 = `${hPool[0]} Kenalin ${prod} yang lagi hits ini. Gak cuma ${b1}, tapi ${b2}. Ditambah lagi ${pr1}. ${ctas[0]}`;
  const v2 = `${hPool[1]} ${prod} ini hadir jadi jawaban buat kamu. Rasain sendiri gimana ${b1} dengan kualitas yang gak main-main. ${ctas[1]}`;
  const v3 = `${hPool[2]} Pas dicoba, beneran juara banget karena ${b2}. Nyesel banget kalau gak tahu dari dulu. ${ctas[2]}`;
  const v4 = `${hPool[3]} Kapan lagi dapet ${prod} yang ${b1} dan beneran awet dipakai? ${ctas[3]}`;

  return {
    category_detected: cat,
    variasi_1: v1,
    variasi_2: v2,
    variasi_3: v3,
    variasi_4: v4,
    hook_types_used: [
      'Hook Tajam & Benefit Fokus',
      'Hook Solutif & Penawar Masalah',
      'Hook Storytelling & Rekomendasi Tulus',
      'Hook Urgensi & Nilai Hemat',
    ],
  };
}

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed', expect: 'POST' });

  try {
    const result = generate(req.body || {});
    return res.status(200).json(result);
  } catch (e) {
    return res.status(500).json({ error: 'generate_failed', detail: String(e).slice(0, 300) });
  }
}

export const config = { api: { bodyParser: { sizeLimit: '1mb' } } };
