# -*- coding: utf-8 -*-
import streamlit as st
import os
import time
import glob
import re
from io import BytesIO
from gtts import gTTS
from PIL import Image

# -----------------------------------------------------------------------------
# Configuración de página
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Audio", page_icon="🎧", layout="centered")

# -----------------------------------------------------------------------------
# Estilos (solo estética)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
  font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial, 'Noto Sans';
}
main .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 900px; }

/* Título y badge */
.header { display:flex; align-items:center; gap:.6rem; margin-bottom:.25rem; }
.badge {
  font-size:.75rem; padding:.25rem .55rem; border-radius:999px;
  background:#E6FFFA; color:#0F766E; border:1px solid #99F6E4; font-weight:600;
}

/* Tarjetas */
.card {
  background:#ffffff; border:1px solid rgba(0,0,0,0.06); border-radius:18px;
  padding:18px 20px; box-shadow:0 10px 30px rgba(0,0,0,0.06);
}

/* “Hero” imagen centrada y con sombra */
div[data-testid="stImage"] img {
  border-radius:18px !important;
  box-shadow: 0 20px 50px rgba(2,6,23,.15);
}

/* Separador suave */
.soft-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,0,0,.08), transparent);
  margin: 1rem 0 1.25rem 0;
  border: 0;
}

/* Botones más elegantes */
.stButton > button {
  border-radius: 999px;
  padding: .65rem 1rem;
  border: 1px solid rgba(0,0,0,.08);
  box-shadow: 0 6px 16px rgba(2,6,23,.06);
}

/* Inputs */
textarea, .stTextArea textarea {
  border-radius: 16px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] > div:first-child {
  background: linear-gradient(180deg, #22d3ee 0%, #6366f1 100%);
}
section[data-testid="stSidebar"] * { color: #f7faff !important; }

.small { opacity:.85; font-size:.9rem; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Utilidades
# -----------------------------------------------------------------------------
def ensure_temp_dir(path="temp"):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass
    return path

def slugify_filename(text, fallback="audio", max_len=40):
    base = (text or "").strip().splitlines()[0][:max_len]
    if not base:
        base = fallback
    base = re.sub(r"[^A-Za-z0-9 _-]", "", base)
    base = re.sub(r"\s+", "_", base)
    return base or fallback

def text_to_speech(text, lang="es", slow=False, outdir="temp"):
    ensure_temp_dir(outdir)
    tts = gTTS(text=text, lang=lang, slow=slow)  # requiere conexión
    fname = slugify_filename(text)
    fname = f"{fname}_{int(time.time())}.mp3"
    fpath = os.path.join(outdir, fname)
    tts.save(fpath)
    return fpath

def remove_old_files(days=7, pattern="temp/*.mp3"):
    mp3_files = glob.glob(pattern)
    if not mp3_files:
        return
    now = time.time()
    cutoff = days * 86400
    for f in mp3_files:
        try:
            if os.stat(f).st_mtime < now - cutoff:
                os.remove(f)
        except Exception:
            pass

# -----------------------------------------------------------------------------
# Cabecera / Hero
# -----------------------------------------------------------------------------
st.markdown(
    '<div class="header"><h1>Audio</h1><span class="badge">Texto → MP3</span></div>',
    unsafe_allow_html=True
)
st.markdown("Escribe o pega un texto, elige idioma y conviértelo a **MP3** en un clic. Sin drama.")

# Imagen “hero” centrada
with st.container():
    try:
        img = Image.open("gato_raton.png")
        st.image(img, width=360, caption=None)
    except Exception:
        st.markdown('<div class="small">Tip: añade <code>gato_raton.png</code> en el directorio para mostrar una imagen.</div>', unsafe_allow_html=True)

# Separador limpio
st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.subheader("Escucha tu texto")
    lang_label = st.selectbox("Idioma", ("Español (es)", "English (en)"))
    lang_code = "es" if "Español" in lang_label else "en"
    slow_voice = st.toggle("Voz lenta", value=False)
    st.markdown("---")
    st.markdown("#### Tips")
    st.markdown("- Para textos largos, conviértelos por partes.\n- Usa signos de puntuación para mejor entonación.\n- Revisa el nombre del archivo al descargar.")

# -----------------------------------------------------------------------------
# Texto + acciones
# -----------------------------------------------------------------------------
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

# Layout más limpio: texto a la izquierda, acciones a la derecha (botones agrupados)
col_a, col_b = st.columns([4, 1.6])
with col_a:
    default_text = st.session_state.get("tts_text", "")
    text = st.text_area("Ingresa el texto a convertir", value=default_text, height=180, placeholder="Pega aquí tu texto…")
    st.session_state["tts_text"] = text  # persistencia ligera
    chars = len(text or "")
    st.caption(f"Caracteres: {chars}")
    # Indicador visual de longitud (aprox límite práctico 5k)
    st.progress(min(chars / 5000, 1.0))

with col_b:
    if st.button("Usar fábula de ejemplo", use_container_width=True):
        st.session_state["tts_text"] = FABULA
        st.rerun()
    st.write("")  # pequeño espaciado
    if st.button("Limpiar", use_container_width=True):
        st.session_state["tts_text"] = ""
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Acción: convertir
# -----------------------------------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
convert = st.button("🔊 Convertir a Audio (MP3)", use_container_width=True)

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

            # Botón de descarga
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

# -----------------------------------------------------------------------------
# Limpieza de archivos antiguos
# -----------------------------------------------------------------------------
remove_old_files(days=7)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown(
    "<div class='small' style='text-align:center; margin-top:24px;'>"
    "Hecho con Streamlit + gTTS • UI pulida ✨"
    "</div>",
    unsafe_allow_html=True
)
