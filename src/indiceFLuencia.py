# Esse script integra as funcionalidades de reconhecimento de fala, 
# análise de texto e interação com banco de dados. A função process_audio_file atua como o principal ponto de entrada, 
# que processa um arquivo de áudio, realiza a análise necessária e, em seguida, insere os resultados no banco de dados.

import speech_recognition as sr
import wave
import nltk
import pymysql
from datetime import datetime

nltk.download('punkt')

def transcribe_audio(audio_file: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        transcript = recognizer.recognize_google(audio_data, language='pt-BR')
        return transcript
    except Exception as e:
        print(f"Error in speech recognition: {e}")
        return None

def get_audio_duration(audio_file: str) -> float:
    try:
        with wave.open(audio_file, 'rb') as file:
            sample_rate = file.getframerate()
            num_frames = file.getnframes()
            duration = num_frames / sample_rate
            return duration
    except Exception as e:
        print(f"Error in getting audio duration: {e}")
        return None

def calculate_word_accuracy(transcript: str, reference_text: str) -> float:
    words_transcript = nltk.word_tokenize(transcript.lower())
    words_reference = nltk.word_tokenize(reference_text.lower())
    correct_words = [word for word in words_transcript if word in words_reference]
    accuracy = (len(correct_words) / len(words_reference)) * 100 if words_reference else 0
    return accuracy

def calculate_words_per_minute(transcript: str, audio_duration: float) -> float:
    words_transcript = nltk.word_tokenize(transcript.lower())
    wpm = (len(words_transcript) / audio_duration) * 60 if audio_duration > 0 else 0
    return wpm

def get_word_count(transcript: str) -> int:
    words_transcript = nltk.word_tokenize(transcript.lower())
    word_count = len(words_transcript)
    return word_count

def connect_to_db():
    return pymysql.connect(host='127.0.0.1', user='root', password='root', db='IndiceFLuencia')

def insert_transcription_into_db(transcription, accuracy, word_count, wpm, audio_duration, aluno_leitura, id_avaliacao):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            # Atualize esta query SQL conforme a estrutura do seu banco de dados
            sql = "UPDATE Avaliacao SET resultado_avaliacao=%s WHERE id_avaliacao=%s"
            cursor.execute(sql, (aluno_leitura, id_avaliacao))
        conn.commit()
    except Exception as e:
        print(f"Error interacting with the database: {e}")
    finally:
        conn.close()

def process_audio_file(audio_file, reference_text, id_avaliacao):
    transcription = transcribe_audio(audio_file)
    if transcription is not None:
        accuracy = calculate_word_accuracy(transcription, reference_text)
        audio_duration = get_audio_duration(audio_file)
        wpm = calculate_words_per_minute(transcription, audio_duration)
        word_count = get_word_count(transcription)
        aluno_leitura = "Nível 4 - aluno sabe ler" if accuracy == 100 else "Nível 2 - aluno tem dificuldade em ler" if 0 < accuracy < 50 else "Nível 3 - aluno quase leitor" if 50 < accuracy < 100 else "Nível 1 - aluno não sabe ler"
        insert_transcription_into_db(transcription, accuracy, word_count, wpm, audio_duration, aluno_leitura, id_avaliacao)
        print("Audio transcription:", transcription)
        print("Accuracy of recognized words:", accuracy, "%")
        print("Word count:", word_count)
        print("Words per minute:", wpm)
        print("Audio duration:", audio_duration, "seconds")
        print("Índice de fluência:", aluno_leitura)

# Exemplo de uso
reference_text = "amanhã é o último dia para a entrega do projeto"
audio_file = "teste5.wav"
id_avaliacao = 1  # Exemplo, substitua pelo ID real conforme seu banco de dados
process_audio_file(audio_file, reference_text, id_avaliacao)


# exemplo de saída de resultado utilizando arquivo de áudio 5

"""Palavras Tokenizadas: ['amanhã', 'é', 'o', 'último', 'dia', 'para', 'a', 'entrega', 'do', 'projeto']
Audio transcription: Amanhã é o último dia para a entrega do projeto
Accuracy of recognized words: 100.0 %
Word count: 10
Words per minute: 88.52370166910335
Audio duration: 6.7778458049886625 seconds
Índice de fluência: Nível 4 - aluno sabe ler"""
