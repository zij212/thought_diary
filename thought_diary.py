import streamlit as st
import utils
import warnings

warnings.filterwarnings("ignore")


st.title("Thought Diary")
st.header("Background")

background = "Thought records are used by cognitive behavioural therapist to help their clients capture, evaluate, " \
      "and restructure their automatic thoughts. Recording and evaluating thoughts allows us to test the accuracy " \
      "of our thinking, and oftentimes feel better by identifying and correcting bias or inaccuracies. One " \
      "objective when using thought records in CBT is to encourage more balanced thinking. " \
      "<br><br>Thought diary is a tool that guides user to examine their thinking pattern."
st.markdown(background, unsafe_allow_html=True)


st.header("Describe a stressful event")
instruction = "Recall a recent event that evokes emotion, your thoughts and your reaction. In a voice memo, try to " \
              "include as many details as possible. "
st.markdown(instruction)

uploaded_file = st.file_uploader("Please upload the voice memo")
if uploaded_file is not None:
    st.audio(uploaded_file, start_time=0)
    paragraphs = utils.extract_transcript(uploaded_file)
    #TODO: alert the user to reupload if it is not a thought record voice memo

    st.header("Audio Transcript")
    transcript = ""
    for para in paragraphs:
        transcript += para["text"] + "\n"
    st.markdown(transcript.replace("\n", "<br>"), unsafe_allow_html=True)

    st.header("It's Practice Time!")
    st.subheader("Split and Expand")
    st.markdown("We extract the situation, thoughts, and emotions from the transcript and pre-filled the following "
                "text areas. The goal of this section is to separate out fact from our perceptions and feelings, "
                "and show us how intertwined these elements are.")

    situation, thoughts, emotions = utils.extract_ste(transcript)

    situation = st.text_area("What led to this unpleasant feeling? Feel free to add more facts.", situation, height=40)
    thoughts = st.text_area("What thoughts went through your mind? Dump them out!", thoughts, height=5)
    score_thoughts_before = st.slider("How much did you believe the thought? Give it a number.", 0, 100, 50)
    emotions = st.text_area("What emotions did you feel?", emotions, height=100)
    emotions_dropdown = st.multiselect(
        label="We're here to help if you're having a hard time describing your emotions",
        options=[
            "cheerful",
            "joyful",
            "depressed",
            "grief",
            "content",
            "pleased",
            "disappointed",
            "hopeless",
            "elated",
            "pride",
            "down",
            "lonely",
            "excited",
            "relieved",
            "embarrassed",
            "regret",
            "glad",
            "satisfied",
            "empty",
            "shame",
            "anger",
            "fear",
            "annoyed",
            "hate",
            "afraid",
            "nervous",
            "appalled",
            "irritated",
            "anxious",
            "petrified",
            "contempt",
            "mad",
            "dread",
            "scared",
            "enraged",
            "offended",
            "frightened",
            "terrified",
            "frustrated",
            "upset",
            "horrified",
            "worried"
         ])
    score_emotions_before = st.slider("How intense was the emotion?", 0, 100, 50)

    st.subheader("Re-examination")
    st.markdown("In the previous section, we've made our negative automatic thoughts visible. "
                "Now, let's identify patterns in our thinking.", unsafe_allow_html=True)
    thinking_traps = st.multiselect(
        label="What thinking trap(s) did you engage in? In the drop down below, we've included some examples.",
        options=[
            "Black & white thinking",
            "Over-generalizing",
            "Discounting the positives",
            "Minimizing",
            "Jumping to conclusions",
            "Fortune telling",
            "Magnifying"
        ])

    coping_plan = st.text_area(
        "The prompt in the text area below will guide you to examine the evidence "
        "for and against the thought, and come up with a coping strategy",
        "Evidence for thought:\nEvidence against thought:\nWorst that could happen:\n"
        "Best that could happen:\nMost realistic outcome:\nWhat would you tell a friend?\n",
        height=400
    )

    score_thoughts_after = st.slider("How much do you believe the thought now?", 0, 100, 50, key="score_thoughts_after")
    score_emotions_after = st.slider("What intensity is your emotion now?", 0, 100, 50, key="score_emotions_after")

    create_report = st.button("Create Report")
    if create_report:
        st.subheader("Report")
        if emotions_dropdown:
            emotions = emotions + ", " + ", ".join(emotions_dropdown)
        linebreak = "\n"
        report = "{}<br>{}<br>Thinking traps: {}<br>{}<br>{}".format(
            situation,
            emotions,
            ", ".join(thinking_traps),
            thoughts,
            coping_plan.replace(linebreak, "<br>")
        )
        st.markdown(report, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        col1.metric("Belief of original thoughts", score_thoughts_after, score_thoughts_after - score_thoughts_before)
        col2.metric("Intensity of emotion", score_emotions_after, score_emotions_after - score_emotions_before)

        with st.empty():
            download = st.download_button("Download Report", report.replace("<br>", "\n"))












