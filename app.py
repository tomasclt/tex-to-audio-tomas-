# -*- coding: utf-8 -*-
import streamlit as st
import os, time, glob, re
from gtts import gTTS
from PIL import Image

# =========================
# Config
# =========================
st.set_page_config(page_title="Audio Pro · Texto → MP3", page_icon="🎧", layout="centered")

# =========================
# Styles (Glassmorphism + Gradients)
# =========================
st.markdown("""
<style>
:root{
  --radius: 18px;
}
html, body, [class*="css"] {
  font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
}
main .block-container { max-width: 980px; padding-top: 2rem; padding-bottom: 3rem; }

/* Background gradient */
body{
  background: radial-gradient(1100px 600px at 10% 10%, #ecfeff 0%, transparent 60%),
              radial-gradient(900px 600px at 90% 0%, #eef2ff 0%, transparent 60%),
              linear-gradient(180deg,#ffffff, #f8fafc 60%);
}

/* Cards (glass) */
.card{
  backdrop-filter: blur(10px);
  background: rgba(255,255,255,.6);
  border: 1px solid rgba(2,6,23,.08);
  border-radius: var(--radius);
  box-shadow: 0 20px 50px rgba(2,6,23,.06);
  padding: 18px 20px;
}

/* Title + badge */
.header { display:flex; align-items:center; gap:.6rem; margin-bottom:.25rem; }
.badge {
  padding:.28rem .6rem; border-radius: 999px;
  background: linear-gradient(90deg,#22d3ee,#6366f1);
  color: white; font-weight: 600; font-size:.78rem;
  border: 0;
}

/* Image */
div[data-testid="stImage"] img{
  border-radius: 16px !important;
  box-shadow: 0 24px 60px rgba(2,6,23,.18);
}

/* Soft divider */
.soft-divider{ height:1px; margin: 1rem 0 1.25rem 0;
  background: linear-gradient(90deg, transparent, rgba(2,6,23,.12), transparent);
  border:0;
}

/* Inputs */
.stTextArea textarea{
  border-radius: 16px !important;
  background: #f1f5f9 !important;
  border: 1px solid rgba(2,6,23,.08) !important;
}
.stSelectbox, .stToggle, .stSlider, .stNumberInput{ border-radius: 12px !important; }

/* Buttons (pill + gradient hover) */
.stButton > button{
  border-radius: 999px;
  padding: .70rem 1.1rem;
  border: 1px solid rgba(2,6,23,.08);
  transition: all .2s ease;
  box-shadow: 0 10px 26px rgba(2,6,23,.08);
}
.stButton > button:hover{
  transform: translateY(-1px);
  box-shadow: 0 16px 40px rgba(2,6,23,.12);
}
.btn-primary button{
  background: linear-gradient(90deg,#22d3ee,#6366f1) !important;
  color: white !important; border: 0 !important;
}
.btn-ghost button{
  background: white !important;
}

/* Sidebar */
section[data-testid="stSidebar"] > div:first-child{
  background: linear-gradient(180deg, #22d3ee 0%, #6366f1 100%);
}
section[data-testid="stSidebar"] *{ color:#f8fafc !important; }

.small{ opacity:.85; font-size:.9rem; }

/* Progress bar subtile */
[data-testid="stProgressBar"] > div > div{
  background: linear-gradient(90deg,#67e8f9,#a5b4fc) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Utils
# =========================
def ensure_temp_dir(path="temp"):
  os.makedirs(path, exist_ok=True)
  return path

def slugify_filename(text, fallback="audio", max_len=40):
  base = (text or "").strip().splitlines()[0][:max_len]
  if not base: base = fallback
  base = re.sub(r"[^A-Za-z0-9 _-]", "", base)
  base = re.sub(r"\s+", "_", base)
  return base or fallback

def text_to_speech(text, lang="es", slow=False, outdir="temp"):
  ensure_temp_dir(outdir)
  tts = gTTS(text=text, lang=lang, slow=slow)   # requiere Internet
  fname = f"{slugify_filename(text)}_{int(time.time())}.mp3"
  fpath = os.path.join(outdir, fname)
  tts.save(fpath)
  return fpath

def remove_old_files(days=7, pattern="temp/*.mp3"):
  now = time.time(); cutoff = days * 86400
  for f in glob.glob(pattern):
    try:
      if os.stat(f).st_mtime < now - cutoff: os.remove(f)
    except: pass

# =========================
# Hero
# =========================
st.markdown(
  '<div class="header"><h1 style="margin:0">Audio Pro</h1>'
  '<span class="badge">Texto → MP3</span></div>',
  unsafe_allow_html=True
)
st.markdown("Convierte texto en **audio nítido** en segundos. UI moderna, proceso simple.")

# Imagen hero
with st.container():
  try:
    img = Image.open("gato_raton.png")
    st.image(img, width=380)
  except Exception:
    st.markdown('<div class="small">Sugerencia: agrega <code>gato_raton.png</code> para mostrar una imagen de portada.</div>', unsafe_allow_html=True)

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

# =========================
# Top controls (chips)
# =========================
with st.container():
  colA, colB, colC = st.columns([2.2, 1.2, 1.2])
  with colA:
    st.markdown("##### Preferencias")
    lang_label = st.selectbox("Idioma", ("Español (es)", "English (en)"), index=0)
    lang_code = "es" if "Español" in lang_label else "en"
  with colB:
    slow_voice = st.toggle("Voz lenta", value=False)
  with colC:
    # Para futuras extensiones (volumen, pitch, etc.). Por ahora placeholder.
    st.selectbox("Salida", ("MP3 • 128kbps",), index=0)

# =========================
# Text card
# =========================
FABULA = (
  "¡Ay! —dijo el ratón—. El mundo se hace cada día más pequeño. "
  "Al principio era tan grande que le tenía miedo. Corría y corría "
  "y me alegraba ver esos muros, a diestra y siniestra, en la distancia. "
  "Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto "
  "y ahí en el rincón está la trampa sobre la cual debo pasar. "
  "—Todo lo que debes hacer es cambiar de rumbo —dijo el gato… y se lo comió. "
  "Franz Kafka."
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Texto")

col1, col2 = st.columns([4, 1.6], vertical_alignment="top")
with col1:
  default_text = st.session_state.get("tts_text", "")
  text = st.text_area("Ingresa el texto a convertir", value=default_text, height=180, placeholder="Pega aquí tu texto…")
  st.session_state["tts_text"] = text
  chars = len(text or "")
  st.caption(f"Caracteres: {chars}")
  st.progress(min(chars/5000, 1.0))

with col2:
  st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
  if st.button("🧩 Usar fábula", use_container_width=True):
    st.session_state["tts_text"] = FABULA
    st.rerun()
  st.markdown('</div>', unsafe_allow_html=True)
  st.write("")
  if st.button("🧼 Limpiar", use_container_width=True):
    st.session_state["tts_text"] = ""
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Convert card
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)

# Primary button (gradient)
st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
convert = st.button("🔊 Convertir a Audio (MP3)", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

text = st.session_state.get("tts_text", "")

if convert:
  if not text or not text.strip():
    st.warning("Escribe o pega un texto antes de convertir. 😉")
  else:
    try:
      mp3_path = text_to_speech(text, lang=lang_code, slow=slow_voice, outdir="temp")
      with open(mp3_path, "rb") as f:
        audio_bytes = f.read()

      st.success("Audio generado con éxito.")
      st.markdown("#### Tu audio")
      st.audio(audio_bytes, format="audio/mp3", start_time=0)

      # Download CTA
      fname = os.path.basename(mp3_path)
      st.download_button(
        label="⬇️ Descargar MP3",
        data=audio_bytes,
        file_name=fname,
        mime="audio/mpeg",
        use_container_width=True
      )

      with st.expander("Ver texto usado"):
        st.write(text)

    except Exception as e:
      st.error(f"Algo falló al generar el audio: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Housekeeping
# =========================
def _cleanup():
  try: remove_old_files(days=7)
  except: pass
_cleanup()

# =========================
# Footer
# =========================
st.markdown(
  "<div class='small' style='text-align:center; margin-top:20px;'>"
  "Audio Pro · Streamlit + gTTS • Diseño glass ✨"
  "</div>",
  unsafe_allow_html=True
)

