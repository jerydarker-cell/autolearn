import random
from datetime import datetime
from typing import Dict, Any

import streamlit as st

from . import ui

VOCAB = [
    ("accelerate", "/əkˈseləreɪt/", "tăng tốc", "You should not accelerate near a crowded intersection."),
    ("brake", "/breɪk/", "phanh", "Brake gently on a wet road."),
    ("merge", "/mɜːrdʒ/", "nhập làn", "Merge into the lane smoothly."),
    ("yield", "/jiːld/", "nhường đường", "Yield to pedestrians at the crossing."),
    ("medicine", "/ˈmedɪsɪn/", "thuốc", "Please take your medicine after breakfast."),
    ("reminder", "/rɪˈmaɪndər/", "lời nhắc", "The app sends a reminder at 7 a.m."),
    ("confidence", "/ˈkɑːnfɪdəns/", "sự tự tin", "Daily practice builds confidence."),
    ("fluently", "/ˈfluːəntli/", "trôi chảy", "She speaks English fluently."),
]

QUESTIONS = [
    ("What does 'yield' mean?", ["nhường đường", "tăng tốc", "đỗ xe", "quay đầu"], "nhường đường", "Yield = nhường đường."),
    ("Choose the meaning of 'merge'.", ["nhập làn", "dừng xe", "lùi xe", "đèn xe"], "nhập làn", "Merge into a lane = nhập làn."),
    ("Correct sentence:", ["He doesn't drive fast.", "He don't drive fast.", "He not drive fast.", "He isn't drive fast."], "He doesn't drive fast.", "Dùng doesn't với he/she/it."),
    ("Natural medicine reminder:", ["Mom, please take your medicine now.", "Medicine now!", "Take now medicine.", "Mother take quick."], "Mom, please take your medicine now.", "Đây là câu lịch sự và tự nhiên."),
]


def render(profile: Dict[str, Any], save_cb) -> None:
    st.title("🇬🇧 English Production Coach")
    st.caption("Từ vựng, phát âm, quiz và AI gợi ý học đều mỗi ngày.")
    eng = profile.setdefault("english", {})
    learned = set(eng.setdefault("learned_words", []))
    topic = st.selectbox("Chọn từ", [v[0] for v in VOCAB])
    word = next(v for v in VOCAB if v[0] == topic)
    st.markdown(f"<div class='panel'><h1>{word[0]}</h1><h3>{word[1]}</h3><p><b>Nghĩa:</b> {word[2]}</p><p>{word[3]}</p></div>", unsafe_allow_html=True)
    ui.speak_button(word[0] + ". " + word[3], "🔊 Listen", lang="en-US", key="eng_word")
    if st.button("⭐ Đánh dấu đã học"):
        learned.add(word[0]); eng["learned_words"] = sorted(learned); save_cb(profile); st.success("Đã lưu từ đã học.")
    st.markdown("### Speaking Coach")
    sentence = st.selectbox("Câu mẫu", [v[3] for v in VOCAB])
    ui.speak_button(sentence, "🔊 Nghe câu mẫu", lang="en-US", key="speak_model")
    user_sentence = st.text_input("Gõ lại câu bạn nói/nhớ được")
    if user_sentence:
        ratio = round(len(set(user_sentence.lower().split()) & set(sentence.lower().replace('.', '').split())) / max(1, len(set(sentence.lower().replace('.', '').split()))) * 100)
        st.progress(ratio/100); st.caption(f"Độ giống từ khóa: {ratio}%")


def render_quiz(profile: Dict[str, Any], save_cb) -> None:
    st.title("🧪 English Quiz")
    eng = profile.setdefault("english", {})
    wrong = eng.setdefault("wrong_bank", {})
    quiz = random.sample(QUESTIONS, min(4, len(QUESTIONS)))
    with st.form("english_quiz"):
        answers=[]
        for i,q in enumerate(quiz,1):
            st.markdown(f"**{i}. {q[0]}**"); answers.append(st.radio("Answer", q[1], key=f"eq_{i}", label_visibility="collapsed"))
        submitted=st.form_submit_button("Check")
    if submitted:
        correct=0
        for q,a in zip(quiz,answers):
            if a==q[2]: correct+=1; st.success("Correct")
            else: wrong[q[0]]={"answer":q[2],"explain":q[3]}; st.error(f"Wrong. Correct: {q[2]}")
            st.info(q[3])
        score=round(correct/len(quiz)*100); eng.setdefault("quiz_history",[]).append({"time":datetime.now().isoformat(timespec="seconds"),"score":score})
        save_cb(profile); st.metric("Score", f"{score}%")
