// Vercel serverless: /api/ugc-studio
// UGC Studio — generate structured scenes, prompts, and voiceovers.

function cleanProductName(text) {
  text = String(text || '').replace(/https?:\/\/\S+/g, '');
  text = text.replace(/[^\w\s\d%-]/g, ' ');
  const words = text.split(/\s+/).filter(Boolean);
  if (words.length > 7) words.length = 7;
  return words.join(' ') || 'produk pilihan ini';
}

function detectCategory(text) {
  const t = text.toLowerCase();
  if (/(baju|gamis|tunik|dress|hijab|kemeja|kaos|celana|rok|outfit|jaket|bomber|harrington|hoodie|blouse|kulot)/.test(t)) return 'fashion';
  if (/(serum|cream|krim|sunscreen|toner|lipstik|cushion|bedak|facial|glow|jerawat|skincare|parfum|lotion)/.test(t)) return 'skincare';
  if (/(sepatu|sandal|sneakers|heels|flatshoes|boots|loafers|wedges)/.test(t)) return 'shoes';
  if (/(hp|case|casing|charger|tws|headset|earphone|powerbank|kabel|holder|smartwatch|gadget|tripod)/.test(t)) return 'gadget';
  if (/(wajan|panci|blender|spatula|sapu|rak|botol|tumbler|dapur|rumah|organizer|bantal|sprei)/.test(t)) return 'home';
  if (/(snack|keripik|sambal|kopi|madu|teh|makanan|minuman|cokelat|baso|herbal)/.test(t)) return 'food';
  return 'general';
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
    const cat = detectCategory(product_input || '');
    let num_scenes = parseInt(req.body?.num_scenes);
    if (!Number.isFinite(num_scenes)) num_scenes = 2;
    num_scenes = Math.max(1, Math.min(3, num_scenes));

    let analysis = `Produk '${prod}' memiliki daya tarik visual yang kuat, finishing rapi, serta fungsi esensial untuk kebutuhan harian target audiens.`;
    let strategy = `Menangkap atensi dalam 3 detik pertama dengan visual dinamis di ${setting}, dilanjutkan sorotan detail spesifik, dan diakhiri CTA penunjuk keranjang kuning.`;

    let intros = [];
    let vos = [];
    let prompts = [];

    if (cat === 'fashion') {
      analysis = `'${prod}' memiliki keunggulan visual pada siluet fitting yang pas, jahitan rapi, serta jatuhnya material kain yang estetik saat bergerak untuk gaya ${model_style}.`;
      strategy = `Scene 1 fokus pada hook gerak jalan model (motion), Scene 2 menyorot tekstur kain dan jahitan (detail), Scene 3 pose percaya diri + ajakan checkout keranjang kuning.`;
      intros = [
        `Model (${model_style}) berjalan santai memasuki frame dengan angle 45 derajat di ${setting}, memperlihatkan siluet '${prod}' saat bergerak aktif.`,
        `Kamera macro 85mm mengambil close-up detail tekstur bahan '${prod}', memperlihatkan kerapian jahitan dan warna kain di bawah cahaya alami.`,
        `Model berpose percaya diri tersenyum ke arah lensa, memegang bagian produk sambil memberi isyarat gestur ke arah kiri bawah (keranjang kuning).`
      ];
      vos = [
        `Halo bestie! Asli, kalian wajib liat '${prod}' yang lagi kupakai ini. Bahannya jatuh, adem, dan potongannya bikin look auto rapi!`,
        `Detail bahannya beneran premium, jahitannya halus dan gak gampang kusut. Nyaman banget dipakai dari pagi sampai malam.`,
        `Gak heran ini jadi favorit banyak orang. Mumpung varian lengkap ready stock, yuk langsung amankan di keranjang kuning sekarang!`
      ];
      prompts = [
        `Vertical 9:16 video prompt, UGC aesthetic. Indonesian female model (${model_style}) walking into frame holding and wearing ${prod}, located in ${setting}. Eye-level handheld tracking shot, natural soft daylight, authentic fabric motion and realistic textures, 4k resolution, cinematic raw footage --ar 9:16`,
        `Vertical 9:16 macro detail shot. Extreme close-up focus on the fine texture and neat stitching of ${prod}, subtle rim lighting, shallow depth of field, 85mm lens, photorealistic, ultra-detailed fabric weave --ar 9:16`,
        `Vertical 9:16 influencer UGC close-up. Friendly model (${model_style}) smiling genuinely at camera while pointing towards bottom-left corner, wearing ${prod} in ${setting}. Soft golden hour light, authentic smartphone video aesthetic --ar 9:16`
      ];
    } else if (cat === 'skincare') {
      analysis = `'${prod}' menonjolkan tekstur formula yang ringan, sensasi glow natural, serta kemasan higienis yang meyakinkan calon pembeli.`;
      strategy = `Fokus pada tekstur formula saat diaplikasikan (swatch test), efek kulit lembap seketika, dan rekomendasi tulus tanpa overclaim.`;
      intros = [
        `Model menunjukkan kemasan '${prod}' di depan kamera dengan riasan wajah natural glowing di area ${setting}.`,
        `Close-up ekstrem tekstur '${prod}' diaplikasikan ke punggung tangan / pipi, memperlihatkan daya serap cepat tanpa rasa lengket.`,
        `Model tersenyum puas menyentuh pipi yang plumpy, menunjukkan kemasan produk di samping wajah dengan gestur CTA.`
      ];
      vos = [
        `Jujur kaget banget nemu formula '${prod}' ini! Sekali oles langsung kerasa lembap dan enteng banget di kulit.`,
        `Teksturnya seringan air, cepat meresap tanpa bikin muka berminyak atau gerah. Kandungannya beneran bikin kulit auto plumpy!`,
        `Buat kamu yang mau kulit sehat terawat tanpa ribet, langsung checkout '${prod}' ini di keranjang kuning mumpung lagi promo ya!`
      ];
      prompts = [
        `Vertical 9:16 skincare UGC video. Indonesian female model with natural radiant dewy skin, holding ${prod} bottle up to the camera in ${setting}. Soft diffused studio lighting, authentic beauty creator aesthetic, crisp 4k --ar 9:16`,
        `Vertical 9:16 macro texture swatch. Extreme close-up of ${prod} formula droplet sliding smoothly on skin, glowing translucent texture, high-speed camera capture, crystal clear clarity, commercial skincare editorial --ar 9:16`,
        `Vertical 9:16 authentic testimonial shot. Smiling model touching hydrated glowing cheek, holding ${prod}, casual friendly interaction, natural indoor morning sunlight --ar 9:16`
      ];
    } else if (cat === 'shoes') {
      analysis = `'${prod}' memiliki daya tarik pada bantalan sol empuk, fleksibilitas saat melangkah, dan siluet modern yang cocok untuk berbagai outfit.`;
      strategy = `Demonstrasikan kelenturan sol (bend test), kenyamanan saat melangkah di lantai, dan perpaduan gaya (outfit matching).`;
      intros = [
        `Kamera low-angle tracking model melangkah percaya diri mengenakan '${prod}' di area ${setting}, menonjolkan siluet sepatu.`,
        `Tangan model memegang '${prod}', mendemonstrasikan kelembutan bantalan insole empuk dan detail kerapian material sol.`,
        `Model berdiri santai sambil melihat ke kamera, memperlihatkan look keseluruhan yang stylish dipadu '${prod}', menutup dengan ajakan belanja.`
      ];
      vos = [
        `Akhirnya nemu juga '${prod}' yang beneran empuk kayak nginjak awan! Dipakai jalan seharian kaki bebas pegal dan lecet.`,
        `Liat sendiri fleksibilitas sol dan bantalannya, empuk maksimal dan sol bawahnya anti-slip aman banget di segala medan.`,
        `Biar outfit harianmu makin keren dan kaki tetap nyaman, yuk langsung klik keranjang kuning sebelum ukuran favoritmu habis!`
      ];
      prompts = [
        `Vertical 9:16 footwear dynamic shot. Low angle tracking shot of model walking gracefully wearing ${prod} on polished floor at ${setting}. Cinematic depth of field, crisp shoe details, realistic natural lighting --ar 9:16`,
        `Vertical 9:16 close-up product demonstration. Hands gently bending ${prod} to showcase flexible cushioned sole and premium stitching, 4k ultra-sharp product showcase --ar 9:16`,
        `Vertical 9:16 full outfit UGC view. Model posing confidently styled with ${prod}, natural candid posture, lifestyle influencer vibe --ar 9:16`
      ];
    } else if (cat === 'gadget') {
      analysis = `'${prod}' menonjolkan build quality presisi, desain futuristik minimalis, serta kemudahan pengoperasian plug-and-play.`;
      strategy = `Unboxing kilat, unjuk fitur fisik dalam 3 detik, dan peragaan kepraktisan penggunaan harian.`;
      intros = [
        `Kamera merekam tangan membuka packaging '${prod}' di meja bernuansa minimalis dengan pencahayaan estetik.`,
        `Detail close-up 360 derajat bodi '${prod}', memperlihatkan port, tombol sentuh, serta finishing material doff/metalik.`,
        `Model menggunakan '${prod}' dalam aktivitas nyata, tersenyum puas menikmati kepraktisannya dan mengarahkan ke keranjang kuning.`
      ];
      vos = [
        `Ini dia upgrade wajib bulan ini! Kenalin '${prod}' yang desainnya compact dan teknologinya beneran mempermudah hidup.`,
        `Materialnya kokoh presisi, koneksinya super responsif tanpa delay, dan baterainya awet banget dipakai kerja maupun santai.`,
        `Daripada beli barang abal-abal, mending amankan '${prod}' original ini sekarang di keranjang kuning ya bestie!`
      ];
      prompts = [
        `Vertical 9:16 tech unboxing shot. Overhead clean desk view with hands unboxing ${prod} in modern minimalist workspace. Soft ambient studio lighting, crisp product reflections, 4k macro --ar 9:16`,
        `Vertical 9:16 close-up tech showcase. Slow rotation showing premium matte metallic finish and precise ports of ${prod}, cinematic slow motion, shallow depth of field --ar 9:16`,
        `Vertical 9:16 authentic user test. Model happily interacting with ${prod} in daily routine, modern lifestyle aesthetic, 4k --ar 9:16`
      ];
    } else {
      intros = [
        `Scene 1 dimulai dengan model memperlihatkan '${prod}' secara langsung ke arah lensa kamera di area ${setting}.`,
        `Scene 2 memperlihatkan detail close-up pada bagian fitur utama '${prod}', dengan pencahayaan natural yang tajam.`,
        `Scene 3 menunjukkan ekspresi senyum puas sambil memegang produk, memberikan gestur rekomendasi ke arah keranjang kuning.`
      ];
      vos = [
        `Pernah gak sih butuh '${prod}' yang beneran berkualitas dan awet? Sini aku kasih liat produk rekomendasi terbaik yang satu ini!`,
        `Kualitas materialnya beneran di atas ekspektasi: rapi, kokoh, dan super praktis dipakai setiap hari.`,
        `Jangan sampai nyesel kehabisan stok ya, langsung klik keranjang kuning di bawah sekarang sebelum kehabisan!`
      ];
      prompts = [
        `Vertical 9:16 UGC video shot. Friendly presenter holding ${prod} in ${setting}. Eye-level natural handheld camera, bright daylight, clear product visibility, photorealistic --ar 9:16`,
        `Vertical 9:16 macro commercial shot. Detailed close-up of ${prod} showing durability and fine finish, 85mm lens portrait, sharp focus --ar 9:16`,
        `Vertical 9:16 call to action shot. Creator smiling approvingly with thumbs up holding ${prod}, pointing towards bottom left corner, 4k --ar 9:16`
      ];
    }

    const phases = ['Hook Pembuka (0-5s)', 'Sorotan Benefit & Detail (5-10s)', 'Call To Action & Checkout (10-15s)'];
    const scenes = [];
    let scriptTextArr = [
      `=== STORYBOARD LENGKAP UGC VIDEO: ${prod.toUpperCase()} ===`,
      `Kategori: ${cat.toUpperCase()} | Gaya Model: ${model_style} | Latar: ${setting}`,
      `------------------------------------------------------------`
    ];
    let promptTextArr = [
      `// BATCH PROMPT AI GENERATOR (MIDJOURNEY / KLING / LUMA / RUNWAY)`,
      `// Produk: ${prod} (Gaya: ${model_style})`,
      `------------------------------------------------------------`
    ];

    for (let i = 0; i < num_scenes; i++) {
      const sceneObj = {
        scene_num: i + 1,
        title: `Scene ${i + 1}`,
        phase: phases[i] || `Scene ${i + 1}`,
        duration: "5 Detik",
        visual: intros[i],
        vo: vos[i],
        omni_prompt: prompts[i],
      };
      scenes.push(sceneObj);

      scriptTextArr.push(`\n[${sceneObj.title.toUpperCase()}: ${sceneObj.phase}]`);
      scriptTextArr.push(`Visual: ${sceneObj.visual}`);
      scriptTextArr.push(`Voiceover: "${sceneObj.vo}"`);
      scriptTextArr.push(`Prompt AI: ${sceneObj.omni_prompt}`);

      promptTextArr.push(`\n[SCENE ${i + 1}: ${sceneObj.phase}]`);
      promptTextArr.push(sceneObj.omni_prompt);
    }

    return res.status(200).json({
      product_name: prod,
      category_detected: cat,
      product_analysis: analysis,
      promo_strategy: strategy,
      model_style_used: model_style,
      setting_used: setting,
      scenes,
      copyable_script: scriptTextArr.join('\n'),
      copyable_prompts: promptTextArr.join('\n'),
    });
  } catch (e) {
    return res.status(500).json({ error: 'ugc_failed', detail: String(e).slice(0, 300) });
  }
}

export const config = { api: { bodyParser: { sizeLimit: '1mb' } } };
