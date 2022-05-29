import requests
import time
import streamlit as st
import os

openai_api_key = os.environ["OPENAI_AUTH_TOKEN"]
aai_api_key = os.environ["AAI_AUTH_TOKEN"]
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"


# Uploads a file to AAI servers
@st.cache
def upload_file(audio_file, header):
    upload_response = requests.post(
        upload_endpoint,
        headers=header, data=audio_file
    )
    return upload_response.json()


# Request transcript for file uploaded to AAI servers
@st.cache
def request_transcript(upload_url, header):
    transcript_request = {
        'audio_url': upload_url['upload_url']
    }
    transcript_response = requests.post(
        transcript_endpoint,
        json=transcript_request,
        headers=header
    )
    return transcript_response.json()


# Make a polling endpoint
@st.cache
def make_polling_endpoint(transcript_response):
    polling_endpoint = "https://api.assemblyai.com/v2/transcript/"
    polling_endpoint += transcript_response['id']
    return polling_endpoint


# Wait for the transcript to finish
@st.cache
def wait_for_completion(polling_endpoint, header):
    while True:
        polling_response = requests.get(polling_endpoint, headers=header)
        polling_response = polling_response.json()

        if polling_response['status'] == 'completed':
            break

        time.sleep(5)


# Get the paragraphs of the transcript
def get_paragraphs(polling_endpoint, header):
    paragraphs_response = requests.get(polling_endpoint + "/paragraphs", headers=header)
    paragraphs_response = paragraphs_response.json()

    paragraphs = []
    for para in paragraphs_response['paragraphs']:
        paragraphs.append(para)

    return paragraphs


@st.cache
def extract_ste(transcript):
    header = {"Content-Type": "application/json", "Authorization": f"Bearer {openai_api_key}"}
    prompt = transcript + "As a kind bot, please separate out the situation, thoughts, and emotions out of what was described above, and list it out in a CBT thought records format, each in one line."
    req = requests.post(
        url="https://api.openai.com/v1/engines/text-davinci-002/completions",
        data='{"prompt": "' + prompt.replace("\n", "") + '", "temperature": 0.7, "max_tokens": 256, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0}',
        headers=header
    )
    resp = req.json()
    thought_record = resp["choices"][0]["text"]
    try:
        _, situation, thoughts, emotions = thought_record.split("\n\n")
    except ValueError:
        situation, thoughts, emotions = thought_record, "", ""
    return situation, thoughts, emotions


@st.cache
def extract_transcript(uploaded_file):

    header = {
        'authorization': aai_api_key,
        'content-type': 'application/json'
    }
    upload_url = upload_file(uploaded_file, header)
    transcript_response = request_transcript(upload_url, header)
    polling_endpoint = make_polling_endpoint(transcript_response)
    wait_for_completion(polling_endpoint, header)
    paragraphs = get_paragraphs(polling_endpoint, header)
    return paragraphs


