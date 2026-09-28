async function api(url, options={}) {
  options.headers = options.headers || {};
  if (options.body && !(options.body instanceof FormData)) options.headers['Content-Type'] = 'application/json';
  const response = await fetch(url, options);
  let data = {};
  try { data = await response.json(); } catch (_) { data = {detail: 'Unexpected server response'}; }
  return {ok: response.ok, status: response.status, data};
}
function showMessage(message, error=false) {
  const el=document.getElementById('formMessage'); if(!el) return;
  el.textContent=message; el.className='message '+(error?'error':'success');
}
function escapeHtml(value){return String(value??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));}
function renderLoading(){const el=document.getElementById('result');el.innerHTML='<div class="loading">Generating your plan…</div>';}
function renderResult(r){
  const el=document.getElementById('result');
  if(!r.ok){el.innerHTML=`<div class="message error">${escapeHtml(r.data.detail||'Something went wrong.')}</div>`;return;}
  const d=r.data;
  const alloc=Object.entries(d.allocation||{}).map(([k,v])=>`<div class="alloc"><span>${escapeHtml(k)}</span><b>₹${Number(v).toLocaleString('en-IN')}</b></div>`).join('');
  const cards=(d.recommendations||[]).map(x=>`<article class="rec"><div><span class="tag">${escapeHtml(x.platform)}</span><h3>${escapeHtml(x.name)}</h3><p>${escapeHtml(x.category)} · ${escapeHtml(x.reason)}</p></div><div class="rec-right"><strong>₹${Number(x.price).toLocaleString('en-IN')}</strong><a target="_blank" rel="noopener" href="${x.url}">View search ↗</a></div></article>`).join('');
  const tips=(d.tips||[]).map(x=>`<li>${escapeHtml(x)}</li>`).join('');
  el.innerHTML=`<div class="result-top"><span class="tag">${d.ai_used?'Gemini AI':'Fallback engine'}</span><h2>Your plan</h2><p>${escapeHtml(d.summary)}</p></div><div class="allocation"><h3>Suggested allocation</h3>${alloc}</div><div><h3>Recommendations</h3>${cards||'<p>No matching items found.</p>'}</div><div class="tips"><h3>Tips</h3><ul>${tips}</ul></div>`;
}
