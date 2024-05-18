# Orile API README

The link to access Api online is : "http://ec2-3-8-117-75.eu-west-2.compute.amazonaws.com:8000"

## Overview
The Orile API is designed to facilitate various language processing tasks, including audio transcription, translation, and text-to-speech conversion, specifically for tourists exploring Benin. The API integrates multiple services such as Google Translate, Google Text-to-Speech (gTTS), and Hugging Face models, as well as Firebase for file storage and retrieval.

## Features
1. **Audio to Text Conversion (French)**: Convert audio files to French text.
2. **Text Translation**: Translate text between English, French, and Yoruba.
3. **Audio Transcription**: Transcribe audio in Yoruba and Fongbe languages.
4. **Monument Description**: Identify and describe Beninese monuments from images.
5. **Audio Translation**: Convert French audio to Yoruba audio and vice versa.

## Setup and Installation

### Prerequisites
- Python 3.7+
- Virtual Environment (recommended)

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Firebase Setup
1. Place your Firebase service account key JSON file as `credentials.json` in the root directory.
2. Configure your Firebase storage bucket name in the `firebase_admin.initialize_app()` function.

### Running the API
```bash
uvicorn main:app --reload
```

## API Endpoints

### Home
- **GET** `/`
  - Response: Welcome message.

### Audio to Text (French)
- **POST** `/audio_to_text/`
  - Request: UploadFile (audio file)
  - Response: Transcribed text in French.

### Text Translation
- **POST** `/texte_en_to_texte_fr/`
  - Request: Text (English)
  - Response: Translated text in French.
  
- **POST** `/texte_fr_to_texte_en/`
  - Request: Text (French)
  - Response: Translated text in English.

- **POST** `/texte_fr_to_texte_yo/`
  - Request: Text (French)
  - Response: Translated text in Yoruba.

- **POST** `/texte_yo_to_texte_fr/`
  - Request: Text (Yoruba)
  - Response: Translated text in French.

### Audio Transcription
- **POST** `/transcribe_fongbe`
  - Request: UploadFile (audio file)
  - Response: Transcribed text in Fongbe.

- **POST** `/transcribe_yoruba`
  - Request: UploadFile (audio file)
  - Response: Transcribed text in Yoruba.

### Monument Description
- **POST** `/describe_monument`
  - Request: UploadFile (image file)
  - Response: Description of the monument in French, English, Spanish, and Yoruba.

### Audio Translation
- **POST** `/audio_fr_to_audio_yo`
  - Request: UploadFile (audio file)
  - Response: Translated text and link to Yoruba audio file.

- **POST** `/audio_yo_to_audio_fr/`
  - Request: UploadFile (audio file)
  - Response: Translated text and link to French audio file.

## Firebase Integration
Files are uploaded to Firebase storage, and the URLs of the uploaded files are returned in API responses.

## Error Handling
The API uses `HTTPException` to handle errors. Common errors include issues with audio processing, file handling, and external API requests. Each endpoint handles exceptions and returns appropriate error messages.

## Future Improvements
- Enhance error handling for more robust API performance.
- Add support for more languages and transcription models.
- Implement user authentication for secured API access.

## License
This project is licensed under the MIT License.

---

This README provides a comprehensive overview of the Orile API, its features, setup instructions, and endpoint descriptions. For detailed usage and examples, refer to the API documentation or source code comments.
