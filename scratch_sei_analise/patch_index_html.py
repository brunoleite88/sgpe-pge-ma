import os

static_file = 'sgpe_app/static/index.html'
docs_file = 'docs/index.html'

with open(static_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update header badge
old_hdr = '<p class="text-xs text-slate-300">Gestão de Metas, Planos de Ação e Governança</p>'
new_hdr = '<p class="text-xs text-slate-300 flex items-center gap-2"><span>Gestão de Metas, Planos de Ação e Governança</span> <span class="px-1.5 py-0.5 rounded bg-emerald-800 text-emerald-200 text-[10px] font-semibold border border-emerald-500">v2.1 Saneado</span></p>'

assert old_hdr in text, 'old_hdr not found'
text = text.replace(old_hdr, new_hdr, 1)

# 2. Update ensureStaticBundle & caching
old_bundle = '''    const _nativeFetch = window.fetch.bind(window);
    async function ensureStaticBundle() {
      if (STATE.staticBundle) return STATE.staticBundle;
      const saved = localStorage.getItem('SGPE_STATIC_BUNDLE_V1');
      if (saved) {
        try {
          STATE.staticBundle = JSON.parse(saved);
          return STATE.staticBundle;
        } catch (e) {}
      }
      const res = await _nativeFetch('dados_sgpe.json');
      STATE.staticBundle = await res.json();
      return STATE.staticBundle;
    }

    function saveStaticBundle() {
      if (STATE.staticBundle) {
        try { localStorage.setItem('SGPE_STATIC_BUNDLE_V1', JSON.stringify(STATE.staticBundle)); } catch (e) {}
      }
    }'''

new_bundle = '''    const _nativeFetch = window.fetch.bind(window);

    // Limpeza forçada de cache antigo da versão V1
    try { localStorage.removeItem('SGPE_STATIC_BUNDLE_V1'); } catch (e) {}

    async function ensureStaticBundle(forceRefresh = false) {
      if (!forceRefresh && STATE.staticBundle) return STATE.staticBundle;

      try {
        const bust = '?v=' + Date.now();
        const res = await _nativeFetch('dados_sgpe.json' + bust, { cache: 'no-store' });
        if (res.ok) {
          STATE.staticBundle = await res.json();
          try {
            sessionStorage.setItem('SGPE_STATIC_BUNDLE_V2', JSON.stringify(STATE.staticBundle));
          } catch (e) {}
          return STATE.staticBundle;
        }
      } catch (err) {
        console.warn('Modo offline ou falha ao baixar dados_sgpe.json:', err);
      }

      const saved = sessionStorage.getItem('SGPE_STATIC_BUNDLE_V2') || localStorage.getItem('SGPE_STATIC_BUNDLE_V2');
      if (saved) {
        try {
          STATE.staticBundle = JSON.parse(saved);
          return STATE.staticBundle;
        } catch (e) {}
      }
      return STATE.staticBundle;
    }

    function saveStaticBundle() {
      if (STATE.staticBundle) {
        try {
          sessionStorage.setItem('SGPE_STATIC_BUNDLE_V2', JSON.stringify(STATE.staticBundle));
          localStorage.setItem('SGPE_STATIC_BUNDLE_V2', JSON.stringify(STATE.staticBundle));
        } catch (e) {}
      }
    }'''

# Normalize newlines for matching
text_lf = text.replace('\r\n', '\n')
old_bundle_lf = old_bundle.replace('\r\n', '\n')
assert old_bundle_lf in text_lf, 'old_bundle not found'
text_lf = text_lf.replace(old_bundle_lf, new_bundle.replace('\r\n', '\n'), 1)

# 3. Update reindex-xlsx / regenerar-relatorios
old_reindex = '''      if (path === '/api/reindex-xlsx' || path === '/api/regenerar-relatorios') {
        localStorage.removeItem('SGPE_STATIC_BUNDLE_V1');
        STATE.staticBundle = null;
        await ensureStaticBundle();
        return mockJsonResponse({ status: 'ok', message: 'Base de dados web recarregada com sucesso.' });
      }'''

new_reindex = '''      if (path === '/api/reindex-xlsx' || path === '/api/regenerar-relatorios') {
        try {
          localStorage.removeItem('SGPE_STATIC_BUNDLE_V1');
          localStorage.removeItem('SGPE_STATIC_BUNDLE_V2');
          sessionStorage.removeItem('SGPE_STATIC_BUNDLE_V2');
        } catch (e) {}
        STATE.staticBundle = null;
        await ensureStaticBundle(true);
        return mockJsonResponse({ status: 'ok', message: 'Dados recarregados com sucesso do servidor GitHub.' });
      }'''

old_reindex_lf = old_reindex.replace('\r\n', '\n')
assert old_reindex_lf in text_lf, 'old_reindex not found'
text_lf = text_lf.replace(old_reindex_lf, new_reindex.replace('\r\n', '\n'), 1)

# Convert back to CRLF
final_text = text_lf.replace('\n', '\r\n')

with open(static_file, 'w', encoding='utf-8') as f:
    f.write(final_text)

with open(docs_file, 'w', encoding='utf-8') as f:
    f.write(final_text)

print('Updated sgpe_app/static/index.html and docs/index.html successfully!')
