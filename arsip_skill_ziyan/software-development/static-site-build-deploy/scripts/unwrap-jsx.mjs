import fs from 'fs';
// Usage: node unwrap-jsx.mjs path/to/File.jsx
// Rejoins string literals that were broken across lines by a hard-wrapping
// paste (LLM canvas exports). String-aware: skips comments, handles template
// literals and nested ${...} so JSX className template strings survive.
const p = process.argv[2];
let s = fs.readFileSync(p, 'utf8').replace(/\r\n/g, '\n');
let out = '';
let i = 0;
const stack = ['code'];
const braceDepth = [0];
const top = () => stack[stack.length - 1];
while (i < s.length) {
  const c = s[i];
  const st = top();
  if (st === 'sq' || st === 'dq') {
    const qc = st === 'sq' ? "'" : '"';
    if (c === '\\') { out += c + (s[i + 1] ?? ''); i += 2; continue; }
    if (c === qc) { out += c; stack.pop(); i++; continue; }
    if (c === '\n') { let j = i; while (j < s.length && /[\n\r \t]/.test(s[j])) j++; out += ' '; i = j; continue; }
    out += c; i++; continue;
  }
  if (st === 'tpl') {
    if (c === '\\') { out += c + (s[i + 1] ?? ''); i += 2; continue; }
    if (c === '`') { out += c; stack.pop(); i++; continue; }
    if (c === '$' && s[i + 1] === '{') { out += '${'; stack.push('code'); braceDepth.push(0); i += 2; continue; }
    out += c; i++; continue;
  }
  if (c === '/' && s[i + 1] === '/') { const e = s.indexOf('\n', i); const k = e === -1 ? s.length : e; out += s.slice(i, k); i = k; continue; }
  if (c === '/' && s[i + 1] === '*') { const e = s.indexOf('*/', i); const k = e === -1 ? s.length : e + 2; out += s.slice(i, k); i = k; continue; }
  if (c === "'") { stack.push('sq'); out += c; i++; continue; }
  if (c === '"') { stack.push('dq'); out += c; i++; continue; }
  if (c === '`') { stack.push('tpl'); out += c; i++; continue; }
  if (c === '{') { braceDepth[braceDepth.length - 1]++; out += c; i++; continue; }
  if (c === '}') {
    if (braceDepth[braceDepth.length - 1] === 0 && stack.length > 1) { stack.pop(); braceDepth.pop(); out += c; i++; continue; }
    braceDepth[braceDepth.length - 1]--; out += c; i++; continue;
  }
  out += c; i++;
}
fs.writeFileSync(p, out);
console.log('unwrapped ok');
