// Vercel serverless: /api/ugc-studio
// UGC fashion studio — generate scenes tanpa API key.

function cleanProductName(text) {
  text = String(text || '').replace(/https?:\/\/\S+/g, '');
  text = text.replace(/[^\w\s\d%]/g, ' ');
  const words = text.split(/\s+/).filter(Boolean);
  if (words.length > 7) words.length = 7;
  return words.join(' ') || 'produk pilihan ini';
}

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });

  try {
    const { product_input, model_style = 'Hijab Casual Modern', setting = 'Aesthetic Cafe Outdoor' } = req.body || {};
    const prod = cleanProductName(product_input);
    let num_scenes = parseInt(req.body?.num_scenes);
    if (!Number.isFinite(num_scenes)) num_scenes = 2;
    num_scenes = Math.max(1, Math.min(3, num_scenes));

    const analysis = `Pakaian '${prod}' memiliki keunggulan visual pada cutting yang flowy, material ringan berkualitas, serta fitting yang pas di badan untuk gaya ${model_style}.`;
    const strategy = `Menarik perhatian dalam 3 detik pertama dengan gerakan jalan model natural di ${setting}, memperlihatkan jatuhnya bahan kain saat bergerak, dan menutup dengan ajakan belanja (CTA) keranjang kuning.`;

    const intros = [
      `Scene 1 dimulai dengan model berjalan masuk frame dari arah kamera 45 derajat di area ${setting}, tatapan langsung ke lensa.`,
      `Scene 2 memperlihatkan detail close-up pada bagian ${prod}, dengan pencahayaan natural golden hour.`,
      `Scene 3 menunjukkan ekspresi senyum percaya diri sambil memegang produk, memperlihatkan tekstur dan warna pakaian.`,
    ];
    const vos = [
      `Halo bestie! Lihat deh ${prod} ini, cantik banget kan? Bahannya adem dan jatuhnya bagus banget di badan.`,
      `Detail ${prod} ini yang bikin jatuh cinta: jahitan rapi, warna elegan, dan super nyaman dipakai seharian.`,
      `Gak cuma aesthetic, ${prod} ini juga multifungsi. Bisa buat hangout, kerja, atau acara spesial!`,
    ];
    const scenes = [];
    for (let i = 0; i < num_scenes; i++) {
      scenes.push({
        title: `Scene ${i + 1}`,
        duration: "5 detik",
        visual: intros[i],
        vo: vos[i],
        omni_prompt: `Cinematic vertical shot, ${model_style} model in ${setting}, ${prod}, detailed texture, soft natural light, 8k resolution, photorealistic.`,
      });
    }

    return res.status(200).json({
      product_analysis: analysis,
      promo_strategy: strategy,
      model_style_used: model_style,
      setting_used: setting,
      scenes,
    });
  } catch (e) {
    return res.status(500).json({ error: 'ugc_failed', detail: String(e).slice(0, 300) });
  }
}

export const config = { api: { bodyParser: { sizeLimit: '1mb' } } };
