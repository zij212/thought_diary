# Thought Diary
## Background
Thought records are used by cognitive behavioural therapist to help their clients capture, evaluate, and restructure their automatic thoughts. Recording and evaluating thoughts allows us to test the accuracy of our thinking, and oftentimes feel better by identifying and correcting bias or inaccuracies. One objective when using thought records in CBT is to encourage more balanced thinking.

**Thought Diary** is a tool that transcribes user's voice memo into text; extract the situation, thoughts, and emotions from the user's narrative; and guides user to examine their thinking pattern.

## Set Ups

```
conda create -n td python=3.9
conda activate td
pip install openai
pip install streamlit
```

You'll also need API key from [AssemblyAI](https://www.assemblyai.com/) and [OpenAI](https://openai.com/api/) to run Thought Diary
```
export AAI_AUTH_TOKEN=<YOUR_AAI_API_KEY>
export OPENAI_AUTH_TOKEN=<YOUR_OPENAI_API_KEY>
```


