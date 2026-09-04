// Vercel serverless: /api/telemetry
// Catat log QC aktivitas NarasiKilat PWA ke Google Sheets & Telegram secara otomatis 24/7.

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });

  try {
    const {
      feature = 'Umum',
      input = '-',
      params = '-',
      status = 'SUCCESS',
      latency_ms = 0,
      output_summary = '-',
      error = '-'
    } = req.body || {};

    const now = new Date();
    // Offset +7 jam untuk Waktu Indonesia Barat (WIB)
    const wib = new Date(now.getTime() + 7 * 60 * 60 * 1000);
    const timeStr = wib.toISOString().replace('T', ' ').slice(0, 19) + ' WIB';

    const cleanInput = String(input).slice(0, 300);
    const cleanParams = String(params).slice(0, 200);
    const cleanOutput = String(output_summary).slice(0, 400);
    const cleanError = error ? String(error).slice(0, 300) : '-';

    let loggedToSheet = false;

    // 1. Kirim ke Google Sheets via OAuth2 Refresh Token
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
            feature,
            cleanInput,
            cleanParams,
            status,
            latency_ms,
            cleanOutput,
            cleanError,
            status === 'SUCCESS' ? 'Auto-Logged QC: Normal' : 'Auto-Logged QC: Perlu Review'
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
          if (appendResp.ok) {
            loggedToSheet = true;
          }
        }
      } catch (sheetErr) {
        console.warn('[telemetry] Sheet log error:', sheetErr);
      }
    }

    // 2. Jika ada ERROR, kirim notifikasi darurat ke Telegram
    const tgToken = process.env.TELEGRAM_BOT_TOKEN;
    const tgChat = process.env.TELEGRAM_CHAT_ID;
    if (status === 'ERROR' && tgToken && tgChat) {
      try {
        const text = `🚨 *[QC ALERT NARASIKILAT]*\n⏰ ${timeStr}\n🎯 Fitur: ${feature}\n📦 Input: ${cleanInput}\n❌ Error: ${cleanError}`;
        await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: tgChat, text, parse_mode: 'Markdown' })
        });
      } catch (tgErr) {
        console.warn('[telemetry] Telegram alert error:', tgErr);
      }
    }

    return res.status(200).json({ ok: true, logged_to_sheet: loggedToSheet, time: timeStr });
  } catch (e) {
    return res.status(200).json({ ok: false, error: String(e).slice(0, 100) });
  }
}

export const config = { api: { bodyParser: { sizeLimit: '256kb' } } };
