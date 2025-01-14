import streamlit as st
from PIL import Image, ImageSequence
from io import BytesIO

st.title("🎈 GIF looper")

uploaded_files = st.file_uploader("Choose a GIF", type=["gif"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Leggi i byte del file caricato
        bytes_data = uploaded_file.read()
        gif = Image.open(BytesIO(bytes_data))
        original_duration_ms = sum(frame.info.get("duration", 0) for frame in ImageSequence.Iterator(gif))
        original_duration_sec = original_duration_ms / 1000  # Conversione in secondi

        # Mostra GIF originale nella UI
        st.image(gif, caption=f"Original GIF: {uploaded_file.name}")
        st.write(f"**Original Duration:** {original_duration_sec} sec")

        # Ottieni tutti i frame della GIF
        frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]

        # Modifica il numero di loop (esempio: 2 volte)
        loop_count = st.number_input("Set loop count (0 for infinite)", min_value=0, value=2)

        # Salva la GIF con il loop modificato in memoria
        output_gif = BytesIO()
        frames[0].save(
            output_gif,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            loop=loop_count,
        )
        output_gif.seek(0)

        modified_duration_ms = original_duration_ms * (loop_count if loop_count > 0 else 1)
        modified_duration_sec = modified_duration_ms / 1000

        st.write(f"**Modified Duration:** {modified_duration_sec} sec")


        # Mostra la GIF modificata
        st.image(output_gif, caption="Modified GIF")

        # Pulsante per scaricare la GIF modificata
        st.download_button(
            label="Download modified GIF",
            data=output_gif,
            file_name=f"modified_{uploaded_file.name}",
            mime="image/gif"
        )
