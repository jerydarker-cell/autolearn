import html
import streamlit as st

CSS = """
<style>
:root{--bg:#050a13;--panel:#0c1424;--card:#0f1728;--card2:#111b2f;--ink:#eef4ff;--muted:#93a4be;--line:#1f2b42;--blue:#3b82f6;--green:#22c55e;--purple:#8b5cf6;--amber:#f59e0b;--red:#ef4444;}
html,body,[class*="css"]{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink)!important;}
.stApp{background:radial-gradient(circle at 12% 8%,rgba(34,211,238,.1),transparent 28%),radial-gradient(circle at 88% 12%,rgba(59,130,246,.12),transparent 26%),linear-gradient(180deg,#050a13 0%,#0a1120 45%,#09101c 100%);}
.main .block-container{padding-top:1rem;padding-bottom:5rem;max-width:1380px;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#08111f 0%,#0b1426 100%);border-right:1px solid #122038;} div[data-testid="stSidebar"] *{color:#e9f2ff!important;}
.hero{position:relative;overflow:hidden;color:white;border-radius:34px;padding:1.5rem;margin-bottom:1rem;background:radial-gradient(circle at 10% 12%,rgba(34,211,238,.16),transparent 24%),radial-gradient(circle at 88% 18%,rgba(34,197,94,.12),transparent 26%),linear-gradient(135deg,#0b1220 0%,#0c1424 45%,#0f1f38 100%);border:1px solid rgba(90,120,180,.18);box-shadow:0 30px 80px rgba(0,0,0,.34);}
.hero h1{font-size:clamp(2rem,4vw,3.2rem);line-height:1.05;margin:0 0 .45rem 0;letter-spacing:-.03em;color:#f8fbff;}.hero p{max-width:980px;font-size:1.03rem;color:#d7e7ff;}.hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:1rem;align-items:center;}
.card,.metric-card,.panel,.soft-card{background:var(--card);border:1px solid var(--line);border-radius:24px;box-shadow:0 14px 40px rgba(0,0,0,.24);color:var(--ink);}.card{padding:1.1rem;height:100%;}.panel{padding:1.1rem;background:linear-gradient(180deg,#0d1628,#101b2f)}.soft-card{padding:1rem;background:var(--card2)}
.metric-card{padding:1rem;background:linear-gradient(180deg,#0d1628,#101b2f)}.metric-title{color:var(--muted);font-size:.9rem}.metric-value{font-size:1.85rem;font-weight:950;margin:.1rem 0;color:#f8fbff;letter-spacing:-.03em}.muted{color:var(--muted)!important}.big-icon{font-size:2.35rem;line-height:1;margin-bottom:.35rem;}
.pill{display:inline-block;padding:.36rem .74rem;border-radius:999px;background:#12203a;color:#d9e7ff;font-weight:900;font-size:.78rem;margin-right:.35rem;margin-bottom:.35rem;border:1px solid #1d2b45}.green{background:rgba(34,197,94,.12);color:#86efac;border-color:rgba(34,197,94,.26)}.yellow{background:rgba(245,158,11,.12);color:#fcd34d;border-color:rgba(245,158,11,.26)}.red{background:rgba(239,68,68,.12);color:#fda4af;border-color:rgba(239,68,68,.26)}.purple{background:rgba(139,92,246,.12);color:#c4b5fd;border-color:rgba(139,92,246,.26)}.blue{background:rgba(59,130,246,.12);color:#93c5fd;border-color:rgba(59,130,246,.26)}
.road{position:relative;height:124px;border-radius:22px;overflow:hidden;background:linear-gradient(180deg,rgba(10,18,32,.72),rgba(10,18,32,.96));border:1px solid rgba(90,120,180,.18)}.road-lane{position:absolute;left:0;right:0;bottom:14px;height:48px;background:#0a0f1a}.road-line{position:absolute;left:-20%;bottom:36px;width:150%;height:4px;background-image:linear-gradient(90deg,transparent 0 5%,#e2e8f0 5% 10%,transparent 10% 20%);background-size:120px 100%;animation:dash 2.2s linear infinite}.drive-car{position:absolute;left:4%;bottom:39px;font-size:2.5rem;animation:drive 6.2s ease-in-out infinite alternate}.phone-panel{border:1px solid rgba(90,120,180,.18);background:linear-gradient(180deg,rgba(14,23,39,.65),rgba(14,23,39,.92));border-radius:24px;padding:1rem;}
.fin-grid{display:grid;grid-template-columns:1.35fr .65fr;gap:14px;margin:1rem 0 1.2rem 0}.fin-card{background:linear-gradient(180deg,#0c1424,#0f1728);border:1px solid #1f2b42;border-radius:28px;padding:1.1rem;box-shadow:0 16px 40px rgba(0,0,0,.28)}.fin-label{font-size:.86rem;color:#93a4be;text-transform:uppercase;letter-spacing:.12em;font-weight:800}.fin-big{font-size:3rem;font-weight:950;letter-spacing:-.04em;color:#f8fbff;margin:.25rem 0}.action-row{display:flex;gap:10px;flex-wrap:wrap;margin-top:1rem}.action-chip{padding:.7rem 1rem;border-radius:18px;background:#111b2f;border:1px solid #20314f;color:#eef4ff;font-weight:900}
.stButton>button,.stDownloadButton>button,.stLinkButton>a{border-radius:999px!important;font-weight:900!important;border:1px solid #22324f!important;background:#0f1728!important;color:#eef4ff!important} div[data-baseweb="select"]>div,.stTextInput input,.stNumberInput input,.stTextArea textarea{background:#0b1220!important;color:#eef4ff!important;border:1px solid #22324f!important;border-radius:14px!important;}
@keyframes dash{from{transform:translateX(0)}to{transform:translateX(-120px)}}@keyframes drive{from{transform:translateX(0)}to{transform:translateX(min(720px,58vw))}}@media(max-width:980px){.hero-grid,.fin-grid{grid-template-columns:1fr}.main .block-container{padding-left:.75rem;padding-right:.75rem}}

/* v15.7 Mobile Pro additions */
@media(max-width:780px){.main .block-container{padding-left:.55rem!important;padding-right:.55rem!important;padding-top:.5rem!important}.hero{border-radius:24px!important;padding:1rem!important}.fin-big{font-size:2.2rem!important}.card,.panel,.metric-card,.fin-card{border-radius:18px!important;padding:.9rem!important}.stButton>button,.stDownloadButton>button{min-height:46px!important;width:100%!important}.stTabs [data-baseweb="tab"]{padding:.42rem .65rem!important;font-size:.88rem!important}.big-icon{font-size:2rem!important}}
.deploy-note{border:1px dashed #31507e;border-radius:18px;background:#0b1220;padding:12px;color:#dbeafe}.license-card{background:linear-gradient(180deg,#0d1628,#101b2f);border:1px solid #22324f;border-radius:24px;padding:1rem;height:100%}.mini-visual{border:1px solid #243857;border-radius:18px;background:#0b1220;padding:10px}.stat-row{display:flex;gap:10px;flex-wrap:wrap}.tiny-muted{font-size:.84rem;color:#9db0c9}

.public-safe-card{border:1px solid #1f3a5f;background:linear-gradient(180deg,#0b1627,#101d33);border-radius:22px;padding:1rem;margin:.55rem 0;box-shadow:0 14px 32px rgba(0,0,0,.18)}
.safe-ok{border-left:5px solid #22c55e}.safe-warn{border-left:5px solid #f59e0b}.safe-bad{border-left:5px solid #ef4444}
.admin-tile{border:1px solid #22324f;background:#0d1628;border-radius:20px;padding:1rem;margin:.4rem 0}
.deploy-fix{border:1px dashed #31507e;background:#071225;border-radius:18px;padding:1rem;margin:.5rem 0}
@media(max-width:640px){
  .public-safe-card,.admin-tile,.deploy-fix{border-radius:16px!important;padding:.75rem!important}
  .stSelectbox,.stTextInput,.stTextArea,.stNumberInput{font-size:16px!important}
  .stButton>button,.stDownloadButton>button{min-height:48px!important;font-size:15px!important}
  .stRadio div[role="radiogroup"]{gap:8px!important}
  section[data-testid="stSidebar"] .stRadio label{padding:.3rem 0!important}
}

</style>
"""


def apply_style() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def metric_card(title, value, note="") -> None:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>{html.escape(str(title))}</div><div class='metric-value'>{html.escape(str(value))}</div><div class='muted'>{html.escape(str(note))}</div></div>", unsafe_allow_html=True)


def card(icon, title, desc, tag="") -> None:
    tag_html = f"<span class='pill blue'>{html.escape(tag)}</span>" if tag else ""
    st.markdown(f"<div class='card'><div class='big-icon'>{icon}</div><h3>{html.escape(title)}</h3><p class='muted'>{html.escape(desc)}</p>{tag_html}</div>", unsafe_allow_html=True)


def pills(items, cls="blue") -> None:
    st.markdown("".join([f"<span class='pill {cls}'>{html.escape(str(x))}</span>" for x in items]), unsafe_allow_html=True)


def speak_button(text: str, label: str = "🔊 Nghe đọc", lang: str = "vi-VN", key: str = "tts") -> None:
    import json, re
    import streamlit.components.v1 as components
    safe = json.dumps(text, ensure_ascii=False)
    skey = re.sub(r"[^a-zA-Z0-9_]", "_", str(key))
    components.html(f"""
    <div style='border:1px solid #1f2b42;border-radius:18px;padding:10px 12px;background:#0f1728;color:#eef4ff;font-family:Arial,sans-serif;'>
      <button onclick='play_{skey}()' style='border:1px solid #334155;border-radius:999px;padding:8px 12px;background:#111b2f;color:#eef4ff;font-weight:800;cursor:pointer;'>{label}</button>
      <button onclick='speechSynthesis.cancel()' style='margin-left:6px;border:1px solid #334155;border-radius:999px;padding:8px 12px;background:#111b2f;color:#eef4ff;font-weight:800;cursor:pointer;'>⏹️ Dừng</button>
      <label style='margin-left:8px;font-size:12px;color:#93a4be'>Tốc độ <input id='rate_{skey}' type='range' min='0.75' max='1.15' step='0.05' value='0.95'/></label>
    </div>
    <script>
    function play_{skey}(){{
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance({safe});
      u.lang = '{lang}'; u.rate = parseFloat(document.getElementById('rate_{skey}').value || '0.95'); u.pitch = 1.0;
      const voices = speechSynthesis.getVoices();
      const match = voices.find(v => (v.lang||'').toLowerCase().includes('{lang[:2].lower()}'));
      if(match) u.voice = match;
      window.speechSynthesis.speak(u);
    }}
    </script>
    """, height=70)


def lane_svg() -> None:
    import streamlit.components.v1 as components
    components.html("""
    <div style='border:1px solid #1f2b42;border-radius:22px;background:#0e1628;padding:10px;'>
    <svg viewBox='0 0 720 260' width='100%' height='250'>
      <rect width='720' height='260' fill='#0e1628'/><rect x='0' y='40' width='720' height='180' rx='20' fill='#334155'/>
      <line x1='0' y1='100' x2='720' y2='100' stroke='#fff' stroke-width='4' stroke-dasharray='24 18' opacity='.8'/><line x1='0' y1='160' x2='720' y2='160' stroke='#fff' stroke-width='4' stroke-dasharray='24 18' opacity='.8'/>
      <rect x='80' y='122' width='94' height='38' rx='14' fill='#f59e0b'><animate attributeName='x' values='80;180;280;380;480' dur='7s' repeatCount='indefinite'/><animate attributeName='y' values='122;122;122;92;92' dur='7s' repeatCount='indefinite'/></rect>
      <text x='127' y='146' text-anchor='middle' font-size='18' fill='white'>Xe bạn</text>
      <path d='M140 140 C210 140,260 140,320 110 C380 84,430 82,500 82' fill='none' stroke='#22c55e' stroke-width='6' stroke-dasharray='10 8'><animate attributeName='stroke-dashoffset' values='0;-180' dur='5s' repeatCount='indefinite'/></path>
      <polygon points='500,82 486,74 488,90' fill='#22c55e'/>
      <text x='32' y='30' font-size='20' fill='#e2e8f0'>↔️ Rẽ làn: gương → xi nhan → điểm mù → chuyển mượt</text>
    </svg></div>""", height=270)
