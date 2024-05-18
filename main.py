from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import PlainTextResponse
import speech_recognition as sr
import audioread
import wave
import os 
import tempfile
from googletrans import Translator
import requests
import base64

from gtts import gTTS

########=================#########
import firebase_admin
from firebase_admin import credentials, storage
import datetime

cred = credentials.Certificate("credentials.json") # fill the file "credentials.json" with your information

firebase_admin.initialize_app(cred, {
    'storageBucket': 'Place_your_Bucket_yere' 
})

def upload_to_firebase(file_path):

    bucket = storage.bucket()
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    destination_blob_name = f"audios_senia/{current_time}.mp4"
    
    blob = bucket.blob(destination_blob_name)

    # Uploader le fichier
    blob.upload_from_filename(file_path)

    # Rendre le fichier accessible publiquement
    blob.make_public()

    # Obtenir l'URL de téléchargement
    return blob.public_url

########=================#########


api_key = "your_key_here"

def convert_to_wav(audio_file_path, wav_file_path):
    with audioread.audio_open(audio_file_path) as source:
        with wave.open(wav_file_path, 'w') as destination:
            destination.setnchannels(source.channels)
            destination.setframerate(source.samplerate)
            destination.setsampwidth(2)

            for buffer in source:
                destination.writeframes(buffer)

def audio_to_text(wav_file_path):
    r = sr.Recognizer()
    
    with sr.AudioFile(wav_file_path) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio, language='fr-FR')
        return text
    except sr.UnknownValueError:
        return "Google Web Speech API n'a pas pu comprendre l'audio"
    except sr.RequestError as e:
        return f"Impossible d'obtenir les résultats de Google Web Speech API; {e}"

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')


def transcrire_yoruba(filename):
    try:
        API_URL = "https://api-inference.huggingface.co/models/neoform-ai/whisper-medium-yoruba"
        headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxx"} ## Place your token Huggingface here

        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")
    
def read_yo(texte):
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-yor"
    headers = {"Authorization": "Bearer hf_xxxxxxxxxxxx"} ## Place your token Huggingface here

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    audio_bytes = query({
        "inputs": texte,
    })
    # Save the audio to a file
    with open("output_yo.mkv", "wb") as file:
        file.write(audio_bytes)


##===================================## 
#    Les routes de l'API

app = FastAPI()

@app.get("/")
def great():
    return {"Message" : "Bienvenue dans notre API E-Tourist !"}

@app.post("/audio_to_text/")
async def convert_audio_francais_to_texte_francais(file: UploadFile = File(...)):
    try : 
        audio_data = await file.read()

        # Utiliser un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_audio_file_path = temp_audio_file.name

        # Chemin pour le fichier WAV converti
        temp_wav_file_path = tempfile.mktemp(suffix=".wav")

        convert_to_wav(temp_audio_file_path, temp_wav_file_path)
        response = audio_to_text(temp_wav_file_path)

        # Nettoyage des fichiers temporaires
        os.remove(temp_audio_file_path)
        os.remove(temp_wav_file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")

    return {"text": response}


@app.post("/texte_en_to_texte_fr/")
def traduire_anglais_to_francais(texte):
    traducteur = Translator()
    traduction = traducteur.translate(texte, src='en', dest='fr')
    trad = traduction.text
    return {"text" : trad}

@app.post("/texte_fr_to_texte_en/")
def traduire_francais_to_anglais(texte):
    traducteur = Translator()
    traduction = traducteur.translate(texte, src='fr', dest='en')
    trad = traduction.text
    return {"text" : trad}

@app.post("/texte_fr_to_texte_yo/")
def traduire_francais_to_yoruba(texte):
    try:
        traducteur = Translator()
        traduction = traducteur.translate(texte, src='fr', dest='yo')
        trad = traduction.text
        return {"text" : trad}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")

@app.post("/texte_yo_to_texte_fr/")
def traduire_yoruba_to_francais(texte):
    try:
        traducteur = Translator()
        traduction = traducteur.translate(texte, src='yo', dest='fr')
        trad = traduction.text
        return {"text" : trad}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")


@app.post("/transcribe_fongbe")
async def transcribe_fongbe(file: UploadFile = File(...)):

    try:
        API_URL = "https://api-inference.huggingface.co/models/chrisjay/fonxlsr"
        headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxx"}  ## Place your token Huggingface here

        data = await file.read()
        
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")


@app.post("/transcribe_yoruba")
async def transcribe_yoruba(file: UploadFile = File(...)):

    try:
        API_URL = "https://api-inference.huggingface.co/models/neoform-ai/whisper-medium-yoruba"
        headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxx"} ## Place your token Huggingface here

        data = await file.read()

        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")


context = "Tu es un guide touristique du Bénin. Je vais te montrer des images de monuments béninois, et tu dois me dire à quel monument cela correspond."

@app.post("/describe_monument")
async def transcribe_monument(file: UploadFile = File(...)):
    try:

        # Getting the base64 string
        base64_image = encode_image(file.file)

        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": context + "Identifie ce monument et raconte moi son histoire"
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                    }
                ]
                }
            ],
            "max_tokens": 500
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        texte_francais = response.json()['choices'][0]['message']['content']

        ## On traduit maintenant 

        translator = Translator()

        # Traduction en anglais
        texte_anglais = translator.translate(texte_francais, src='fr', dest='en').text

        # Traduction en espagnol
        texte_espagnol = translator.translate(texte_francais, src='fr', dest='es').text

        # Traduction en yoruba
        texte_yoruba = translator.translate(texte_francais, src='fr', dest='yo').text

        return {
                    'francais': texte_francais,
                    'anglais': texte_anglais,
                    'espagnol': texte_espagnol,
                    'yoruba': texte_yoruba
                }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")


@app.post("/audio_fr_to_audio_yo")
async def convert_audio_fr_to_audio_yoruba(file: UploadFile = File(...)):
    try : 
        audio_data = await file.read()

        # Utiliser un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_audio_file_path = temp_audio_file.name

        # Chemin pour le fichier WAV converti
        temp_wav_file_path = tempfile.mktemp(suffix=".wav")

        convert_to_wav(temp_audio_file_path, temp_wav_file_path)
        response_fr = audio_to_text(temp_wav_file_path)

        # Nettoyage des fichiers temporaires
        os.remove(temp_audio_file_path)
        os.remove(temp_wav_file_path)

        translator = Translator()

        response_yoruba = translator.translate(response_fr, src='fr', dest='yo').text

        read_yo(response_yoruba)

        output_audio_path="output_yo.mkv"
        firebase_url = upload_to_firebase(output_audio_path)

        return {"text": response_yoruba,
                "link": firebase_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")
    
    
@app.post("/audio_yo_to_audio_fr/")
async def convert_audio_yo_to_audio_fr(file: UploadFile = File(...)):
    try : 
        audio_data = await file.read()

        # Utiliser un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_audio_file_path = temp_audio_file.name

        # Chemin pour le fichier WAV converti
        temp_wav_file_path = tempfile.mktemp(suffix=".wav")

        convert_to_wav(temp_audio_file_path, temp_wav_file_path)
        response_yo_json = transcrire_yoruba(temp_wav_file_path)

        response_yo = response_yo_json['text']

        # Nettoyage des fichiers temporaires
        os.remove(temp_audio_file_path)
        os.remove(temp_wav_file_path)

        translator = Translator()

        response_fr = translator.translate(response_yo, src='yo', dest='fr').text

        # Convertir le texte en parole et enregistrer en local sous "output.wav"
        
        tts = gTTS(response_fr, lang='fr')
        output_audio_path = "audio_output.wav"
        tts.save(output_audio_path)
        
        firebase_url = upload_to_firebase(output_audio_path)

        return {"text": response_fr, 
                "link": firebase_url }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur est survenue : {e}")


