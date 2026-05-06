import random
from datetime import datetime
from typing import Dict, Any, List

import streamlit as st
import streamlit.components.v1 as components

from . import ui


@st.cache_data(show_spinner=False)
def get_vocab() -> List[Dict[str, Any]]:
    return [
        {"word":"accelerate","ipa":"/əkˈseləreɪt/","meaning":"tăng tốc","topic":"Driving","level":"A1","example":"Do not accelerate near a crowded intersection.","tip":"Liên hệ với acceleration."},
        {"word":"brake","ipa":"/breɪk/","meaning":"phanh","topic":"Driving","level":"A1","example":"Brake gently on a wet road.","tip":"Brake là phanh, khác break là làm vỡ."},
        {"word":"merge","ipa":"/mɜːrdʒ/","meaning":"nhập làn","topic":"Driving","level":"A1","example":"Merge into the lane smoothly.","tip":"Rất hay dùng trên đường lớn / cao tốc."},
        {"word":"yield","ipa":"/jiːld/","meaning":"nhường đường","topic":"Driving","level":"A1","example":"Yield to pedestrians at the crossing.","tip":"Xuất hiện nhiều ở biển báo."},
        {"word":"intersection","ipa":"/ˌɪntərˈsekʃn/","meaning":"giao lộ","topic":"Driving","level":"A1","example":"Slow down before the intersection.","tip":"inter + section = chỗ giao nhau."},
        {"word":"distance","ipa":"/ˈdɪstəns/","meaning":"khoảng cách","topic":"Driving","level":"A1","example":"Keep a safe distance from the car ahead.","tip":"Safe distance = khoảng cách an toàn."},
        {"word":"lane","ipa":"/leɪn/","meaning":"làn đường","topic":"Driving","level":"A1","example":"Stay in your lane.","tip":"Lane dùng rất nhiều trong học lái xe."},
        {"word":"medicine","ipa":"/ˈmedɪsɪn/","meaning":"thuốc","topic":"Care","level":"A1","example":"Please take your medicine after breakfast.","tip":"Medicine là thuốc nói chung."},
        {"word":"reminder","ipa":"/rɪˈmaɪndər/","meaning":"lời nhắc","topic":"Care","level":"A1","example":"The app sends a reminder every morning.","tip":"Reminder dùng nhiều trong app nhắc lịch."},
        {"word":"carefully","ipa":"/ˈkerfəli/","meaning":"cẩn thận","topic":"Daily","level":"A1","example":"Read the sign carefully.","tip":"Adverb của careful."},
        {"word":"slippery","ipa":"/ˈslɪpəri/","meaning":"trơn trượt","topic":"Driving","level":"A2","example":"The road is slippery after the rain.","tip":"Hay đi với road / floor."},
        {"word":"confidence","ipa":"/ˈkɑːnfɪdəns/","meaning":"sự tự tin","topic":"Study","level":"A2","example":"Daily practice builds confidence.","tip":"Tự tin đến từ luyện tập đều."},
        {"word":"fluently","ipa":"/ˈfluːəntli/","meaning":"trôi chảy","topic":"Speaking","level":"A2","example":"She speaks English fluently.","tip":"Fluent là tính từ, fluently là trạng từ."},
        {"word":"improve","ipa":"/ɪmˈpruːv/","meaning":"cải thiện","topic":"Study","level":"A1","example":"I want to improve my speaking.","tip":"Động từ rất hay dùng trong học tập."},
        {"word":"describe","ipa":"/dɪˈskraɪb/","meaning":"miêu tả","topic":"Speaking","level":"A2","example":"Describe the picture in simple English.","tip":"Từ quan trọng trong nói và viết."},
        {"word":"schedule","ipa":"/ˈskedʒuːl/","meaning":"lịch trình","topic":"Daily","level":"A2","example":"I follow a study schedule every day.","tip":"Nên học theo schedule để đều hơn."},
        {"word":"compare","ipa":"/kəmˈper/","meaning":"so sánh","topic":"Study","level":"B1","example":"Compare the two traffic signs.","tip":"B1 thường yêu cầu biết so sánh và giải thích."},
        {"word":"respond","ipa":"/rɪˈspɑːnd/","meaning":"phản hồi / đáp lại","topic":"Communication","level":"B1","example":"You should respond calmly in a difficult situation.","tip":"B1 cần phản xạ giao tiếp tốt hơn."},
        {"word":"recommend","ipa":"/ˌrekəˈmend/","meaning":"đề xuất","topic":"Communication","level":"B1","example":"I recommend practicing for ten minutes every day.","tip":"Thường dùng khi đưa lời khuyên."},
        {"word":"safely","ipa":"/ˈseɪfli/","meaning":"một cách an toàn","topic":"Driving","level":"A2","example":"You should drive safely in heavy rain.","tip":"Adverb của safe."},
        {"word":"direction","ipa":"/dəˈrekʃn/","meaning":"hướng đi","topic":"Travel","level":"A1","example":"Can you show me the direction to the station?","tip":"Hữu ích khi hỏi đường."},
        {"word":"appointment","ipa":"/əˈpɔɪntmənt/","meaning":"cuộc hẹn","topic":"Daily","level":"A2","example":"I have a doctor appointment at 9 a.m.","tip":"Rất thực tế trong giao tiếp hàng ngày."},
        {"word":"available","ipa":"/əˈveɪləbl/","meaning":"có sẵn / rảnh","topic":"Daily","level":"A2","example":"Are you available this afternoon?","tip":"Dùng để hỏi lịch hoặc tình trạng còn chỗ."},
        {"word":"explain","ipa":"/ɪkˈspleɪn/","meaning":"giải thích","topic":"Communication","level":"B1","example":"Could you explain that again?","tip":"Câu rất hữu ích khi chưa hiểu."},
    ]


@st.cache_data(show_spinner=False)
def get_tracks() -> List[Dict[str, Any]]:
    return [
        {"level":"A1","title":"A1 Foundation","focus":"Từ cơ bản, câu ngắn, phản xạ đọc – nghe – nói đơn giản.","items":["Từ vựng giao thông cơ bản", "Mẫu câu nhắc thuốc", "Hiện tại đơn", "Question-answer ngắn"]},
        {"level":"A2","title":"A2 Expansion","focus":"Mô tả tình huống, giải thích ngắn, nghe câu dài hơn một chút.","items":["Từ vựng mở rộng", "Because / so", "Listening tình huống", "Speaking theo chủ đề"]},
        {"level":"B1","title":"B1 Practical Use","focus":"Diễn đạt ý kiến, so sánh, đưa khuyến nghị, phản hồi tự nhiên hơn.","items":["Nói theo tình huống", "So sánh và nêu ý kiến", "Listening dài hơn", "Câu đệm giao tiếp"]},
    ]


@st.cache_data(show_spinner=False)
def get_grammar() -> List[Dict[str, Any]]:
    return [
        {"level":"A1","title":"Hiện tại đơn","pattern":"S + V(s/es) / do-does","tip":"Dùng cho thói quen, sự thật, lịch trình.","example":"He drives carefully every day."},
        {"level":"A1","title":"Mệnh lệnh lịch sự","pattern":"Please + V ...","tip":"Rất hay dùng khi nhắc ai đó làm gì.","example":"Please take your medicine now."},
        {"level":"A2","title":"Because / so","pattern":"Clause + because + clause / Clause, so clause","tip":"Dùng để giải thích nguyên nhân và kết quả.","example":"I slow down because the road is slippery."},
        {"level":"A2","title":"Can / Could","pattern":"Can/Could + S + V ...?","tip":"Dùng để xin phép hoặc yêu cầu lịch sự.","example":"Could you say that again?"},
        {"level":"B1","title":"Should / shouldn't","pattern":"S + should + V","tip":"Dùng để đưa lời khuyên.","example":"You should keep a safe distance."},
        {"level":"B1","title":"Comparatives","pattern":"A is + comparative + than B","tip":"Dùng để so sánh an toàn hơn, dễ hơn...", "example":"Driving slowly is safer than driving fast in the rain."},
        {"level":"B1","title":"Giving opinions","pattern":"In my opinion, ... / I think ... because ...","tip":"Giúp bạn nói tự nhiên hơn khi nêu quan điểm.", "example":"In my opinion, this option is safer because the road is wider."},
    ]


@st.cache_data(show_spinner=False)
def get_listening() -> List[Dict[str, Any]]:
    return [
        {"level":"A1","title":"Medicine reminder","script":"Please take your medicine after breakfast and drink enough water.","question":"When should you take the medicine?","answer":"After breakfast","choices":["After breakfast","Before sleep","At midnight","On the bus"]},
        {"level":"A1","title":"Changing lanes","script":"Check the mirror, turn on the signal, and look over your shoulder before changing lanes.","question":"What should you do before changing lanes?","answer":"Check the mirror","choices":["Check the mirror","Speed up a lot","Close your eyes","Turn off the signal"]},
        {"level":"A2","title":"Road safety","script":"The road is slippery, so slow down and keep a safe distance from the car in front.","question":"Why should you slow down?","answer":"Because the road is slippery","choices":["Because the road is slippery","Because the road is empty","Because the car is new","Because it is sunny"]},
        {"level":"A2","title":"Study routine","script":"I review ten new words every morning, then I listen to one short audio and practice speaking for five minutes.","question":"What does the speaker do after reviewing words?","answer":"Listen to one short audio","choices":["Listen to one short audio","Go to sleep","Watch a movie","Drive to work"]},
        {"level":"B1","title":"Giving advice","script":"If you feel nervous during the driving test, breathe slowly, focus on one step at a time, and do not rush your decisions.","question":"What should you do when you feel nervous?","answer":"Focus on one step at a time","choices":["Focus on one step at a time","Drive faster","Ignore the examiner","Close your eyes"]},
        {"level":"B1","title":"Comparing options","script":"The first route is shorter, but the second route is safer because it has less traffic and better lighting at night.","question":"Why is the second route safer?","answer":"It has less traffic and better lighting","choices":["It has less traffic and better lighting","It is shorter","It has more traffic","It is more expensive"]},
    ]


@st.cache_data(show_spinner=False)
def get_conversations() -> List[Dict[str, Any]]:
    return [
        {"level":"A1","title":"At the pharmacy","context":"Mua thuốc và hỏi cách dùng.","dialogue":[("Customer","Hello. I need this medicine, please."),("Pharmacist","Sure. Take one pill after breakfast."),("Customer","Thank you. How often should I take it?"),("Pharmacist","Twice a day.")],"phrases":["I need this medicine.","How often should I take it?","Twice a day."],"challenge":"Hãy thử đổi 'twice a day' thành 'three times a day'."},
        {"level":"A1","title":"Asking for directions","context":"Hỏi đường đến bến xe / ga tàu.","dialogue":[("You","Excuse me, where is the bus station?"),("Local","Go straight and turn left at the traffic light."),("You","Is it far from here?"),("Local","No, it is about five minutes away.")],"phrases":["Where is the bus station?","Go straight.","Turn left.","Is it far from here?"],"challenge":"Đổi 'bus station' thành 'hospital' hoặc 'school'."},
        {"level":"A1","title":"Driving school","context":"Nói chuyện với giáo viên dạy lái.","dialogue":[("Teacher","Today we will practice changing lanes."),("Student","Okay. What should I do first?"),("Teacher","Check the mirror and turn on the signal."),("Student","Got it. Then I check the blind spot.")],"phrases":["What should I do first?","Check the mirror.","Turn on the signal.","Check the blind spot."],"challenge":"Đọc lại cả đoạn thật chậm rồi tăng tốc độ nói lên."},
        {"level":"A2","title":"At the clinic","context":"Đặt lịch và hỏi thời gian khám.","dialogue":[("Patient","Hello. I would like to make an appointment."),("Receptionist","Sure. Are you available tomorrow morning?"),("Patient","Yes, that works for me."),("Receptionist","Great. Your appointment is at 9 a.m.")],"phrases":["I would like to make an appointment.","Are you available...?","That works for me."],"challenge":"Đổi thời gian hẹn sang buổi chiều."},
        {"level":"A2","title":"Small talk before class","context":"Nói chuyện ngắn trước giờ học.","dialogue":[("Friend A","How is your English practice going?"),("Friend B","It is getting better because I practice every day."),("Friend A","That is great. What do you practice most?"),("Friend B","Listening and speaking.")],"phrases":["How is ... going?","It is getting better.","What do you practice most?"],"challenge":"Thay 'English' bằng 'driving theory'."},
        {"level":"A2","title":"Restaurant order","context":"Gọi món và hỏi gợi ý.","dialogue":[("Customer","Could you recommend something light?"),("Staff","Yes. Our chicken salad is very popular."),("Customer","That sounds good. I will have one."),("Staff","Would you like a drink as well?")],"phrases":["Could you recommend ...?","That sounds good.","I will have one."],"challenge":"Đổi món ăn khác và trả lời theo ý bạn."},
        {"level":"B1","title":"Discussing safer options","context":"So sánh 2 lựa chọn xử lý tình huống lái xe.","dialogue":[("Instructor","Which option is safer in this situation?"),("Student","In my opinion, slowing down is safer than overtaking here."),("Instructor","Why do you think so?"),("Student","Because the road is narrow and visibility is limited.")],"phrases":["In my opinion...","... is safer than ...","Because ..."],"challenge":"Đổi lý do và tự tạo một câu trả lời mới."},
        {"level":"B1","title":"Giving a recommendation","context":"Khuyên một người mới học tiếng Anh.","dialogue":[("Friend","I want to improve my English, but I do not know how."),("You","I recommend practicing for ten minutes every day."),("Friend","What should I focus on first?"),("You","Start with useful phrases and short listening exercises.")],"phrases":["I recommend ...","What should I focus on first?","Start with ..."],"challenge":"Hãy thay lời khuyên sang chủ đề học lái xe."},
    ]


@st.cache_data(show_spinner=False)
def get_quiz() -> List[Dict[str, Any]]:
    return [
        {"level":"A1","topic":"Vocabulary","icon":"↔️","question":"What does 'yield' mean?","options":["nhường đường","tăng tốc","đỗ xe","quay đầu"],"answer":"nhường đường","explain":"Yield = nhường đường, rất hay gặp trong ngữ cảnh giao thông."},
        {"level":"A1","topic":"Vocabulary","icon":"🚗","question":"Choose the meaning of 'merge'.","options":["nhập làn","dừng xe","lùi xe","đèn xe"],"answer":"nhập làn","explain":"Merge into a lane = nhập làn."},
        {"level":"A1","topic":"Grammar","icon":"✍️","question":"Correct sentence:","options":["He doesn't drive fast.","He don't drive fast.","He not drive fast.","He isn't drive fast."],"answer":"He doesn't drive fast.","explain":"Dùng doesn't với he/she/it."},
        {"level":"A1","topic":"Daily English","icon":"💊","question":"Natural medicine reminder:","options":["Mom, please take your medicine now.","Medicine now!","Take now medicine.","Mother take quick."],"answer":"Mom, please take your medicine now.","explain":"Đây là câu lịch sự và tự nhiên."},
        {"level":"A1","topic":"Listening","icon":"🎧","question":"If the road is slippery, what should you do?","options":["Slow down","Accelerate","Close your eyes","Turn off the car"],"answer":"Slow down","explain":"Slippery road = đường trơn, cần giảm tốc."},
        {"level":"A1","topic":"Driving English","icon":"👀","question":"'Check the blind spot' means:","options":["Kiểm tra điểm mù","Kiểm tra xăng xe","Bật đèn sương mù","Đóng cửa kính"],"answer":"Kiểm tra điểm mù","explain":"Blind spot là vùng khó quan sát bằng gương."},
        {"level":"A1","topic":"Conversation","icon":"🧭","question":"How do you ask for directions politely?","options":["Excuse me, where is the bus station?","Where bus station?","Bus station now?","You bus station?"],"answer":"Excuse me, where is the bus station?","explain":"Đây là mẫu câu hỏi đường tự nhiên và lịch sự."},
        {"level":"A2","topic":"Speaking","icon":"🗣️","question":"Which response is best when you need more time to answer?","options":["Let me think for a second.","No think.","I fast answer.","Nothing."],"answer":"Let me think for a second.","explain":"Đây là câu đệm tự nhiên khi giao tiếp."},
        {"level":"A2","topic":"Grammar","icon":"🔗","question":"Which sentence gives a reason?","options":["I study daily because I want to improve.","What is your name?","Please open the door.","Nice to meet you."],"answer":"I study daily because I want to improve.","explain":"Because nối nguyên nhân với kết quả."},
        {"level":"A2","topic":"Vocabulary","icon":"🌧️","question":"What does 'slippery' mean?","options":["trơn trượt","ổn định","chậm chạp","hẹp"],"answer":"trơn trượt","explain":"Slippery thường mô tả mặt đường trơn sau mưa."},
        {"level":"A2","topic":"Pronunciation","icon":"🔊","question":"Which word has stress on the second syllable?","options":["reMINDer","BRAke","MERge","CAREful"],"answer":"reMINDer","explain":"re-MIND-er nhấn vào âm tiết thứ hai."},
        {"level":"A2","topic":"Vocabulary","icon":"📅","question":"What does 'schedule' mean?","options":["lịch trình","thói quen xấu","điểm mù","gương chiếu hậu"],"answer":"lịch trình","explain":"Schedule là lịch trình hoặc thời gian biểu."},
        {"level":"A2","topic":"Speaking","icon":"📝","question":"Which sentence is the best self-improvement statement?","options":["I want to improve my English little by little.","I English improve big.","Improve I want English.","No improve me."],"answer":"I want to improve my English little by little.","explain":"Đây là câu tự nhiên và đúng ngữ pháp."},
        {"level":"A2","topic":"Conversation","icon":"💬","question":"Which sentence is the best for making an appointment?","options":["I would like to make an appointment.","Make appointment me.","I appointment now.","Appointment do."],"answer":"I would like to make an appointment.","explain":"Mẫu câu lịch sự và rất thực tế."},
        {"level":"A2","topic":"Conversation","icon":"🍽️","question":"How do you accept a food suggestion naturally?","options":["That sounds good. I will have one.","I eat this yes.","This me now.","Good, one food."],"answer":"That sounds good. I will have one.","explain":"Câu tự nhiên khi đồng ý gọi món."},
        {"level":"B1","topic":"Advice","icon":"💡","question":"Choose the best advice sentence:","options":["You should keep a safe distance in heavy rain.","You should keeps a safe distance.","You safe distance should.","Should you to keep distance."],"answer":"You should keep a safe distance in heavy rain.","explain":"Should + base verb là cấu trúc đúng để đưa lời khuyên."},
        {"level":"B1","topic":"Comparison","icon":"⚖️","question":"Choose the best comparison:","options":["Driving slowly in the rain is safer than driving fast.","Driving slowly safer than.","Safer slow driving.","Driving fast is safe more."],"answer":"Driving slowly in the rain is safer than driving fast.","explain":"Đây là câu so sánh đúng và tự nhiên."},
        {"level":"B1","topic":"Communication","icon":"📣","question":"Which sentence gives a recommendation?","options":["I recommend practicing for ten minutes every day.","Practice ten minute every day me.","Recommend I you practice.","Ten minute recommend."],"answer":"I recommend practicing for ten minutes every day.","explain":"Recommend + V-ing là cách dùng phổ biến."},
        {"level":"B1","topic":"Listening","icon":"🎯","question":"If you feel nervous during the driving test, what should you do?","options":["Focus on one step at a time","Drive faster","Stop listening","Forget the mirrors"],"answer":"Focus on one step at a time","explain":"Đây là chiến lược bình tĩnh và thực tế."},
        {"level":"B1","topic":"Vocabulary","icon":"📘","question":"What does 'respond calmly' mean?","options":["phản hồi bình tĩnh","lái thật nhanh","đỗ xe sai chỗ","mất tập trung"],"answer":"phản hồi bình tĩnh","explain":"Respond calmly = phản hồi / xử lý một cách bình tĩnh."},
        {"level":"B1","topic":"Speaking","icon":"🧠","question":"Which answer sounds the most natural?","options":["In my opinion, this option is safer because the road is wider.","My opinion this road safer.","Road wide safer me.","Opinion I safer road."],"answer":"In my opinion, this option is safer because the road is wider.","explain":"B1 cần biết nêu ý kiến và giải thích lý do ngắn gọn."},
        {"level":"B1","topic":"Conversation","icon":"🗨️","question":"Which reply best gives a reasoned opinion?","options":["In my opinion, slowing down is safer because visibility is limited.","Slow safer maybe.","I think road.","Because yes."],"answer":"In my opinion, slowing down is safer because visibility is limited.","explain":"Đây là câu hoàn chỉnh, tự nhiên và có lý do rõ ràng."},
        {"level":"B1","topic":"Conversation","icon":"👥","question":"Which sentence best starts a recommendation?","options":["I recommend practicing useful phrases every day.","Recommend phrases every day I.","Practice because recommend.","Useful phrase recommend."],"answer":"I recommend practicing useful phrases every day.","explain":"Cấu trúc recommend + V-ing rất tự nhiên trong hội thoại."},
    ]


def _english_hero_svg():
    components.html("""
    <div style='border:1px solid #1f2b42;border-radius:22px;background:#0e1628;padding:10px;'>
    <svg viewBox='0 0 720 220' width='100%' height='210'>
      <rect width='720' height='220' fill='#0e1628'/>
      <rect x='24' y='26' width='672' height='168' rx='24' fill='#111b2f' stroke='#334155'/>
      <rect x='44' y='52' width='180' height='116' rx='18' fill='#1d4ed8'/><text x='134' y='94' text-anchor='middle' fill='white' font-size='28'>A1 → B1</text><text x='134' y='124' text-anchor='middle' fill='white' font-size='18'>Conversation Pack</text>
      <circle cx='314' cy='110' r='34' fill='#8b5cf6'/><text x='314' y='120' text-anchor='middle' fill='white' font-size='24'>🗣️</text>
      <circle cx='414' cy='110' r='34' fill='#22c55e'/><text x='414' y='120' text-anchor='middle' fill='white' font-size='24'>🎧</text>
      <circle cx='514' cy='110' r='34' fill='#f59e0b'/><text x='514' y='120' text-anchor='middle' fill='white' font-size='24'>✍️</text>
      <circle cx='614' cy='110' r='34' fill='#ef4444'/><text x='614' y='120' text-anchor='middle' fill='white' font-size='24'>💬</text>
      <text x='360' y='26' text-anchor='middle' fill='#e2e8f0' font-size='18'>English Master A1–B2: vocabulary · conversation · listening · grammar · quiz</text>
    </svg></div>
    """, height=220)


def _word_card(item):
    st.markdown(f"<div class='panel'><div class='stat-row'><span class='pill purple'>{item['level']}</span><span class='pill blue'>{item['topic']}</span></div><h1 style='margin:.25rem 0'>{item['word']}</h1><h4 style='margin:0;color:#93c5fd'>{item['ipa']}</h4><p><b>Nghĩa:</b> {item['meaning']}</p><p><b>Ví dụ:</b> {item['example']}</p><p class='muted'><b>Mẹo nhớ:</b> {item['tip']}</p></div>", unsafe_allow_html=True)


def _level_visual(level: str):
    labels = {
        "A1": ["Từ cơ bản", "Câu ngắn", "Nghe chậm", "Mẫu câu đời sống"],
        "A2": ["Từ mở rộng", "Giải thích ngắn", "Speaking chủ đề", "Listening dài hơn"],
        "B1": ["Nêu ý kiến", "So sánh", "Đưa lời khuyên", "Phản hồi tự nhiên"],
    }
    chips = ''.join([f"<span style='display:inline-block;margin:6px;padding:8px 12px;border-radius:999px;background:#14233f;border:1px solid #29406d;color:#dbeafe;font-weight:700'>{x}</span>" for x in labels[level]])
    st.markdown(f"<div class='glass-card'><h3>{level} Learning Focus</h3><p class='muted'>Mục tiêu của cấp độ {level}</p><div>{chips}</div></div>", unsafe_allow_html=True)


def render(profile: Dict[str, Any], save_cb) -> None:
    st.title("🇬🇧 English Master A1–B2")
    st.caption("Master Pack: thêm conversation tình huống thực tế, nhiều bài hơn theo A1–B2 và giao diện rõ đẹp hơn để học lâu mà vẫn dễ tiếp thu.")
    eng = profile.setdefault('english', {})
    learned = set(eng.setdefault('learned_words', []))
    eng.setdefault('quiz_history', [])
    eng.setdefault('wrong_bank', {})
    vocab = get_vocab(); tracks = get_tracks(); grammar = get_grammar(); listening = get_listening(); conversations = get_conversations()
    tabs = st.tabs(["🗺️ Lộ trình A1–B2", "📘 Vocabulary", "💬 Conversation", "🎧 Listening", "✍️ Grammar", "📈 Tiến độ"])
    with tabs[0]:
        _english_hero_svg()
        cols = st.columns(3)
        for i, item in enumerate(tracks):
            with cols[i]:
                ui.card("🇬🇧", item['title'], item['focus'], item['level'])
                ui.pills(item['items'], 'blue')
                _level_visual(item['level'])
    with tabs[1]:
        level_filter = st.selectbox("Lọc theo cấp độ", ["Tất cả", "A1", "A2", "B1"])
        topic_filter = st.selectbox("Lọc theo chủ đề", ["Tất cả"] + sorted({v['topic'] for v in vocab}))
        filtered = vocab
        if level_filter != 'Tất cả': filtered = [v for v in filtered if v['level'] == level_filter]
        if topic_filter != 'Tất cả': filtered = [v for v in filtered if v['topic'] == topic_filter]
        preview_cols = st.columns(3)
        for i, item in enumerate(filtered[:9]):
            with preview_cols[i % 3]: ui.card("📘", item['word'], f"{item['meaning']} · {item['topic']}", item['level'])
        topic = st.selectbox("Chọn từ để học sâu", [v['word'] for v in filtered] if filtered else [v['word'] for v in vocab])
        word = next(v for v in vocab if v['word'] == topic)
        _word_card(word)
        ui.speak_button(word['word'] + '. ' + word['example'], "🔊 Listen", lang='en-US', key='eng_word')
        if st.button("⭐ Đánh dấu đã học", key=f"learn_{word['word']}"):
            learned.add(word['word']); eng['learned_words'] = sorted(learned); save_cb(profile); st.success('Đã lưu từ đã học.')
    with tabs[2]:
        st.markdown("### 💬 Real-life Conversation")
        level = st.selectbox("Chọn cấp độ conversation", ["A1", "A2", "B1"])
        available = [x for x in conversations if x['level'] == level]
        title = st.selectbox("Chọn tình huống", [x['title'] for x in available])
        conv = next(x for x in available if x['title'] == title)
        st.markdown(f"<div class='panel'><div class='stat-row'><span class='pill purple'>{conv['level']}</span><span class='pill blue'>{conv['context']}</span></div><h3>{conv['title']}</h3></div>", unsafe_allow_html=True)
        for idx, (speaker, line) in enumerate(conv['dialogue']):
            bubble_cls = 'bubble-a' if idx % 2 == 0 else 'bubble-b'
            st.markdown(f"<div class='conversation-bubble {bubble_cls}'><b>{speaker}:</b> {line}</div>", unsafe_allow_html=True)
        full_script = ' '.join([line for _, line in conv['dialogue']])
        ui.speak_button(full_script, '🔊 Nghe hội thoại', lang='en-US', key='conv_tts')
        st.markdown("#### Useful phrases")
        ui.pills(conv['phrases'], 'green')
        st.info('Bài tập: ' + conv['challenge'])
        roleplay = st.text_area('Viết lại 1–2 câu phản hồi của bạn trong tình huống này', key='roleplay_box')
        if roleplay:
            if len(roleplay.split()) < 4:
                st.warning('Bạn hãy viết dài thêm một chút để luyện phản xạ câu đầy đủ.')
            else:
                st.success('Tốt! Hãy đọc to phần bạn vừa viết để luyện nói.')
    with tabs[3]:
        st.markdown("### 🎧 Listening Lab")
        level = st.selectbox("Chọn cấp độ listening", ["A1", "A2", "B1"])
        available = [x for x in listening if x['level'] == level]
        item = st.selectbox("Chọn đoạn nghe", [x['title'] for x in available])
        obj = next(x for x in available if x['title'] == item)
        st.markdown(f"<div class='panel'><div class='pill purple'>{obj['level']}</div><h4>{obj['title']}</h4><p>{obj['script']}</p></div>", unsafe_allow_html=True)
        ui.speak_button(obj['script'], "🔊 Phát đoạn nghe", lang='en-US', key=f"listen_{item}")
        ans = st.radio(obj['question'], obj['choices'], key=f"listen_ans_{item}")
        if st.button("Kiểm tra nghe", key=f"check_{item}"):
            if ans == obj['answer']:
                st.success("Đúng rồi! Bạn nghe bắt được ý chính khá tốt.")
            else:
                st.error(f"Chưa đúng. Đáp án: {obj['answer']}")
                st.info("Mẹo: nghe từ khóa thời gian, hành động hoặc lý do trước.")
    with tabs[4]:
        st.markdown("### ✍️ Grammar mini-lessons")
        level = st.selectbox("Chọn cấp độ grammar", ["Tất cả", "A1", "A2", "B1"])
        items = grammar if level == 'Tất cả' else [g for g in grammar if g['level'] == level]
        for g in items:
            with st.expander(f"{g['level']} · {g['title']}"):
                st.write(f"**Cấu trúc:** {g['pattern']}")
                st.write(f"**Mẹo nhớ:** {g['tip']}")
                st.write(f"**Ví dụ:** {g['example']}")
    with tabs[5]:
        c1, c2 = st.columns(2)
        with c1: ui.metric_card('Từ đã học', len(eng.get('learned_words', [])), 'từ')
        with c2: ui.metric_card('Lượt quiz', len(eng.get('quiz_history', [])), 'lượt')
        if eng.get('learned_words'): ui.pills(eng['learned_words'][:20], 'green')


def render_quiz(profile: Dict[str, Any], save_cb) -> None:
    st.title("🧪 English Quiz Master")
    st.caption("Quiz tiếng Anh mở rộng theo cấp độ A1–B2, thêm câu conversation tình huống thực tế và ngân hàng câu hỏi lớn hơn.")
    eng = profile.setdefault('english', {})
    wrong = eng.setdefault('wrong_bank', {})
    quiz_bank = get_quiz()
    mode = st.radio('Chế độ', ['Quiz ngẫu nhiên', 'Chỉ ôn câu sai'], horizontal=True)
    level_filter = st.selectbox('Cấp độ', ['Tất cả', 'A1', 'A2', 'B1', 'B2'])
    topic_filter = st.selectbox('Chủ đề', ['Tất cả'] + sorted({q['topic'] for q in quiz_bank}))
    pool = quiz_bank
    if level_filter != 'Tất cả': pool = [q for q in pool if q['level'] == level_filter]
    if topic_filter != 'Tất cả': pool = [q for q in pool if q['topic'] == topic_filter]
    if mode == 'Chỉ ôn câu sai' and wrong:
        pool = [q for q in pool if q['question'] in wrong]
        if not pool:
            st.info('Bộ lọc hiện tại chưa có câu sai. App sẽ dùng ngân hàng câu hỏi thường.')
            pool = quiz_bank
    if not pool:
        st.warning('Không có câu hỏi phù hợp với bộ lọc hiện tại.')
        return
    count = st.slider('Số câu mỗi lượt', 5, min(12, len(pool)), min(8, len(pool)))
    quiz = random.sample(pool, count)
    with st.form('english_quiz_master'):
        answers=[]
        for i,q in enumerate(quiz,1):
            st.markdown(f"### Câu {i}")
            st.markdown(f"<div class='panel'><div class='stat-row'><span class='pill purple'>{q['level']}</span><span class='pill blue'>{q['topic']}</span></div><div style='font-size:2rem'>{q['icon']}</div><b>{q['question']}</b></div>", unsafe_allow_html=True)
            answers.append(st.radio('Answer', q['options'], key=f"eq_{i}", label_visibility='collapsed'))
        submitted=st.form_submit_button('📌 Check & explain')
    if submitted:
        correct=0
        st.markdown('## 📋 Kết quả chi tiết')
        for i,(q,a) in enumerate(zip(quiz,answers),1):
            with st.container(border=True):
                st.markdown(f"**Câu {i}. {q['question']}**")
                if a==q['answer']:
                    correct+=1; st.success(f"✅ Correct · {q['answer']}")
                    wrong.pop(q['question'], None)
                else:
                    wrong[q['question']]={'answer':q['answer'],'explain':q['explain'],'topic':q['topic'],'level':q['level']}
                    st.error(f"❌ Wrong · Correct: {q['answer']}")
                st.info(q['explain'])
                with st.expander('💡 Gợi ý nhớ nhanh'):
                    st.write(f"Cấp độ: {q['level']} · Chủ đề: {q['topic']}")
                    st.write('Hãy đọc to đáp án đúng 2 lần và tự đặt 1 ví dụ ngắn của riêng bạn.')
        score=round(correct/len(quiz)*100)
        eng.setdefault('quiz_history',[]).append({'time':datetime.now().isoformat(timespec='seconds'),'score':score,'correct':correct,'total':len(quiz),'level':level_filter,'topic':topic_filter})
        save_cb(profile); st.metric('Score', f"{score}%", f"{correct}/{len(quiz)}")
        if score < 50: st.warning('Bạn nên ôn lại Vocabulary / Conversation / Grammar của đúng cấp độ trước khi làm vòng tiếp theo.')
        elif score < 80: st.info('Khá tốt. Hãy đọc kỹ phần explain để hiểu sâu hơn và chuyển thành phản xạ.')
        else: st.success('Excellent! Hãy thử cấp độ / chủ đề khác hoặc quay lại Conversation để dùng kiến thức vào thực hành.')

# =========================================================
# v15.6 Final Ultra Pro extensions: B2 + more conversations/quizzes
# =========================================================
_OLD_GET_VOCAB = get_vocab
_OLD_GET_TRACKS = get_tracks
_OLD_GET_GRAMMAR = get_grammar
_OLD_GET_LISTENING = get_listening
_OLD_GET_CONVERSATIONS = get_conversations
_OLD_GET_QUIZ = get_quiz

@st.cache_data(show_spinner=False)
def get_vocab() -> List[Dict[str, Any]]:
    b2 = [
        {"word":"nevertheless","ipa":"/ˌnevərðəˈles/","meaning":"tuy nhiên","topic":"Linking","level":"B2","example":"The route is longer; nevertheless, it is safer at night.","tip":"Dùng để nối ý tương phản trang trọng hơn but."},
        {"word":"consequently","ipa":"/ˈkɑːnsəkwentli/","meaning":"do đó","topic":"Linking","level":"B2","example":"The road was slippery; consequently, we drove more slowly.","tip":"Dùng để diễn tả kết quả."},
        {"word":"visibility","ipa":"/ˌvɪzəˈbɪləti/","meaning":"tầm nhìn","topic":"Driving","level":"B2","example":"Visibility is limited in heavy rain.","tip":"Từ rất hữu ích khi nói về thời tiết và lái xe."},
        {"word":"priority","ipa":"/praɪˈɔːrəti/","meaning":"sự ưu tiên","topic":"Driving","level":"B2","example":"Safety should always be your first priority.","tip":"First priority = ưu tiên hàng đầu."},
        {"word":"precaution","ipa":"/prɪˈkɔːʃn/","meaning":"biện pháp phòng ngừa","topic":"Safety","level":"B2","example":"Taking precautions can prevent accidents.","tip":"Dùng nhiều trong ngữ cảnh an toàn."},
        {"word":"evaluate","ipa":"/ɪˈvæljueɪt/","meaning":"đánh giá","topic":"Study","level":"B2","example":"Evaluate the risk before changing lanes.","tip":"B2 cần biết phân tích và đánh giá."},
        {"word":"alternative","ipa":"/ɔːlˈtɜːrnətɪv/","meaning":"phương án thay thế","topic":"Communication","level":"B2","example":"If this route is crowded, choose an alternative route.","tip":"Dùng khi đề xuất lựa chọn khác."},
        {"word":"consistent","ipa":"/kənˈsɪstənt/","meaning":"đều đặn / nhất quán","topic":"Study","level":"B2","example":"Consistent practice leads to steady progress.","tip":"Rất hay dùng khi nói về học tập."},
    ]
    return _OLD_GET_VOCAB() + b2

@st.cache_data(show_spinner=False)
def get_tracks() -> List[Dict[str, Any]]:
    return _OLD_GET_TRACKS() + [
        {"level":"B2","title":"B2 Confident Communication","focus":"Nói rõ quan điểm, phân tích rủi ro, nối ý tự nhiên và thảo luận tình huống thực tế.",
         "items":["Linking words nâng cao", "Risk explanation", "Debate ngắn", "Conversation tự nhiên hơn"]}
    ]

@st.cache_data(show_spinner=False)
def get_grammar() -> List[Dict[str, Any]]:
    return _OLD_GET_GRAMMAR() + [
        {"level":"B2","title":"Although / nevertheless","pattern":"Although + clause, clause / Clause; nevertheless, clause","tip":"Dùng để diễn đạt tương phản rõ hơn.",
         "example":"Although the route is longer, it is safer at night."},
        {"level":"B2","title":"Consequently / therefore","pattern":"Clause; consequently/therefore, clause","tip":"Dùng để nối nguyên nhân với kết quả theo kiểu trang trọng.",
         "example":"Visibility was poor; therefore, we slowed down."},
        {"level":"B2","title":"Conditionals for advice","pattern":"If + situation, you should / would ...","tip":"Dùng khi đưa lời khuyên theo tình huống.",
         "example":"If visibility is limited, you should increase your following distance."},
    ]

@st.cache_data(show_spinner=False)
def get_listening() -> List[Dict[str, Any]]:
    return _OLD_GET_LISTENING() + [
        {"level":"B2","title":"Risk evaluation","script":"Before overtaking, evaluate visibility, road markings, speed difference, and the available gap. If any factor is unclear, delay the maneuver.",
         "question":"What should you do if any factor is unclear?","answer":"Delay the maneuver","choices":["Delay the maneuver","Overtake immediately","Ignore the road markings","Speed up quickly"]},
        {"level":"B2","title":"Study consistency","script":"Consistent practice is more effective than long, irregular sessions. A focused ten-minute routine every day can build stronger memory and speaking confidence.",
         "question":"What is more effective than long irregular sessions?","answer":"Consistent practice","choices":["Consistent practice","No practice","Only reading once","Watching random videos"]},
        {"level":"B2","title":"Discussing alternatives","script":"Although the highway is faster, the local road may be a better alternative at night because it has lower speeds and more lighting.",
         "question":"Why may the local road be better at night?","answer":"It has lower speeds and more lighting","choices":["It has lower speeds and more lighting","It is always shorter","It has no traffic rules","It is more expensive"]},
    ]

@st.cache_data(show_spinner=False)
def get_conversations() -> List[Dict[str, Any]]:
    return _OLD_GET_CONVERSATIONS() + [
        {"level":"B2","title":"Evaluating a risky overtake","context":"Thảo luận có nên vượt xe hay không.",
         "dialogue":[("Instructor","Would you overtake in this situation?"),("Student","No. Although the car ahead is slow, visibility is limited."),("Instructor","Good. What would you do instead?"),("Student","I would keep a safe distance and wait for a clearer section.")],
         "phrases":["Although ...", "visibility is limited", "I would ... instead", "wait for a clearer section"],"challenge":"Hãy thay tình huống bằng 'heavy rain' và tự viết lại câu trả lời."},
        {"level":"B2","title":"Explaining a safer choice","context":"Giải thích vì sao chọn phương án an toàn hơn.",
         "dialogue":[("Friend","Why did you choose the longer route?"),("You","The shorter route is crowded; consequently, the longer route may be safer."),("Friend","That makes sense."),("You","Safety is my first priority, especially at night.")],
         "phrases":["consequently", "may be safer", "first priority", "especially at night"],"challenge":"Tự tạo câu với 'nevertheless'."},
        {"level":"B2","title":"Professional feedback","context":"Nhận phản hồi sau buổi học lái.",
         "dialogue":[("Teacher","Your lane changes are smoother now."),("Student","Thank you. What should I improve next?"),("Teacher","You should evaluate the gap earlier and signal more consistently."),("Student","I will focus on that in the next session.")],
         "phrases":["What should I improve next?", "evaluate the gap earlier", "more consistently", "focus on that"],"challenge":"Viết một câu phản hồi lịch sự sau khi được góp ý."},
    ]

@st.cache_data(show_spinner=False)
def get_quiz() -> List[Dict[str, Any]]:
    more = [
        {"level":"B2","topic":"Linking","icon":"🔗","question":"Choose the best connector: The road is longer; ___, it is safer at night.","options":["nevertheless","banana","quickly","under"],"answer":"nevertheless","explain":"Nevertheless nối ý tương phản: dài hơn nhưng an toàn hơn."},
        {"level":"B2","topic":"Risk","icon":"⚠️","question":"What does 'evaluate the risk' mean?","options":["đánh giá rủi ro","tăng tốc","đỗ xe","mở cửa"],"answer":"đánh giá rủi ro","explain":"Evaluate = đánh giá; risk = rủi ro."},
        {"level":"B2","topic":"Driving English","icon":"🌧️","question":"Which sentence is most natural?","options":["Visibility is limited, so we should slow down.","Visibility limited slow we.","We slow because visibility limited is.","Limited visibility so down slow."],"answer":"Visibility is limited, so we should slow down.","explain":"Câu này đúng ngữ pháp và tự nhiên."},
        {"level":"B2","topic":"Conversation","icon":"💬","question":"Best response to feedback: 'You should signal earlier.'","options":["Thank you. I will focus on that.","No you wrong.","Signal earlier me no.","I don't care."],"answer":"Thank you. I will focus on that.","explain":"Đây là phản hồi lịch sự và chuyên nghiệp."},
        {"level":"B2","topic":"Advice","icon":"💡","question":"Choose the best conditional advice.","options":["If visibility is limited, you should increase your following distance.","If visibility limited, distance should you.","Limited if visibility distance.","You should if visibility."],"answer":"If visibility is limited, you should increase your following distance.","explain":"If + clause, you should + verb là cấu trúc khuyên theo tình huống."},
        {"level":"B2","topic":"Vocabulary","icon":"📘","question":"What is an 'alternative route'?","options":["phương án đường khác","biển cấm","vạch dừng","tốc độ tối đa"],"answer":"phương án đường khác","explain":"Alternative = phương án thay thế."},
    ]
    return _OLD_GET_QUIZ() + more
