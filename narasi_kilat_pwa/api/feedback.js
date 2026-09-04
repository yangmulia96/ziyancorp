// Vercel serverless: /api/feedback
// Catat feedback ke Vercel KV / log file. Karena Vercel KV butuh setup,
// kita simpan sementara di log stdout + response sederhana.

const FEEDBACK_LOG = []; // in-memory per cold-start (cukup untuk demo)

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();

  if (req.method === 'GET') {
    return res.status(200).json({ status: 'success', total: FEEDBACK_LOG.length, items: FEEDBACK_LOG });
  }
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });

  try {
    const text = String((req.body && req.body.text) || '').slice(0, 1000);
    if (!text) return res.status(400).json({ error: 'missing_text' });
    const item = { timestamp: new Date().toISOString(), text };
    FEEDBACK_LOG.push(item);
    console.log('[feedback]', item);
    return res.status(200).json({ ok: true, count: FEEDBACK_LOG.length });
  } catch (e) {
    return res.status(500).json({ error: 'feedback_failed', detail: String(e).slice(0, 200) });
  }
}

export const config = { api: { bodyParser: { sizeLimit: '256kb' } } };
