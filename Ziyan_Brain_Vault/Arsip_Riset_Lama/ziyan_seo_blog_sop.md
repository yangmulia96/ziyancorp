# ZIYAN — SOP Blog & SEO (berlaku tiap minta artikel blog)

## Alur Wajib (setiap artikel)
1. **Riset Basis Kompetitor**
   - Bos kasih keyword -> cari URL artikel kompetitor peringkat atas.
   - CATATAN TEKNIS: jangan pakai google.com (bot-blocked/recaptcha).
     Pakai Bing/DuckDuckGo atau fetch langsung domain.
   - Masukkan URL sebagai `notebooklm source add --type url <url>` (bukan acak).

2. **SEO Outline (NotebookLM)**
   - Perintah generate kerangka: Judul SEO, Meta Description, H1/H2/H3,
     LSI Keywords, saran internal/external link.

3. **Draft Markdown**
   - Generate report -> format .md (struktur rapi saat upload blog).

4. **Two-Brain Polish**
   - Jika draf kaku -> masukkan ke sub-agent 9router (gemma-4/poolside/channel-researcher)
     untuk natural tone. BUKAN Claude/ChatGPT berbayar (ZIYAN pakai free 9router).

5. **Aset Multimedia Wajib (embed di blog)**
   - Cover: Infografis PNG (NotebookLM) + Alt Text SEO.
   - Mind Map JSON: embed di tengah artikel (kalau bahas sistem).
   - Audio Overview: embed player. CATATAN: SoundCloud BELUM ada akun ->
     sementara embed dari YouTube (video IonQ) atau Telegram voice note.
     BUTUH Bos sediakan akun SoundCloud kalau wajib.

## Platform Blog ZIYAN
- Blogger: "ZYN AI co" (ziyancorp.blogspot.com) -> autopost via API.
- LinkedIn: carousel dari slide deck.
- Jadwal: <=1 artikel/hari (anti AdSense NOV/scaled-content).

## Etik
- Pakai data orisinal ZIYAN (riset kita), bukan rekap web umum.
- Wajib AI disclosure.
- Jangan janjikan cuan sebelum ada bukti sendiri.
