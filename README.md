# Projeto de Transcrição de Áudio e Análise de Leitura

## Descrição
Este projeto é um sistema de reconhecimento de voz que transcreve áudios e avalia a capacidade de leitura do falante. Utiliza Python para o processamento de áudio, reconhecimento de voz e interage com um banco de dados SQL para armazenar os resultados.

## Requisitos
- Python 3.x
- Bibliotecas Python: `speech_recognition`, `wave`, `nltk`, `pymysql`
- Um banco de dados SQL configurado conforme a estrutura definida no script SQL desenvolvido
- Áudios para teste

## Instalação
1. Instale Python 3.x em seu sistema.
2. Instale as bibliotecas necessárias utilizando pip:
3. Execute `nltk.download('punkt')` no Python para baixar os dados necessários do NLTK.

## Configuração do Banco de Dados
- Crie um banco de dados SQL e execute o script SQL fornecido para criar as tabelas necessárias.
- Atualize as credenciais do banco de dados no script Python (`host`, `user`, `password`, `db`).

## Uso
1. Execute o script Python.
2. O script processará os arquivos de áudio fornecidos, realizará a transcrição e calculará a acurácia, a contagem de palavras, palavras por minuto e a duração do áudio.
3. Com base na acurácia da transcrição, o sistema classificará a capacidade de leitura do falante.
4. Os resultados serão armazenados no banco de dados configurado.

## Estrutura do Código
- `transcribe_audio`: Função para transcrever o áudio.
- `get_audio_duration`: Função para calcular a duração do áudio.
- `calculate_word_accuracy`: Função para calcular a acurácia da transcrição.
- `calculate_words_per_minute`: Função para calcular palavras por minuto.
- `get_word_count`: Função para contar as palavras na transcrição.
- `insert_transcription_into_db`: Função para inserir os resultados no banco de dados.

## Limitações e Considerações
- A acurácia da transcrição depende da clareza do áudio e da precisão do serviço de reconhecimento de voz (Google Speech Recognition neste caso).
- O sistema atualmente só suporta português brasileiro.
- A interpretação da capacidade de leitura é básica e pode não refletir com precisão as habilidades reais do falante.

## Contribuições
Contribuições para o projeto são bem-vindas. Sinta-se à vontade para clonar, modificar e fazer pull requests.

## Licença
Este projeto está sob a licença MIT.
