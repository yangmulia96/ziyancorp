// Vercel Serverless Function: /api/feedback
export default async function handler(req, res) {
  // Allow CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const TOPIC = 'ziyancorp_narasikilat_feedback_vault_2026';

  if (req.method === 'POST') {
    try {
      const data = req.body;
      const payload = typeof data === 'string' ? JSON.parse(data) : data;

      // Forward to persistent cloud vault
      await fetch(`https://ntfy.sh/${TOPIC}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      return res.status(200).json({ status: 'success', message: 'Feedback received' });
    } catch (err) {
      return res.status(500).json({ status: 'error', message: err.message });
    }
  }

  if (req.method === 'GET') {
    try {
      const resp = await fetch(`https://ntfy.sh/${TOPIC}/json?poll=1`);
      const text = await resp.text();
      const lines = text.trim().split('\n');
      const items = [];
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const d = JSON.parse(line);
          if (d.message) {
            try {
              items.push(JSON.parse(d.message));
            } catch {
              items.push({ message: d.message, timestamp: d.time });
            }
          }
        } catch {}
      }
      return res.status(200).json({ status: 'success', total: items.length, items });
    } catch (err) {
      return res.status(500).json({ status: 'error', message: err.message });
    }
  }

  return res.status(405).json({ status: 'error', message: 'Method not allowed' });
}
