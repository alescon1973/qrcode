import streamlit as st
import qrcode
from PIL import Image
import io
import urllib.parse
import base64




st.set_page_config(page_title="QR Code Oggetto", page_icon="🔳")
st.title("Ciao Cosimo, sono il tuo generatore di QR Code 🔳")

# === Input utente ===
st.info("Qui puoi inserire una descrizione del sito che vuoi che venga visualizzato ed il suo indirizzo web", icon="ℹ️")
descrizione = st.text_area("Descrizione")
sito_url = st.text_input("Indirizzo web da visualizzare")
st.info("Se vuoi, puoi caricare una immagine che comparirà al centro del QR Code", icon="ℹ️")
# Immagine oggetto (per inserimento dentro il QR code)
uploaded_logo = st.file_uploader("Carica immagine/logo da inserire nel QR (opzionale)", type=["jpg", "png", "jpeg"])

# Dimensione QR finale
st.info("Se muovi la barra, decidi la dimensione del QR Code", icon="ℹ️")
qr_size = st.slider("Dimensione QR Code (px)", min_value=200, max_value=800, value=400, step=50)
codice = ""
nome_oggetto = ""
telefono_whatsapp = ""
email_produttore = ""
# === Costruzione dati per QR ===
if st.button("Genera QR Code"):
    dati_qr = ""
    messaggio = f"Ciao, vorrei avere informazioni riguardo {nome_oggetto}, codice {codice}."

    if telefono_whatsapp:  # WhatsApp ha priorità
        messaggio_enc = urllib.parse.quote(messaggio)
        dati_qr = f"https://wa.me/{telefono_whatsapp}?text={messaggio_enc}"

    elif sito_url:  # altrimenti Instagram
        dati_qr = sito_url

    elif email_produttore:  # altrimenti email
        dati_qr = f"mailto:{email_produttore}?subject=Info%20{urllib.parse.quote(nome_oggetto)}&body={urllib.parse.quote(descrizione)}"

    else:  # fallback: solo info oggetto
        dati_qr = f"{nome_oggetto}\n{descrizione}"

    # Generazione QR
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 🔹 Alta tolleranza per inserire un'immagine
        box_size=10,
        border=4,
    )
    qr.add_data(dati_qr)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Ridimensionamento QR
    img_qr = img_qr.resize((qr_size, qr_size), Image.LANCZOS)

    # Inserimento logo al centro
    if uploaded_logo:
        logo = Image.open(uploaded_logo).convert("RGBA")

        # Dimensione del logo: max 25% del QR
        logo_size = qr_size // 4
        logo.thumbnail((logo_size, logo_size), Image.LANCZOS)

        # Calcolo posizione centrale
        pos_x = (img_qr.size[0] - logo.size[0]) // 2
        pos_y = (img_qr.size[1] - logo.size[1]) // 2

        # Inserimento logo con trasparenza
        img_qr.paste(logo, (pos_x, pos_y), logo)

    # Mostra QR
    st.image(img_qr, caption="QR Code generato", use_container_width=False)

    # Salvataggio QR in memoria
    buf = io.BytesIO()
    img_qr.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Scarica QR Code",
        data=byte_im,
        file_name=f"qrcode_{sito_url}.png",
        mime="image/png",
    )


    # Mostra link generato
    st.markdown("### 🔗 Link incorporato nel QR Code:")
    st.code(dati_qr, language="text")
