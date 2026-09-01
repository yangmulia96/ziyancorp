# ZIYAN Blog & SEO SOP — Full Draft (mirror of disk file)

Berlaku tiap Bos minta artikel blog.

## Alur Wajib
1. Riset Basis Kompetitor: Bos kasih keyword -> cari URL kompetitor top organic.
   JANGAN google.com (recaptcha). Pakai Bing/DuckDuckGo/fetch langsung.
   `notebooklm source add -n <NB> --type url <url>`.
2. SEO Outline (NotebookLM): Judul SEO, Meta Description, H1/H2/H3, LSI, link.
3. Draft Markdown: generate report -> .md.
4. Two-Brain Polish: sub-agent 9router (gemma-4/poolside/channel-researcher), BUKAN berbayar.
5. Multimedia wajib: Infografis PNG (cover+alt), MindMap JSON (tengah), Audio (embed; SoundCloud belum ada -> YouTube/Telegram).

## Platform
- Blogger "ZYN AI co" (autopost API)
- LinkedIn carousel dari slide deck
- Jadwal <=1/hari

## Etik
- Data orisinal ZIYAN, AI disclosure, jangan janjikan cuan sebelum bukti.

## Pitfalls (8/3)
- Google recaptcha blokir riset -> Bing/DuckDuckGo/fetch
- generate report TIDAK ada --title
- download butuh subcommand + path positional
- video --format short DITOLAK CLI -> crop ffmpeg
- FREE = 3 video + 3 audio/hari
- JANGAN computer_use UI NotebookLM
