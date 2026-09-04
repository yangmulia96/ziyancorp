// Vercel serverless: /api/feedback
// Catat saran & keluhan pengguna ke Google Sheets & notifikasi Telegram seketika 24/7.

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });

  try {
    const {
      category = 'Saran',
      sender = 'Anonim',
      message = ''
    } = req.body || {};

    if (!message || !message.trim()) {
      return res.status(400).json({ error: 'missing_message' });
    }

    const now = new Date();
    const wib = new Date(now.getTime() + 7 * 60 * 60 * 1000);
    const timeStr = wib.toISOString().replace('T', ' ').slice(0, 19) + ' WIB';

    const cleanCategory = String(category).slice(0, 50);
    const cleanSender = String(sender).slice(0, 80);
    const cleanMessage = String(message).slice(0, 1000);

    let loggedToSheet = false;

    // 1. Kirim ke Google Sheets via OAuth2 Refresh Token (Kolom terstruktur)
    const clientId = process.env.GOOGLE_CLIENT_ID;
    const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
    const refreshToken = process.env.GOOGLE_REFRESH_TOKEN;
    const sheetId = process.env.GOOGLE_SHEET_ID;

    if (clientId && clientSecret && refreshToken && sheetId) {
      try {
        const tokenResp = await fetch('https://oauth2.googleapis.com/token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            client_id: clientId,
            client_secret: clientSecret,
            refresh_token: refreshToken,
            grant_type: 'refresh_token'
          })
        });
        if (tokenResp.ok) {
          const tokenData = await tokenResp.json();
          const accessToken = tokenData.access_token;

          const row = [
            timeStr,
            `[FEEDBACK] ${cleanCategory}`,
            `Kontak: ${cleanSender}`,
            'Sumber: Form Bantuan PWA',
            'SUBMITTED',
            0,
            cleanMessage,
            '-',
            'QC Note: Perlu ditinjau / Follow-up'
          ];

          const appendUrl = `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/Sheet1!A2:I2:append?valueInputOption=USER_ENTERED`;
          const appendResp = await fetch(appendUrl, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${accessToken}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ values: [row] })
          });
          if (appendResp.ok) loggedToSheet = true;
        }
      } catch (sheetErr) {
        console.warn('[feedback] Sheet log error:', sheetErr);
      }
    }

    // 2. Kirim notifikasi instan ke Telegram Bot
    const tgToken = process.env.TELEGRAM_BOT_TOKEN;
    const tgChat = process.env.TELEGRAM_CHAT_ID;
    if (tgToken && tgChat) {
      try {
        const text = `💬 *[SARAN & KELUHAN PENGGUNA]*\n⏰ ${timeStr}\n🏷️ *Kategori:* ${cleanCategory}\n👤 *Pengirim:* ${cleanSender}\n\n📝 *Pesan:*\n${cleanMessage}`;
        await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: tgChat, text, parse_mode: 'Markdown' })
        });
      } catch (tgErr) {
        console.warn('[feedback] Telegram alert error:', tgErr);
      }
    }

    return res.status(200).json({ ok: true, logged_to_sheet: loggedToSheet, time: timeStr });
  } catch (e) {
    return res.status(500).json({ error: String(e).slice(0, 100) });
  }
}

export const config = { api: { bodyParser: { sizeLimit: '256kb' } } };
