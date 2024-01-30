import logging
import configparser
from typing import Optional, Tuple
import wave
import nltk
import pymysql

# Ensure that NLTK 'punkt' package is downloaded
nltk.download('punkt', quiet=True)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load configurations
config = configparser.ConfigParser()
if not config.read('config.ini'):
    logging.error("Missing or corrupt 'config.ini' file.")

def transcribe_audio(audio_file: str, language: str = 'pt-BR') -> Optional[str]:
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        transcript = recognizer.recognize_google(audio_data, language=language)
        return transcript
    except Exception as e:
        logging.error(f"Error in speech recognition: {e}")
        return None

def get_audio_duration(audio_file: str) -> Optional[float]:
    try:
        with wave.open(audio_file, 'rb') as file:
            return file.getnframes() / file.getframerate()
    except Exception as e:
        logging.error(f"Error in getting audio duration: {e}")
        return None

def calculate_word_accuracy(transcript: str, reference_text: str) -> float:
    words_transcript = nltk.word_tokenize(transcript.lower())
    words_reference = nltk.word_tokenize(reference_text.lower())
    # Improved accuracy calculation
    matches = sum(1 for word in words_transcript if word in words_reference)
    return (matches / len(words_reference)) * 100 if words_reference else 0

def calculate_words_per_minute(transcript: str, audio_duration: float) -> float:
    return (len(nltk.word_tokenize(transcript.lower())) / audio_duration) * 60 if audio_duration > 0 else 0

def connect_to_db() -> Optional[pymysql.connections.Connection]:
    try:
        connection = pymysql.connect(
            host=config.get('DATABASE', 'Host'),
            port=config.getint('DATABASE', 'Port'),
            user=config.get('DATABASE', 'User'),
            password=config.get('DATABASE', 'Password'),
            db=config.get('DATABASE', 'DB')
        )
        print("Connection successful!")
        return connection
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        return None

def insert_transcription_into_db(transcription: str, accuracy: float, word_count: int, wpm: float, audio_duration: float, aluno_leitura: str, id_avaliacao: int) -> bool:
    conn = connect_to_db()
    if conn is None:
        return False
    try:
        with conn.cursor() as cursor:
            # Modify your SQL query as per your requirement
            sql = "INSERT INTO avaliacao (transcription, accuracy, word_count, wpm, audio_duration, aluno_leitura, id_avaliacao) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (transcription, accuracy, word_count, wpm, audio_duration, aluno_leitura, id_avaliacao))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error interacting with the database: {e}")
        return False
    finally:
        conn.close()

def process_audio_file(audio_file, reference_text, id_avaliacao):
    transcription = transcribe_audio(audio_file)
    if transcription:
        audio_duration = get_audio_duration(audio_file)
        if audio_duration:
            accuracy = calculate_word_accuracy(transcription, reference_text)
            wpm = calculate_words_per_minute(transcription, audio_duration)
            word_count = len(nltk.word_tokenize(transcription.lower()))
            aluno_leitura = "Nível 4 - aluno sabe ler" if accuracy == 100 else "Nível 2 - aluno tem dificuldade em ler" if 0 < accuracy < 50 else "Nível 3 - aluno quase leitor" if 50 < accuracy < 100 else "Nível 1 - aluno não sabe ler"
            insert_transcription_into_db(transcription, accuracy, word_count, wpm, audio_duration, aluno_leitura, id_avaliacao)

            logging.info(f"Audio transcription: {transcription}")
            logging.info(f"Accuracy of recognized words: {accuracy} %")
            logging.info(f"Word count: {word_count}")
            logging.info(f"Words per minute: {wpm}")
            logging.info(f"Audio duration: {audio_duration} seconds")
            logging.info(f"Índice de fluência: {aluno_leitura}")

# Example usage
reference_text = "amanhã é o último dia para a entrega do projeto"
audio_file = "teste5.wav"
id_avaliacao = 1
process_audio_file(audio_file, reference_text, id_avaliacao)
