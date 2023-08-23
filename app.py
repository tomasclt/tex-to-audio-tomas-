import streamlit as st
import os
import time
import glob
import os
from gtts import gTTS
from PIL import Image

st.title("Interfases Multimodales.")
image = Image.open('text_to_audio.png')

st.image(image, width=200)


try:
    os.mkdir("temp")
except:
    pass

st.subheader("Texto a audio.")
st.write('Las interfaces de texto a audio son fundamentales en las interfaces multimodales ya que permiten '  
         'una comunicación más accesible y natural, facilitando la inclusión de personas con discapacidades ' 
         ' visuales y permitiendo la interacción en situaciones donde no es posible leer texto. Estas interfaces '  
         ' también impulsan tecnologías emergentes como los asistentes de voz inteligentes, haciendo que la tecnología ' 
         ' sea más accesible e intuitiva para todos los usuarios')
           

text = st.text_input("Ingrese el texto.")

tld="es"

def text_to_speech(text, tld):
    
    tts = gTTS(text,"es", tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text


#display_output_text = st.checkbox("Verifica el texto")

if st.button("convertir"):
    result, output_text = text_to_speech(text, tld)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Tú audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    #if display_output_text:
    st.markdown(f"## Texto en audio:")
    st.write(f" {output_text}")


def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)
