import random
from datetime import datetime
from typing import Dict, Any, List

import streamlit as st
import streamlit.components.v1 as components

from . import ui


@st.cache_data(show_spinner=False)
def get_license_packs() -> List[Dict[str, Any]]:
    return [
        {"code": "A1/A", "title": "Xe máy cơ bản", "focus": "Biển báo, giao lộ, xử lý xe máy và luật nền tảng.", "items": ["Biển báo nền tảng", "Giao lộ cơ bản", "Khoảng cách an toàn", "Nhận diện nguy cơ trong phố"]},
        {"code": "B", "title": "Ô tô gia đình", "focus": "Rẽ làn, đỗ xe, đi mưa/đêm, cao tốc cơ bản, sa hình.", "items": ["Rẽ làn & nhập làn", "Sa hình & đỗ xe", "Đi mưa / ban đêm", "Cao tốc cơ bản"]},
        {"code": "C1/C", "title": "Xe tải cơ bản", "focus": "Khoảng cách, quán tính, tầm nhìn hạn chế và xử lý hàng nặng.", "items": ["Phanh & quãng đường dừng", "Điểm mù xe lớn", "Xuống dốc / lên dốc", "Đỗ và quay đầu an toàn"]},
        {"code": "D/E/FC", "title": "Vận tải chuyên nghiệp", "focus": "Kỹ năng phòng vệ nâng cao, hành trình dài và trách nhiệm nghề nghiệp.", "items": ["Quét gương nâng cao", "An toàn hành khách / hàng hóa", "Hành trình đường dài", "Ra quyết định trong tình huống áp lực"]},
    ]


@st.cache_data(show_spinner=False)
def get_lessons() -> List[Dict[str, Any]]:
    return [
        {"id":"defensive","icon":"🧠","title":"Tư duy lái phòng vệ","tag":"Nền tảng","license":"Tất cả","summary":"Nhìn xa, quét rộng, giữ khoảng cách và luôn có phương án thoát.","goal":"Xây nền tư duy an toàn trước khi học kỹ thuật chi tiết.","steps":["Nhìn xa 8–12 giây phía trước.","Quét gương giữa – trái – phải theo nhịp đều.","Giữ khoảng cách để có thời gian phản ứng.","Dự đoán lỗi của xe khác và chuẩn bị phương án tránh."],"mistakes":["Bám đuôi quá gần","Chỉ nhìn gần trước mũi xe","Ít kiểm tra gương"],"tips":["Nhìn xa để lái mượt","Chậm 1 chút vẫn tốt hơn xử lý muộn"],"qa":[("Tại sao nhìn xa quan trọng?","Nhìn xa giúp bạn nhận nguy cơ sớm và xử lý mềm hơn."),("Lái phòng vệ khác gì lái bình thường?","Lái phòng vệ luôn dự đoán rủi ro, không chờ nguy hiểm xảy ra mới phản ứng.")]},
        {"id":"signs","icon":"🚦","title":"Biển báo giao thông","tag":"Lý thuyết","license":"Tất cả","summary":"Nhận diện biển cấm, nguy hiểm, hiệu lệnh, chỉ dẫn và biển phụ.","goal":"Thấy biển là biết mình phải làm gì ngay.","steps":["Nhìn hình dạng trước: tròn, tam giác hay vuông/chữ nhật.","Nhìn màu chính để đoán nhóm biển.","Đọc nhanh nội dung biển chính và biển phụ nếu có.","Liên hệ ngay với hành động: giảm tốc, cấm rẽ, nhường đường..."],"mistakes":["Nhớ tên biển nhưng không hiểu hành động","Bỏ qua biển phụ","Nhầm biển chỉ dẫn với biển cấm"],"tips":["Học theo nhóm biển nhớ nhanh hơn","Luôn ghép biển với hành động"],"qa":[("Gặp biển cảnh báo nên làm gì?","Giảm tốc, quan sát kỹ và chuẩn bị xử lý tình huống."),("Biển tròn viền đỏ thường là gì?","Thường là nhóm biển cấm hoặc hạn chế.")]},
        {"id":"speed_distance","icon":"📏","title":"Tốc độ & khoảng cách","tag":"An toàn","license":"Tất cả","summary":"Làm chủ tốc độ và khoảng cách theo điều kiện đường, thời tiết và lưu lượng xe.","goal":"Biết khi nào cần chậm lại và giữ khoảng cách bao nhiêu là hợp lý.","steps":["Đi đúng tốc độ cho phép và phù hợp điều kiện thực tế.","Tăng khoảng cách khi trời mưa, đường xấu hoặc tầm nhìn kém.","Không chạy theo tốc độ của xe xung quanh nếu không an toàn.","Luôn để xe có vùng đệm phía trước."],"mistakes":["Chỉ nhìn biển tốc độ mà quên điều kiện đường","Đi sát xe lớn","Tăng tốc vì thấy đường thoáng"],"tips":["Khoảng cách là thời gian để sửa sai","Đường xấu thì giảm tốc trước"],"qa":[("Khi nào phải tăng khoảng cách?","Khi mưa, tối, trơn trượt hoặc giao thông phức tạp."),("Vì sao bám sát xe trước nguy hiểm?","Bạn sẽ không đủ thời gian phanh và tránh nếu xe trước xử lý gấp.")]},
        {"id":"lane","icon":"↔️","title":"Rẽ làn & nhập làn","tag":"Kỹ thuật","license":"B/C/D","summary":"Gương → xi nhan → điểm mù → chuyển mượt, nhập làn đúng tốc độ.","goal":"Chuyển làn êm, rõ ý, an toàn với xe xung quanh.","steps":["Kiểm tra gương giữa và gương bên.","Bật xi nhan sớm, rõ ràng.","Liếc vai kiểm tra điểm mù.","Đưa xe sang làn mới từ từ, giữ tốc độ phù hợp.","Ổn định xe rồi tắt xi nhan."],"mistakes":["Bật xi nhan rồi bẻ lái ngay","Quên điểm mù","Nhập làn với tốc độ quá chênh"],"tips":["Tín hiệu sớm giúp xe khác đọc ý định","Điểm mù là bước không được bỏ"],"qa":[("Tại sao phải kiểm tra điểm mù?","Vì có xe máy hoặc ô tô nhỏ nằm ngoài vùng gương phản chiếu."),("Nhập làn thế nào cho đẹp?","Hòa nhịp tốc độ dòng xe rồi nhập từ từ, không do dự giữa làn.")]},
        {"id":"intersection","icon":"🛣️","title":"Giao lộ & vòng xuyến","tag":"Tình huống","license":"Tất cả","summary":"Giảm tốc – quan sát – nhường đúng – đi dứt khoát khi đã an toàn.","goal":"Xử lý giao lộ tự tin, không chen ẩu và không bỏ sót người đi bộ.","steps":["Giảm tốc từ sớm trước giao lộ.","Quan sát trái – phải – trước – người đi bộ.","Nếu là vòng xuyến: ưu tiên xe đang trong vòng.","Khi đã quyết định đi thì đi dứt khoát."],"mistakes":["Tăng tốc cố lách qua","Dừng giữa nút giao","Không nhường người đi bộ"],"tips":["Giao lộ chậm 1 chút là an toàn hơn rất nhiều","Rõ ràng quan trọng hơn nhanh"],"qa":[("Trong vòng xuyến ưu tiên ai?","Ưu tiên xe đang ở trong vòng xuyến."),("Khi giao lộ đông, nên nghĩ gì đầu tiên?","Ưu tiên an toàn, đừng vì vài giây mà chọn nước đi rủi ro.")]},
        {"id":"rain_night","icon":"🌧️","title":"Đi mưa / ban đêm","tag":"Thực chiến","license":"Tất cả","summary":"Giảm tốc, tăng khoảng cách, dùng đèn đúng và thao tác mềm.","goal":"Giữ xe ổn định khi tầm nhìn kém hoặc mặt đường trơn.","steps":["Giảm tốc so với lúc đường khô.","Tăng khoảng cách với xe trước.","Bật đèn phù hợp, giữ kính sạch.","Không phanh gấp hoặc bẻ lái đột ngột."],"mistakes":["Lái như đường khô","Bám đuôi","Phanh gấp qua vũng nước"],"tips":["Đêm và mưa đều làm tăng quãng đường phản ứng","Giữ thao tác mềm để xe ổn định"],"qa":[("Vì sao đi mưa phải tăng khoảng cách?","Vì đường trơn làm quãng đường phanh dài hơn."),("Đi đêm nên lưu ý gì?","Giữ tầm nhìn tốt, tránh chói và giảm tốc để có thời gian xử lý.")]},
        {"id":"highway","icon":"🛣️","title":"Cao tốc cơ bản","tag":"Nâng cao","license":"B/C/D","summary":"Nhập cao tốc, giữ làn, vượt xe và giữ khoảng cách đúng cách.","goal":"Biết nguyên tắc cốt lõi khi lái xe ở tốc độ cao hơn bình thường.","steps":["Nhập làn bằng cách tăng tốc phù hợp trên làn tăng tốc.","Giữ làn ổn định, tránh chuyển làn liên tục.","Vượt xe khi thực sự cần và đủ khoảng trống.","Không dừng, lùi hoặc quay đầu trái phép trên cao tốc."],"mistakes":["Nhập làn quá chậm","Chuyển làn liên tục","Bám xe trước ở tốc độ cao"],"tips":["Trên cao tốc, khoảng cách còn quan trọng hơn trong phố","Giữ làn ổn định giúp toàn dòng xe an toàn hơn"],"qa":[("Vì sao không nên nhập cao tốc quá chậm?","Vì chênh lệch tốc độ lớn làm tăng nguy cơ va chạm."),("Khi nào nên vượt xe?","Khi thực sự cần và có đủ tầm nhìn, khoảng trống, tín hiệu rõ ràng.")]},
        {"id":"parking","icon":"🅿️","title":"Sa hình & đỗ xe","tag":"Thực hành","license":"B/C/D","summary":"Đi chậm, căn gương, nhớ điểm căn, chỉnh lái ít một.","goal":"Lùi chuồng, ghép xe và qua sa hình mượt hơn, ít lỗi hơn.","steps":["Đi thật chậm để mắt và tay lái kịp xử lý.","Nhìn đủ gương trái – phải – giữa.","Nhớ điểm căn nhưng vẫn bám thực tế.","Khi gần vạch/vật cản, dừng lại quan sát rồi mới xử lý tiếp."],"mistakes":["Đi quá nhanh","Chỉnh lái quá mạnh","Phụ thuộc 1 điểm căn"],"tips":["Sa hình không thi tốc độ","Đi chậm sẽ dễ sửa lỗi"],"qa":[("Vì sao lùi chuồng hay lỗi?","Vì đa số học viên vào bài nhanh hoặc chỉnh lái quá muộn."),("Muốn bớt run khi sa hình?","Đi chậm, chia bài thành từng bước nhỏ và luyện theo quy trình cố định.")]},
        {"id":"braking","icon":"🦶","title":"Phanh & quãng đường dừng","tag":"Kỹ năng","license":"Tất cả","summary":"Hiểu quãng đường phản ứng, quãng đường phanh và cách phanh mượt.","goal":"Biết vì sao tốc độ càng cao thì càng cần vùng đệm an toàn.","steps":["Nhìn xa để không bị phanh muộn.","Phanh sớm và tăng lực phanh dần.","Kết hợp giữ thẳng xe, tránh bẻ lái gấp khi phanh.","Tăng khoảng cách để giảm nhu cầu phanh khẩn cấp."],"mistakes":["Đợi sát mới phanh","Vừa phanh gấp vừa bẻ lái lớn","Đánh giá thấp quãng đường dừng"],"tips":["Phanh tốt bắt đầu từ quan sát sớm","Tốc độ cao không cho bạn sửa sai dễ"],"qa":[("Quãng đường dừng gồm những gì?","Gồm quãng đường phản ứng và quãng đường phanh."),("Vì sao đường trơn nguy hiểm khi phanh?","Vì độ bám giảm nên xe dễ trượt và quãng đường dừng dài hơn.")]},
        {"id":"overtake","icon":"🚘","title":"Vượt xe an toàn","tag":"Kỹ thuật","license":"B/C/D","summary":"Chỉ vượt khi đủ tầm nhìn, đủ khoảng trống và vượt dứt khoát.","goal":"Biết khi nào nên vượt, khi nào tuyệt đối không nên vượt.","steps":["Quan sát biển báo, vạch kẻ đường và tình huống phía trước.","Đảm bảo đủ tầm nhìn và khoảng trống an toàn.","Báo tín hiệu rõ ràng trước khi vượt.","Vượt dứt khoát, sau đó trở lại làn khi đã đủ khoảng cách."],"mistakes":["Vượt ở nơi khuất tầm nhìn","Vượt khi chưa đủ khoảng trống","Trở lại làn quá sớm"],"tips":["Nếu còn phân vân thì chưa nên vượt","Vượt xong cần tạo khoảng cách trước khi về làn"],"qa":[("Khi nào tuyệt đối không nên vượt?","Khi khuất tầm nhìn, gần giao lộ hoặc bị cấm vượt."),("Vì sao cần vượt dứt khoát?","Kéo dài thời gian song song với xe khác làm tăng rủi ro.")]},
        {"id":"hill_start","icon":"⛰️","title":"Lên dốc / xuống dốc","tag":"Thực hành","license":"B/C/D","summary":"Kiểm soát xe trên dốc, tránh tụt dốc và tránh lạm dụng phanh.","goal":"Tự tin xử lý dốc trong thi thực hành và ngoài đường thật.","steps":["Giữ xe ổn định, quan sát và chuẩn bị lực chân hợp lý.","Lên dốc: phối hợp chân phanh / ga / côn (nếu xe số sàn).","Xuống dốc: dùng số phù hợp, không thả trôi xe.","Giữ khoảng cách vì xe trên dốc dễ xử lý kém mượt hơn."],"mistakes":["Thả trôi xe xuống dốc","Nhả thiếu lực khiến tụt dốc","Chỉ lạm dụng phanh khi xuống dốc dài"],"tips":["Xe trên dốc cần bình tĩnh và đều thao tác","Số phù hợp giúp kiểm soát tốt hơn"],"qa":[("Xuống dốc dài cần nhớ gì?","Giữ số phù hợp và kiểm soát tốc độ, không nên về N cho xe trôi."),("Vì sao lên dốc dễ run?","Vì phối hợp tay chân và ước lượng lực cần chính xác hơn mặt đường bằng.")]},
    ]


@st.cache_data(show_spinner=False)
def get_question_bank() -> List[Dict[str, Any]]:
    base = [
        {"set":"Bộ đề nền tảng 1","license":"Tất cả","topic":"defensive","icon":"🧠","q":"Lái phòng vệ nhấn mạnh điều gì nhất?","choices":["Dự đoán trước nguy cơ","Lái thật nhanh","Bám sát xe trước","Ưu tiên vượt xe"],"a":"Dự đoán trước nguy cơ","e":"Lái phòng vệ là chủ động dự đoán và tạo vùng an toàn."},
        {"set":"Bộ đề nền tảng 1","license":"Tất cả","topic":"speed_distance","icon":"📏","q":"Khi trời mưa hoặc tầm nhìn kém, bạn nên làm gì với khoảng cách?","choices":["Tăng khoảng cách an toàn","Giữ nguyên như đường khô","Giảm khoảng cách để khỏi chen vào","Chỉ bấm còi"],"a":"Tăng khoảng cách an toàn","e":"Điều kiện xấu làm quãng đường dừng tăng lên."},
        {"set":"Bộ đề nền tảng 1","license":"Tất cả","topic":"signs","icon":"⛔","q":"Biển tròn viền đỏ thường có ý nghĩa gì?","choices":["Biển cấm/hạn chế","Biển chỉ dẫn","Biển cảnh báo đường dài","Biển hiệu lệnh"],"a":"Biển cấm/hạn chế","e":"Đây là nhóm biển rất hay gặp trong phần lý thuyết."},
        {"set":"Bộ đề nền tảng 1","license":"Tất cả","topic":"signs","icon":"⚠️","q":"Gặp biển cảnh báo nguy hiểm, phản ứng tốt nhất là?","choices":["Giảm tốc và quan sát kỹ","Phanh gấp ngay","Bấm còi liên tục","Bỏ qua vì chưa thấy nguy hiểm"],"a":"Giảm tốc và quan sát kỹ","e":"Biển cảnh báo yêu cầu bạn phòng bị sớm."},
        {"set":"Bộ đề nền tảng 1","license":"Tất cả","topic":"defensive","icon":"👀","q":"Tại sao phải nhìn xa phía trước khi lái xe?","choices":["Để có thêm thời gian xử lý","Để đỡ buồn ngủ","Để chạy nhanh hơn","Không có tác dụng"],"a":"Để có thêm thời gian xử lý","e":"Nhìn xa giúp bạn nhận ra tình huống sớm và lái êm hơn."},
        {"set":"Bộ đề kỹ thuật 1","license":"B/C/D","topic":"lane","icon":"↔️","q":"Khi chuyển làn, thứ tự đúng là gì?","choices":["Gương → Xi nhan → Điểm mù → Chuyển làn","Xi nhan rồi chuyển ngay","Bấm còi rồi lách","Tăng tốc trước"],"a":"Gương → Xi nhan → Điểm mù → Chuyển làn","e":"Quy trình này giúp xe khác nhận biết ý định và giúp bạn tránh vùng điểm mù."},
        {"set":"Bộ đề kỹ thuật 1","license":"B/C/D","topic":"lane","icon":"📶","q":"Bật xi nhan sớm trước khi chuyển làn có tác dụng gì?","choices":["Cho xe khác biết ý định của bạn","Làm xe chạy nhanh hơn","Thay cho kiểm tra điểm mù","Không có tác dụng"],"a":"Cho xe khác biết ý định của bạn","e":"Tín hiệu sớm giúp xe xung quanh phản ứng dễ hơn."},
        {"set":"Bộ đề kỹ thuật 1","license":"B/C/D","topic":"lane","icon":"👀","q":"Điểm mù là gì?","choices":["Vùng không nhìn thấy rõ qua gương","Vùng trước kính lái","Vị trí biển báo","Khoảng cách phanh"],"a":"Vùng không nhìn thấy rõ qua gương","e":"Cần liếc vai nhanh trước khi đổi hướng."},
        {"set":"Bộ đề kỹ thuật 1","license":"B/C/D","topic":"lane","icon":"🛣️","q":"Khi nhập làn trên đường lớn, cách làm an toàn là gì?","choices":["Quan sát, tăng tốc phù hợp và nhập từ từ","Dừng giữa làn nhập","Lao thẳng vào làn","Chỉ bấm còi"],"a":"Quan sát, tăng tốc phù hợp và nhập từ từ","e":"Nhập làn an toàn cần hòa nhịp với dòng xe."},
        {"set":"Bộ đề kỹ thuật 1","license":"B/C/D","topic":"highway","icon":"🚙","q":"Vì sao không nên nhập cao tốc quá chậm?","choices":["Vì tạo chênh lệch tốc độ lớn với dòng xe","Vì sẽ tiết kiệm xăng hơn","Vì đèn sẽ yếu","Không ảnh hưởng gì"],"a":"Vì tạo chênh lệch tốc độ lớn với dòng xe","e":"Chênh lệch tốc độ lớn làm tăng nguy cơ va chạm khi nhập cao tốc."},
        {"set":"Bộ đề tình huống 1","license":"Tất cả","topic":"intersection","icon":"🛣️","q":"Gặp giao lộ không đèn, phản ứng đầu tiên là gì?","choices":["Giảm tốc và quan sát","Tăng tốc","Bấm còi liên tục","Dừng giữa đường"],"a":"Giảm tốc và quan sát","e":"Giao lộ có nhiều hướng xung đột nên cần phòng vệ."},
        {"set":"Bộ đề tình huống 1","license":"Tất cả","topic":"intersection","icon":"🔄","q":"Trong vòng xuyến, bạn cần ưu tiên ai?","choices":["Xe đang ở trong vòng xuyến","Xe chuẩn bị vào vòng","Xe phía sau","Không cần ưu tiên"],"a":"Xe đang ở trong vòng xuyến","e":"Đây là nguyên tắc cơ bản để vào vòng xuyến an toàn."},
        {"set":"Bộ đề tình huống 1","license":"Tất cả","topic":"rain_night","icon":"🌧️","q":"Khi trời mưa to, nên làm gì?","choices":["Giảm tốc và tăng khoảng cách","Phanh gấp","Tắt đèn","Chạy sát xe trước"],"a":"Giảm tốc và tăng khoảng cách","e":"Mưa làm giảm tầm nhìn và độ bám đường nên cần lái êm hơn."},
        {"set":"Bộ đề tình huống 1","license":"Tất cả","topic":"rain_night","icon":"🌙","q":"Khi đi ban đêm trên đường vắng, điều quan trọng nhất là?","choices":["Giữ tầm nhìn và tốc độ phù hợp","Tắt đèn cho đỡ chói","Tăng tốc vì đường vắng","Bám xe trước thật gần"],"a":"Giữ tầm nhìn và tốc độ phù hợp","e":"Ban đêm cần ưu tiên tầm nhìn và thời gian phản ứng."},
        {"set":"Bộ đề tình huống 1","license":"Tất cả","topic":"speed_distance","icon":"📏","q":"Khoảng cách an toàn tăng lên khi nào?","choices":["Khi mưa, trơn trượt hoặc tầm nhìn kém","Chỉ khi đi trong phố","Khi xe mới rửa xong","Không cần tăng"],"a":"Khi mưa, trơn trượt hoặc tầm nhìn kém","e":"Điều kiện xấu làm quãng đường dừng tăng lên."},
        {"set":"Bộ đề tình huống 1","license":"B/C/D","topic":"highway","icon":"🚧","q":"Hành vi nào sai trên cao tốc?","choices":["Dừng xe tùy ý trên làn chạy","Giữ khoảng cách an toàn","Nhập làn đúng tốc độ","Bật tín hiệu trước khi đổi làn"],"a":"Dừng xe tùy ý trên làn chạy","e":"Dừng tùy ý trên làn chạy cao tốc cực kỳ nguy hiểm và sai luật."},
        {"set":"Bộ đề sa hình 1","license":"B/C/D","topic":"parking","icon":"🪞","q":"Lỗi phổ biến khi lùi chuồng là gì?","choices":["Đi quá nhanh và căn gương sai","Đi chậm","Nhìn gương","Bật xi nhan"],"a":"Đi quá nhanh và căn gương sai","e":"Lùi chuồng cần chậm và chính xác."},
        {"set":"Bộ đề sa hình 1","license":"B/C/D","topic":"parking","icon":"📏","q":"Yếu tố quan trọng nhất khi ghép xe là gì?","choices":["Đi chậm và quan sát gương","Nhấn ga mạnh","Không cần nhìn gương","Chỉ nhớ một điểm căn"],"a":"Đi chậm và quan sát gương","e":"Đi chậm giúp bạn kiểm soát không gian và chỉnh lái chính xác."},
        {"set":"Bộ đề sa hình 1","license":"B/C/D","topic":"parking","icon":"⬅️","q":"Khi thấy xe lệch trong lúc lùi, nên làm gì?","choices":["Dừng lại, nhìn gương và chỉnh lái từng chút","Tăng ga để vào nhanh","Bỏ qua","Đạp ga rồi phanh gấp"],"a":"Dừng lại, nhìn gương và chỉnh lái từng chút","e":"Sa hình ưu tiên chậm và chính xác, không cần vội."},
        {"set":"Bộ đề sa hình 1","license":"B/C/D","topic":"parking","icon":"🅿️","q":"Vì sao sa hình nên đi thật chậm?","choices":["Để não và mắt kịp xử lý vị trí xe","Để xe đỡ tốn xăng","Vì xe yếu","Không có lý do"],"a":"Để não và mắt kịp xử lý vị trí xe","e":"Đi chậm cho phép bạn chỉnh lái và sửa lỗi an toàn hơn."},
        {"set":"Bộ đề nâng cao 1","license":"B/C/D","topic":"braking","icon":"🦶","q":"Quãng đường dừng bao gồm những gì?","choices":["Quãng đường phản ứng và quãng đường phanh","Chỉ quãng đường phanh","Chỉ khoảng cách đến xe trước","Không liên quan tốc độ"],"a":"Quãng đường phản ứng và quãng đường phanh","e":"Bạn cần thời gian phản ứng trước khi xe thực sự bắt đầu giảm tốc."},
        {"set":"Bộ đề nâng cao 1","license":"B/C/D","topic":"overtake","icon":"🚘","q":"Khi nào không nên vượt xe?","choices":["Khi khuất tầm nhìn hoặc gần giao lộ","Khi xe trước đi chậm","Khi bạn đang vội","Khi có làn trống ngắn"],"a":"Khi khuất tầm nhìn hoặc gần giao lộ","e":"Đây là các vị trí rủi ro cao và thường bị cấm vượt."},
        {"set":"Bộ đề nâng cao 1","license":"B/C/D","topic":"hill_start","icon":"⛰️","q":"Xuống dốc dài, thói quen tốt là?","choices":["Giữ số phù hợp và kiểm soát tốc độ","Về N cho trôi","Tắt máy","Chỉ dùng còi"],"a":"Giữ số phù hợp và kiểm soát tốc độ","e":"Xuống dốc cần kiểm soát tốc độ và tận dụng phanh động cơ."},
        {"set":"Bộ đề nâng cao 1","license":"Tất cả","topic":"defensive","icon":"📏","q":"Khi xe trước phanh gấp, điều nào giúp bạn an toàn nhất?","choices":["Đã giữ khoảng cách từ trước","Đang bấm còi","Xe đẹp","Đường rộng"],"a":"Đã giữ khoảng cách từ trước","e":"Phòng vệ tốt bắt đầu từ khoảng cách an toàn."},
        {"set":"Bộ đề nâng cao 1","license":"Tất cả","topic":"signs","icon":"🚸","q":"Gặp khu vực gần trường học, bạn nên?","choices":["Giảm tốc và quan sát kỹ người đi bộ","Tăng tốc cho nhanh qua","Bấm còi liên tục","Chỉ nhìn xe trước"],"a":"Giảm tốc và quan sát kỹ người đi bộ","e":"Khu vực trường học có nhiều nguy cơ người đi bộ băng qua đường."},
        {"set":"Bộ đề nâng cao 1","license":"Tất cả","topic":"intersection","icon":"🚶","q":"Tại vạch qua đường có người đi bộ, bạn nên?","choices":["Nhường đường an toàn","Lách qua nhanh","Bấm còi để họ né","Tăng tốc"],"a":"Nhường đường an toàn","e":"Người đi bộ tại vạch sang đường cần được ưu tiên đúng luật."},
        {"set":"Bộ đề nâng cao 1","license":"B/C/D","topic":"lane","icon":"🚗","q":"Khi xe bên cạnh chạy song song quá gần, bạn nên?","choices":["Giữ ổn định và chờ khoảng trống rõ hơn","Ép nhanh sang làn","Tăng tốc đột ngột","Phanh gấp không nhìn gương"],"a":"Giữ ổn định và chờ khoảng trống rõ hơn","e":"Không có khoảng trống rõ ràng thì chưa nên đổi làn."},
        {"set":"Bộ đề nâng cao 1","license":"Tất cả","topic":"rain_night","icon":"💡","q":"Đi đêm gặp xe ngược chiều đèn chói, cách xử lý tốt là?","choices":["Nhìn lệch phải, giảm tốc vừa phải","Nhìn thẳng vào đèn","Tăng tốc vượt qua nhanh","Tắt đèn xe mình"],"a":"Nhìn lệch phải, giảm tốc vừa phải","e":"Nhìn lệch giúp hạn chế chói và giữ định hướng tốt hơn."},
        {"set":"Bộ đề nâng cao 1","license":"B/C/D","topic":"highway","icon":"🧭","q":"Khi gần lối ra cao tốc, bạn nên?","choices":["Chuẩn bị từ sớm và chuyển làn đúng tín hiệu","Cắt ngang nhiều làn sát lối ra","Phanh gấp giữa làn","Dừng lại suy nghĩ"],"a":"Chuẩn bị từ sớm và chuyển làn đúng tín hiệu","e":"Trên cao tốc, mọi quyết định nên chuẩn bị sớm và rõ ràng."},
        {"set":"Bộ đề nâng cao 1","license":"Tất cả","topic":"speed_distance","icon":"⏱️","q":"Đi nhanh hơn đồng nghĩa với điều gì?","choices":["Quãng đường xử lý và dừng xe dài hơn","Phanh sẽ ngắn hơn","Ít rủi ro hơn","Không thay đổi gì"],"a":"Quãng đường xử lý và dừng xe dài hơn","e":"Tốc độ càng cao thì thời gian phản ứng càng quý giá."},
        {"set":"Bộ đề mô phỏng 1","license":"B/C/D","topic":"lane","icon":"🪞","q":"Trước khi chuyển làn, kiểm tra nào thường bị người mới bỏ sót?","choices":["Điểm mù","Màu sơn xe","Biển số xe sau","Âm thanh radio"],"a":"Điểm mù","e":"Điểm mù là nguyên nhân phổ biến gây chuyển làn thiếu an toàn."},
        {"set":"Bộ đề mô phỏng 1","license":"Tất cả","topic":"defensive","icon":"🛡️","q":"Mục tiêu của vùng đệm an toàn là gì?","choices":["Cho bạn thời gian xử lý","Giúp đi nhanh hơn","Để người khác không chen","Để đỡ phải nhìn gương"],"a":"Cho bạn thời gian xử lý","e":"Vùng đệm tạo thời gian và không gian để tránh nguy cơ."},
        {"set":"Bộ đề mô phỏng 1","license":"B/C/D","topic":"braking","icon":"🚨","q":"Nếu phát hiện nguy cơ phía trước từ sớm, cách phanh tốt là?","choices":["Phanh sớm và tăng lực dần","Đợi thật gần rồi phanh mạnh","Vừa phanh vừa đánh lái gắt","Bỏ chân khỏi phanh hoàn toàn"],"a":"Phanh sớm và tăng lực dần","e":"Phanh sớm giúp xe ổn định và êm hơn."},
        {"set":"Bộ đề mô phỏng 1","license":"B/C/D","topic":"overtake","icon":"👁️","q":"Dấu hiệu cho thấy chưa nên vượt xe là gì?","choices":["Tầm nhìn bị hạn chế","Đường rất rộng","Bạn có thời gian","Xe trước đi quá chậm"],"a":"Tầm nhìn bị hạn chế","e":"Không đủ tầm nhìn thì không đủ điều kiện vượt an toàn."},
        {"set":"Bộ đề mô phỏng 1","license":"B/C/D","topic":"hill_start","icon":"🧗","q":"Lên dốc với xe số sàn cần chú ý điều gì?","choices":["Phối hợp chân ga, côn và phanh hợp lý","Chỉ nhấn ga mạnh","Về N cho nhẹ xe","Bỏ quan sát gương"],"a":"Phối hợp chân ga, côn và phanh hợp lý","e":"Lên dốc cần phối hợp tay chân chính xác để không tụt dốc."},
        {"set":"Bộ đề mô phỏng 1","license":"C1/C/D","topic":"speed_distance","icon":"🚚","q":"Xe tải hoặc xe lớn cần khoảng cách dừng như thế nào?","choices":["Thường dài hơn xe nhỏ","Luôn ngắn hơn","Không khác biệt","Chỉ phụ thuộc màu xe"],"a":"Thường dài hơn xe nhỏ","e":"Xe lớn nặng hơn, quán tính lớn hơn nên thường cần khoảng cách dừng dài hơn."},
        {"set":"Bộ đề mô phỏng 1","license":"C1/C/D","topic":"defensive","icon":"📦","q":"Khi chở hàng hoặc nhiều người, điều gì càng quan trọng?","choices":["Lái mượt và giữ khoảng cách","Phanh gấp thường xuyên","Chuyển làn liên tục","Tăng tốc nhanh"],"a":"Lái mượt và giữ khoảng cách","e":"Tải trọng và hành khách khiến mọi thao tác cần êm hơn."},
    ]
    # mở rộng thêm bằng bản sao có điều chỉnh nhẹ để tạo nhiều đề lớn hơn
    expanded = []
    suffixes = [("Bộ đề tổng hợp 2", "Đây là câu ôn tập mở rộng để tăng độ bao phủ kiến thức."), ("Bộ đề tổng hợp 3", "Phiên bản mở rộng giúp bạn luyện thêm với cùng nguyên tắc xử lý.")]
    for q in base:
        expanded.append(q)
        if q['set'] in {"Bộ đề nền tảng 1", "Bộ đề kỹ thuật 1", "Bộ đề tình huống 1", "Bộ đề sa hình 1"}:
            for newset, extra in suffixes[:1]:
                nq = dict(q)
                nq['set'] = newset
                nq['e'] = q['e'] + ' ' + extra
                expanded.append(nq)
    return expanded


TOPIC_LABELS = {
    "defensive": "🧠 Tư duy phòng vệ",
    "signs": "🚦 Biển báo giao thông",
    "speed_distance": "📏 Tốc độ & khoảng cách",
    "lane": "↔️ Rẽ làn & nhập làn",
    "intersection": "🛣️ Giao lộ & vòng xuyến",
    "rain_night": "🌧️ Đi mưa / ban đêm",
    "highway": "🛣️ Cao tốc cơ bản",
    "parking": "🅿️ Sa hình & đỗ xe",
    "braking": "🦶 Phanh & quãng đường dừng",
    "overtake": "🚘 Vượt xe an toàn",
    "hill_start": "⛰️ Lên dốc / xuống dốc",
}


def _topic_svgs(topic: str):
    snippets = {
        "lane": ["<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><rect x='0' y='52' width='320' height='80' fill='#334155'/><line x1='0' y1='92' x2='320' y2='92' stroke='white' stroke-width='4' stroke-dasharray='18 12'/><rect x='38' y='97' width='56' height='24' rx='10' fill='#f59e0b'/><path d='M66 110 C120 110,150 110,198 78 C220 64,250 64,280 64' fill='none' stroke='#22c55e' stroke-width='5' stroke-dasharray='10 8'/></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><circle cx='92' cy='88' r='24' fill='#111b2f' stroke='#60a5fa'/><text x='92' y='95' text-anchor='middle' fill='white'>🪞</text><circle cx='160' cy='88' r='24' fill='#111b2f' stroke='#facc15'/><text x='160' y='95' text-anchor='middle' fill='white'>↗️</text><circle cx='228' cy='88' r='24' fill='#111b2f' stroke='#22c55e'/><text x='228' y='95' text-anchor='middle' fill='white'>👀</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><rect x='28' y='62' width='86' height='34' rx='12' fill='#3b82f6'/><rect x='214' y='62' width='86' height='34' rx='12' fill='#f59e0b'/><text x='160' y='40' text-anchor='middle' fill='#e2e8f0'>Khoảng trống đủ an toàn</text><line x1='114' y1='79' x2='214' y2='79' stroke='#22c55e' stroke-width='4' stroke-dasharray='10 8'/></svg>"],
        "signs": ["<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><circle cx='80' cy='90' r='34' fill='none' stroke='#ef4444' stroke-width='10'/><polygon points='200,48 240,116 160,116' fill='#facc15'/><rect x='246' y='56' width='44' height='44' rx='8' fill='#2563eb'/><text x='268' y='84' text-anchor='middle' fill='white'>P</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='68' y='90' font-size='44'>⛔</text><text x='140' y='90' font-size='44'>⚠️</text><text x='220' y='90' font-size='44'>ℹ️</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='160' y='44' text-anchor='middle' fill='#e2e8f0'>Nhìn hình dạng → màu → hành động</text><rect x='30' y='70' width='60' height='60' rx='12' fill='none' stroke='#ef4444' stroke-width='8'/><polygon points='160,70 200,130 120,130' fill='#facc15'/><rect x='230' y='74' width='60' height='52' rx='10' fill='#2563eb'/></svg>"],
        "speed_distance": ["<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><rect x='24' y='92' width='62' height='24' rx='8' fill='#f59e0b'/><rect x='210' y='92' width='62' height='24' rx='8' fill='#3b82f6'/><line x1='86' y1='104' x2='210' y2='104' stroke='#22c55e' stroke-width='5' stroke-dasharray='10 8'/><text x='160' y='62' text-anchor='middle' fill='#e2e8f0'>Khoảng cách an toàn</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><circle cx='160' cy='92' r='42' fill='none' stroke='#e5e7eb' stroke-width='8'/><text x='160' y='100' text-anchor='middle' fill='white' font-size='28'>50</text><text x='160' y='146' text-anchor='middle' fill='#e2e8f0'>Đi chậm lại khi điều kiện xấu</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='70' y='84' font-size='34'>☀️</text><text x='150' y='84' font-size='34'>🌧️</text><text x='230' y='84' font-size='34'>🌙</text><text x='160' y='134' text-anchor='middle' fill='#e2e8f0'>Mưa / đêm = tăng khoảng cách</text></svg>"],
        "intersection": ["<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><rect x='0' y='70' width='320' height='38' fill='#334155'/><rect x='138' y='0' width='44' height='180' fill='#334155'/><line x1='0' y1='89' x2='320' y2='89' stroke='white' stroke-width='3' stroke-dasharray='14 10'/><line x1='160' y1='0' x2='160' y2='180' stroke='white' stroke-width='3' stroke-dasharray='14 10'/></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><circle cx='160' cy='90' r='52' fill='none' stroke='#94a3b8' stroke-width='10'/><rect x='148' y='14' width='24' height='28' rx='8' fill='#f59e0b'/><text x='160' y='154' text-anchor='middle' fill='#e2e8f0'>Vòng xuyến: ưu tiên xe trong vòng</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='70' y='82' font-size='28'>⬅️</text><text x='160' y='82' font-size='28'>➡️</text><text x='250' y='82' font-size='28'>🚶</text><text x='160' y='136' text-anchor='middle' fill='#e2e8f0'>Quan sát trái – phải – người đi bộ</text></svg>"],
        "rain_night": ["<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='70' y='70' font-size='34'>☁️</text><line x1='60' y1='84' x2='56' y2='108' stroke='#38bdf8' stroke-width='4'/><line x1='74' y1='84' x2='70' y2='108' stroke='#38bdf8' stroke-width='4'/><rect x='116' y='96' width='74' height='26' rx='10' fill='#f59e0b'/></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='100' y='86' font-size='30'>🌙</text><text x='158' y='86' font-size='30'>💡</text><text x='210' y='86' font-size='30'>🚗</text><text x='160' y='136' text-anchor='middle' fill='#e2e8f0'>Giữ tầm nhìn và giảm tốc</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><rect x='36' y='92' width='56' height='22' rx='8' fill='#f59e0b'/><rect x='222' y='92' width='56' height='22' rx='8' fill='#3b82f6'/><line x1='92' y1='103' x2='222' y2='103' stroke='#22c55e' stroke-width='5' stroke-dasharray='10 8'/></svg>"],
        "highway": ["<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><rect x='0' y='68' width='320' height='56' fill='#334155'/><line x1='0' y1='96' x2='320' y2='96' stroke='white' stroke-width='3' stroke-dasharray='16 10'/><path d='M0 146 C60 146,82 110,120 110' fill='none' stroke='#22c55e' stroke-width='5'/></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='90' y='86' font-size='34'>🚗</text><text x='150' y='86' font-size='34'>🚙</text><text x='220' y='86' font-size='34'>🚚</text><text x='160' y='136' text-anchor='middle' fill='#e2e8f0'>Giữ làn ổn định, giữ khoảng cách</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='160' y='54' text-anchor='middle' fill='#e2e8f0'>Lối ra cần chuẩn bị từ sớm</text><path d='M40 118 L160 118' stroke='#3b82f6' stroke-width='8'/><path d='M160 118 C200 118,220 90,272 90' fill='none' stroke='#22c55e' stroke-width='8'/></svg>"],
        "parking": ["<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><rect x='26' y='46' width='268' height='96' rx='16' fill='none' stroke='#cbd5e1' stroke-width='4'/><line x1='90' y1='46' x2='90' y2='142' stroke='#cbd5e1' stroke-width='2'/><line x1='154' y1='46' x2='154' y2='142' stroke='#cbd5e1' stroke-width='2'/><rect x='164' y='82' width='56' height='28' rx='10' fill='#3b82f6'/></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='92' y='88' font-size='30'>🪞</text><text x='160' y='88' font-size='30'>👀</text><text x='228' y='88' font-size='30'>↩️</text><text x='160' y='136' text-anchor='middle' fill='#e2e8f0'>Chậm – nhìn gương – chỉnh nhỏ</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='160' y='78' text-anchor='middle' fill='#e2e8f0'>Điểm căn chỉ là gợi ý</text><circle cx='100' cy='98' r='18' fill='#f59e0b'/><circle cx='220' cy='98' r='18' fill='#3b82f6'/></svg>"],
        "braking": ["<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='160' y='52' text-anchor='middle' fill='#e2e8f0'>Phản ứng + phanh = quãng đường dừng</text><rect x='36' y='102' width='70' height='22' rx='8' fill='#f59e0b'/><rect x='214' y='102' width='70' height='22' rx='8' fill='#3b82f6'/><line x1='106' y1='113' x2='214' y2='113' stroke='#ef4444' stroke-width='5' stroke-dasharray='10 8'/></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='94' y='90' font-size='32'>⚠️</text><text x='160' y='90' font-size='32'>🦶</text><text x='228' y='90' font-size='32'>🚗</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><circle cx='160' cy='90' r='44' fill='none' stroke='#e2e8f0' stroke-width='8'/><text x='160' y='98' text-anchor='middle' fill='white' font-size='30'>80</text><text x='160' y='140' text-anchor='middle' fill='#e2e8f0'>Tốc độ cao = dừng dài hơn</text></svg>"],
        "overtake": ["<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><rect x='22' y='94' width='60' height='22' rx='8' fill='#f59e0b'/><rect x='122' y='94' width='60' height='22' rx='8' fill='#3b82f6'/><path d='M90 105 C108 80,124 74,142 74' fill='none' stroke='#22c55e' stroke-width='5'/></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='160' y='48' text-anchor='middle' fill='#e2e8f0'>Chỉ vượt khi đủ tầm nhìn</text><text x='90' y='104' font-size='30'>👁️</text><text x='160' y='104' font-size='30'>➡️</text><text x='230' y='104' font-size='30'>🚘</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='100' y='90' font-size='34'>🚫</text><text x='160' y='90' font-size='34'>↕️</text><text x='220' y='90' font-size='34'>🚘</text><text x='160' y='136' text-anchor='middle' fill='#e2e8f0'>Khuất tầm nhìn: không vượt</text></svg>"],
        "hill_start": ["<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><path d='M30 130 L120 130 L220 70 L290 70' stroke='#94a3b8' stroke-width='8' fill='none'/><rect x='164' y='82' width='48' height='24' rx='8' fill='#f59e0b'/></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='100' y='88' font-size='30'>⛰️</text><text x='160' y='88' font-size='30'>🦶</text><text x='220' y='88' font-size='30'>⚙️</text><text x='160' y='136' text-anchor='middle' fill='#e2e8f0'>Phối hợp ga – phanh – số</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='160' y='48' text-anchor='middle' fill='#e2e8f0'>Xuống dốc: không thả trôi xe</text><text x='160' y='100' font-size='38' text-anchor='middle'>🚫N</text></svg>"],
        "defensive": ["<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='72' y='90' font-size='28'>👁️</text><text x='140' y='90' font-size='28'>🪞</text><text x='208' y='90' font-size='28'>🛡️</text><text x='160' y='136' text-anchor='middle' fill='#e2e8f0'>Nhìn xa – quét rộng – dự đoán</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><rect x='26' y='96' width='54' height='20' rx='8' fill='#f59e0b'/><rect x='240' y='96' width='54' height='20' rx='8' fill='#3b82f6'/><text x='160' y='62' text-anchor='middle' fill='#e2e8f0'>Giữ vùng đệm an toàn</text></svg>","<svg viewBox='0 0 320 180' width='100%' height='170'><rect width='320' height='180' fill='#0e1628'/><text x='160' y='50' text-anchor='middle' fill='#e2e8f0'>Tự hỏi: nếu xe trước phanh gấp?</text><text x='160' y='104' font-size='36' text-anchor='middle'>❓🚗</text></svg>"],
    }
    return snippets.get(topic, snippets['defensive'])


def _show_visual_gallery(topic: str, key_prefix: str = 'g'):
    visuals = _topic_svgs(topic)
    cols = st.columns(len(visuals))
    for col, svg in zip(cols, visuals):
        with col:
            components.html(f"<div class='mini-visual'>{svg}</div>", height=190)


def _lesson_detail(lesson: Dict[str, Any], progress: Dict[str, Any]):
    st.markdown(f"### {lesson['icon']} {lesson['title']}")
    st.caption(f"{lesson['summary']} · Phù hợp: {lesson['license']}")
    _show_visual_gallery(lesson['id'], lesson['id'])
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.markdown(f"<div class='lesson-banner'><div class='stat-row'><span class='pill purple'>{lesson['tag']}</span><span class='pill blue'>{lesson['license']}</span></div><h4>🎯 Mục tiêu</h4><p>{lesson['goal']}</p><h4>📚 Quy trình từng bước</h4><ol>" + ''.join([f"<li>{s}</li>" for s in lesson['steps']]) + "</ol></div>", unsafe_allow_html=True)
        ui.speak_button(lesson['title'] + '. ' + ' '.join(lesson['steps']), '🔊 Nghe hướng dẫn bài học', key=f"drive_lesson_{lesson['id']}")
    with c2:
        st.markdown("<div class='glass-card'><h4>🚫 Lỗi dễ gặp</h4><ul>" + ''.join([f"<li>{s}</li>" for s in lesson['mistakes']]) + "</ul><h4>✅ Mẹo nhớ nhanh</h4><ul>" + ''.join([f"<li>{s}</li>" for s in lesson['tips']]) + "</ul></div>", unsafe_allow_html=True)
        for q, a in lesson['qa']:
            with st.expander(f"❓ {q}"):
                st.write(a)
    conf = st.slider("Mức tự tin hiện tại", 1, 10, 6, key=f"confidence_{lesson['id']}")
    if conf <= 4:
        st.warning("Bạn nên xem lại hình minh họa, nghe hướng dẫn một lần nữa và làm quiz của chủ đề này trước.")
    elif conf <= 7:
        st.info("Khá tốt. Hãy làm quiz và đọc kỹ phần giải thích để khóa kiến thức.")
    else:
        st.success("Rất tốt. Bạn nên sang phần mô phỏng AI hoặc bộ đề tổng hợp để luyện phản xạ.")
    if st.button("✅ Đánh dấu đã học bài này", key=f"done_{lesson['id']}"):
        completed = set(progress.setdefault('completed', [])); completed.add(lesson['title']); progress['completed'] = sorted(completed); st.session_state['_save_drive'] = True; st.success('Đã đánh dấu hoàn thành.')


def _simulation_panel():
    st.markdown("### 🤖 Mô phỏng AI học lái xe chuyên nghiệp")
    st.caption("Nhập tình huống, app đánh giá rủi ro, gợi ý đúng/sai và đưa quy trình xử lý.")
    c1, c2, c3 = st.columns(3)
    with c1:
        scene = st.selectbox("Tình huống", ["Chuyển làn", "Giao lộ đông", "Đi mưa", "Lùi chuồng", "Vòng xuyến", "Xuống dốc dài", "Nhập cao tốc", "Vượt xe"], key='sim_scene')
    with c2:
        speed = st.slider("Tốc độ hiện tại (km/h)", 5, 120, 40, 5, key='sim_speed')
    with c3:
        density = st.select_slider("Mật độ giao thông", ["Thấp", "Vừa", "Cao"], value="Vừa", key='sim_density')
    alert = st.select_slider("Mức tập trung", ["Cao", "Trung bình", "Thấp"], value="Trung bình", key='sim_alert')
    weather = st.selectbox("Điều kiện", ["Khô ráo", "Mưa nhẹ", "Mưa to", "Ban đêm"], key='sim_weather')
    risk = 15 + (speed > 70) * 20 + (speed > 50) * 10 + {"Thấp": 0, "Vừa": 12, "Cao": 24}[density] + {"Cao": 0, "Trung bình": 10, "Thấp": 20}[alert] + {"Khô ráo":0, "Mưa nhẹ":8, "Mưa to":16, "Ban đêm":10}[weather]
    if scene in ["Đi mưa", "Giao lộ đông", "Vòng xuyến", "Nhập cao tốc", "Vượt xe"]: risk += 10
    if scene == "Lùi chuồng" and speed > 20: risk += 20
    risk = min(100, risk)
    st.progress(risk/100)
    if risk < 35: st.success(f"Rủi ro {risk}/100 · Khá an toàn.")
    elif risk < 70: st.warning(f"Rủi ro {risk}/100 · Cần cẩn thận hơn.")
    else: st.error(f"Rủi ro {risk}/100 · Nguy cơ cao, hãy giảm tốc và ổn định lại xe.")
    suggestions = {
        "Chuyển làn": ["Nhìn gương", "Bật xi nhan sớm", "Kiểm tra điểm mù", "Chuyển làn nhẹ và giữ tốc độ"],
        "Giao lộ đông": ["Giảm tốc từ sớm", "Quét trái – phải – trước", "Nhường khi chưa chắc chắn", "Đi dứt khoát khi đã an toàn"],
        "Đi mưa": ["Giảm tốc", "Tăng khoảng cách", "Tránh phanh gấp", "Giữ thao tác mềm"],
        "Lùi chuồng": ["Đi rất chậm", "Nhìn cả hai gương", "Chỉnh lái ít một", "Dừng lại khi gần vạch"],
        "Vòng xuyến": ["Nhường xe trong vòng", "Giảm tốc khi vào", "Giữ làn ổn định", "Xi nhan khi ra vòng"],
        "Xuống dốc dài": ["Giữ số phù hợp", "Không thả trôi xe", "Kiểm soát tốc độ đều", "Quan sát xa để xử lý sớm"],
        "Nhập cao tốc": ["Tăng tốc phù hợp", "Quan sát gương và điểm mù", "Nhập từ từ vào làn", "Giữ khoảng cách sau khi nhập"],
        "Vượt xe": ["Xác nhận đủ tầm nhìn", "Báo tín hiệu rõ", "Vượt dứt khoát", "Về làn khi đã đủ khoảng cách"],
    }
    ui.pills(suggestions[scene], 'purple')
    wrong = {
        "Chuyển làn": "Bật xi nhan và lách ngay khi chưa kiểm tra điểm mù.",
        "Giao lộ đông": "Cố chen nhanh để đi trước vài giây.",
        "Đi mưa": "Chạy như trời khô và phanh gấp.",
        "Lùi chuồng": "Đi nhanh để vào bài cho lẹ.",
        "Vòng xuyến": "Không nhường xe trong vòng.",
        "Xuống dốc dài": "Về N cho xe trôi.",
        "Nhập cao tốc": "Nhập làn quá chậm hoặc cắt ngang vội vàng.",
        "Vượt xe": "Vượt khi khuất tầm nhìn hoặc sát giao lộ.",
    }
    st.success("Đúng: " + ' → '.join(suggestions[scene]))
    st.error("Sai thường gặp: " + wrong[scene])


def render_dashboard(profile: Dict[str, Any], save_cb) -> None:
    st.title("🚗 Driving Academy Final Ultra Pro")
    st.caption("Final Ultra Pro: ngân hàng đề cực lớn hơn, nhiều mô phỏng/ảnh động SVG hơn, học theo hạng bằng và luyện phản xạ chuyên nghiệp hơn.")
    progress = profile.setdefault('driving', {})
    progress.setdefault('completed', [])
    progress.setdefault('quiz_history', [])
    progress.setdefault('wrong_bank', {})
    lessons = get_lessons()
    license_packs = get_license_packs()
    tabs = st.tabs(["📂 Học theo hạng bằng", "📚 Thư viện module", "📖 Bài học chi tiết", "🖼️ Gallery minh họa", "🤖 AI mô phỏng", "📈 Tiến độ"])
    with tabs[0]:
        cols = st.columns(4)
        for i, pack in enumerate(license_packs):
            with cols[i % 4]:
                st.markdown(f"<div class='license-card'><div class='pill purple'>{pack['code']}</div><h3>{pack['title']}</h3><p class='muted'>{pack['focus']}</p><ul>" + ''.join([f"<li>{x}</li>" for x in pack['items']]) + "</ul></div>", unsafe_allow_html=True)
        st.info("Bạn có thể học theo hạng bằng trước, sau đó vào từng module để học sâu và làm quiz.")
    with tabs[1]:
        cols = st.columns(4)
        for i, lesson in enumerate(lessons):
            with cols[i % 4]:
                ui.card(lesson['icon'], lesson['title'], lesson['summary'], f"{lesson['tag']} · {lesson['license']}")
                if st.button("Mở bài học", key=f"open_{lesson['id']}"):
                    st.session_state['driving_current_lesson'] = lesson['id']
        st.info("Lộ trình tốt nhất: xem module → nghe hướng dẫn → làm quiz theo bộ đề → ôn câu sai → mô phỏng AI.")
    with tabs[2]:
        current = st.session_state.get('driving_current_lesson', lessons[0]['id'])
        lesson_titles = [l['title'] for l in lessons]
        current_idx = next((i for i,l in enumerate(lessons) if l['id'] == current), 0)
        selected_title = st.selectbox("Chọn module", lesson_titles, index=current_idx)
        lesson = next(l for l in lessons if l['title'] == selected_title)
        st.session_state['driving_current_lesson'] = lesson['id']
        _lesson_detail(lesson, progress)
    with tabs[3]:
        st.markdown("### 🖼️ Gallery minh họa chủ đề")
        for topic, label in TOPIC_LABELS.items():
            with st.expander(label):
                _show_visual_gallery(topic, topic)
                st.caption("Hãy nhìn hình, đọc tên bước xử lý và tự nói lại quy trình bằng lời của bạn.")
    with tabs[4]:
        _simulation_panel()
    with tabs[5]:
        c1, c2, c3 = st.columns(3)
        with c1: ui.metric_card("Bài đã học", len(progress.get('completed', [])), "module")
        with c2: ui.metric_card("Lượt quiz", len(progress.get('quiz_history', [])), "lần")
        with c3: ui.metric_card("Câu cần ôn", len(progress.get('wrong_bank', {})), "câu")
        if progress.get('completed'): ui.pills(progress['completed'], 'green')
    if st.session_state.pop('_save_drive', False): save_cb(profile)


def _question_visual(topic: str, icon: str):
    st.markdown(f"<div class='panel' style='padding:.75rem'><div class='stat-row'><span class='pill blue'>{TOPIC_LABELS.get(topic, topic)}</span><span class='pill purple'>{icon}</span></div><div class='tiny-muted'>Mỗi câu có nhiều minh họa để giúp nhớ theo hình và tình huống.</div></div>", unsafe_allow_html=True)
    _show_visual_gallery(topic, 'q'+topic)


def render_quiz(profile: Dict[str, Any], save_cb) -> None:
    st.title("🧪 Driving Quiz Final Ultra Pro")
    st.caption("Ngân hàng đề thi lái xe cực lớn hơn, lọc theo bộ đề / hạng bằng / chủ đề, có nhiều minh họa và giải thích đúng sai cho từng câu.")
    driving = profile.setdefault('driving', {})
    wrong_bank = driving.setdefault('wrong_bank', {})
    questions = get_question_bank()
    set_options = ["Tất cả"] + sorted({q['set'] for q in questions})
    license_options = ["Tất cả"] + sorted({q['license'] for q in questions})
    topic_options = ["Tất cả"] + list(TOPIC_LABELS.keys())
    selected_set = st.selectbox("Chọn bộ đề", set_options)
    selected_license = st.selectbox("Lọc theo hạng bằng", license_options)
    selected_topic = st.selectbox("Lọc theo chủ đề", topic_options, format_func=lambda x: "Tất cả chủ đề" if x == "Tất cả" else TOPIC_LABELS[x])
    mode = st.radio("Chế độ", ["Quiz ngẫu nhiên", "Chỉ ôn câu sai"], horizontal=True)
    pool = questions
    if selected_set != "Tất cả": pool = [q for q in pool if q['set'] == selected_set]
    if selected_license != "Tất cả": pool = [q for q in pool if q['license'] == selected_license]
    if selected_topic != "Tất cả": pool = [q for q in pool if q['topic'] == selected_topic]
    if mode == 'Chỉ ôn câu sai' and wrong_bank:
        pool = [q for q in pool if q['q'] in wrong_bank]
        if not pool:
            st.info("Bộ lọc hiện tại chưa có câu sai. App sẽ dùng ngân hàng câu hỏi thường.")
            pool = questions
    count = st.slider("Số câu mỗi lượt", 5, min(12, len(pool)) if pool else 5, min(8, len(pool)) if pool else 5)
    if not pool:
        st.warning('Không có câu hỏi phù hợp với bộ lọc hiện tại.')
        return
    quiz = random.sample(pool, min(count, len(pool)))
    with st.form('driving_quiz_master'):
        answers = []
        for idx, q in enumerate(quiz, 1):
            st.markdown(f"### Câu {idx}")
            _question_visual(q['topic'], q['icon'])
            st.markdown(f"**{q['q']}**")
            answers.append(st.radio("Chọn đáp án", q['choices'], key=f"dq_{idx}_{q['q']}", label_visibility='collapsed'))
        submitted = st.form_submit_button('📌 Chấm điểm & xem giải thích')
    if submitted:
        correct = 0
        st.markdown("## 📋 Kết quả chi tiết")
        for i, (q, a) in enumerate(zip(quiz, answers), 1):
            with st.container(border=True):
                st.markdown(f"**Câu {i}. {q['q']}**")
                st.caption(f"Bộ đề: {q['set']} · Hạng bằng: {q['license']}")
                if a == q['a']:
                    correct += 1
                    st.success(f"✅ Đúng · Đáp án: {q['a']}")
                    if q['q'] in wrong_bank:
                        wrong_bank[q['q']]['fixed'] = wrong_bank[q['q']].get('fixed', 0) + 1
                        if wrong_bank[q['q']]['fixed'] >= 2: wrong_bank.pop(q['q'], None)
                else:
                    st.error(f"❌ Sai · Bạn chọn: {a}")
                    st.info(f"Đáp án đúng: {q['a']}")
                    wrong_bank[q['q']] = {'answer': q['a'], 'explain': q['e'], 'fixed': 0, 'topic': q['topic']}
                st.caption(q['e'])
                with st.expander('🧠 Gợi ý nhớ nhanh cho câu này'):
                    st.write('Chủ đề: ' + TOPIC_LABELS.get(q['topic'], q['topic']))
                    st.write('Hãy nói lại bằng 1 câu: tình huống này mình cần làm gì đầu tiên?')
        score = round(correct / len(quiz) * 100)
        driving.setdefault('quiz_history', []).append({'time': datetime.now().isoformat(timespec='seconds'), 'score': score, 'correct': correct, 'total': len(quiz), 'set': selected_set, 'license': selected_license, 'topic': selected_topic})
        save_cb(profile)
        st.metric("Điểm tổng", f"{score}%", f"{correct}/{len(quiz)}")
        if score < 50: st.warning("Bạn nên quay lại bài học chi tiết của chủ đề vừa làm và bật chế độ ôn câu sai.")
        elif score < 80: st.info("Khá ổn. Hãy đọc kỹ phần giải thích để chuyển từ biết đáp án sang hiểu bản chất.")
        else: st.success("Rất tốt. Bạn nên thử bộ đề khác hoặc sang phần mô phỏng AI để luyện phản xạ.")

# =========================================================
# v15.6 Final Ultra Pro extensions: bigger exam bank + more animated simulations
# =========================================================
_OLD_GET_QUESTION_BANK = get_question_bank
_OLD_GET_LESSONS = get_lessons

@st.cache_data(show_spinner=False)
def get_lessons() -> List[Dict[str, Any]]:
    extra = [
        {"id":"emergency","icon":"🚨","title":"Xử lý khẩn cấp","tag":"Nâng cao","license":"Tất cả","summary":"Phanh khẩn cấp, tránh vật cản, xe chết máy, nổ lốp và giữ bình tĩnh.",
         "goal":"Biết phản xạ ưu tiên an toàn khi tình huống bất ngờ xảy ra.",
         "steps":["Giữ bình tĩnh, giữ thẳng xe nếu có thể.","Giảm tốc có kiểm soát, bật cảnh báo khi cần.","Quan sát lối thoát và tránh đánh lái gấp quá mức.","Dừng ở nơi an toàn rồi mới kiểm tra xe."],
         "mistakes":["Hoảng loạn đánh lái mạnh","Phanh gấp khi xe đang trượt","Dừng ngay giữa làn nguy hiểm"],
         "tips":["Khẩn cấp cần ổn định trước, xử lý sau","Đừng cố cứu tình huống bằng một thao tác quá mạnh"],
         "qa":[("Khi nổ lốp nên làm gì?","Giữ chặt vô lăng, giảm tốc từ từ và đưa xe vào nơi an toàn."),("Vì sao không đánh lái gấp?","Đánh lái gấp khi xe mất ổn định có thể làm tình huống nguy hiểm hơn.")]},
        {"id":"urban","icon":"🏙️","title":"Lái xe trong phố đông","tag":"Thực chiến","license":"Tất cả","summary":"Xử lý xe máy, người đi bộ, mở cửa xe và tình huống chen cắt.",
         "goal":"Lái xe mượt và an toàn trong môi trường đông, hẹp và nhiều bất ngờ.",
         "steps":["Đi chậm hơn tốc độ tối đa khi phố đông.","Giữ khoảng cách bên với xe máy và xe đạp.","Chú ý cửa xe mở bất ngờ, trẻ em, người qua đường.","Không tranh đường; ưu tiên nhường khi chưa chắc chắn."],
         "mistakes":["Chen ép xe máy","Chỉ nhìn xe phía trước","Bấm còi thay cho giảm tốc"],
         "tips":["Phố đông cần mắt quét liên tục","Không gian bên hông xe rất quan trọng"],
         "qa":[("Vì sao đi phố phải quét hai bên?","Vì xe máy/người đi bộ có thể xuất hiện sát thân xe."),("Lái phố đông nên ưu tiên gì?","Ưu tiên mượt, chậm, rõ ý và nhường khi cần.")]},
        {"id":"eco_smooth","icon":"🍃","title":"Lái mượt & tiết kiệm","tag":"Kỹ năng","license":"B/C/D","summary":"Tăng/giảm tốc êm, ít phanh gấp, dự đoán dòng xe và tiết kiệm nhiên liệu.",
         "goal":"Giúp xe êm hơn, người ngồi thoải mái hơn và giảm hao phí.",
         "steps":["Nhìn xa để nhả ga sớm thay vì phanh muộn.","Tăng tốc đều, không thốc ga liên tục.","Giữ khoảng cách để tránh phanh gấp.","Dùng tốc độ ổn định khi điều kiện cho phép."],
         "mistakes":["Ga/phanh liên tục","Bám sát nên phải phanh nhiều","Tăng tốc rồi phanh ngay"],
         "tips":["Lái mượt bắt đầu từ nhìn xa","Ít phanh gấp thường là lái tốt hơn"],
         "qa":[("Lái mượt có liên quan an toàn không?","Có, vì lái mượt thường nghĩa là bạn quan sát sớm và ít xử lý gấp."),("Tại sao giữ khoảng cách giúp tiết kiệm?","Vì bạn có thể nhả ga sớm và hạn chế phanh/ga liên tục.")]},
    ]
    return _OLD_GET_LESSONS() + extra

@st.cache_data(show_spinner=False)
def get_question_bank() -> List[Dict[str, Any]]:
    base = _OLD_GET_QUESTION_BANK()
    templates = [
        ("Bộ đề Final 1", "defensive", "🧠", "Khi cảm thấy xe phía trước có dấu hiệu phanh bất ngờ, phản ứng tốt nhất là gì?", ["Giữ khoảng cách và chuẩn bị giảm tốc", "Tăng tốc vượt ngay", "Bấm còi liên tục", "Đi sát để tránh bị chen"], "Giữ khoảng cách và chuẩn bị giảm tốc", "Phòng vệ tốt là chuẩn bị trước khi nguy hiểm xảy ra."),
        ("Bộ đề Final 1", "urban", "🏙️", "Trong phố đông, vì sao không nên ép sát xe máy?", ["Vì xe máy dễ đổi hướng bất ngờ", "Vì xe máy luôn đi chậm", "Vì đường sẽ rộng hơn", "Vì không cần nhìn gương"], "Vì xe máy dễ đổi hướng bất ngờ", "Lái trong phố cần giữ khoảng cách bên an toàn."),
        ("Bộ đề Final 1", "emergency", "🚨", "Nếu xe có dấu hiệu nổ lốp, việc đầu tiên nên làm là gì?", ["Giữ chặt vô lăng và giảm tốc từ từ", "Đánh lái thật mạnh", "Phanh gấp ngay lập tức", "Tắt máy giữa đường"], "Giữ chặt vô lăng và giảm tốc từ từ", "Ưu tiên ổn định xe trước khi đưa vào nơi an toàn."),
        ("Bộ đề Final 1", "eco_smooth", "🍃", "Muốn lái xe mượt hơn, thói quen nào hữu ích nhất?", ["Nhìn xa và nhả ga sớm", "Ga mạnh rồi phanh mạnh", "Bám sát xe trước", "Chuyển làn liên tục"], "Nhìn xa và nhả ga sớm", "Nhìn xa giúp bạn giảm xử lý gấp và lái êm hơn."),
        ("Bộ đề Final 2", "braking", "🦶", "Đường trơn ảnh hưởng thế nào đến quãng đường phanh?", ["Làm quãng đường phanh dài hơn", "Làm phanh ngắn hơn", "Không ảnh hưởng", "Chỉ ảnh hưởng màu xe"], "Làm quãng đường phanh dài hơn", "Độ bám giảm khiến xe cần nhiều khoảng cách hơn để dừng."),
        ("Bộ đề Final 2", "overtake", "🚘", "Trước khi vượt xe, yếu tố nào bắt buộc phải rõ ràng?", ["Tầm nhìn và khoảng trống phía trước", "Màu xe trước", "Âm nhạc trong xe", "Tên con đường"], "Tầm nhìn và khoảng trống phía trước", "Không đủ tầm nhìn thì chưa đủ điều kiện vượt an toàn."),
        ("Bộ đề Final 2", "hill_start", "⛰️", "Khi lên dốc, điều gì giúp tránh tụt xe?", ["Phối hợp ga/phanh/côn hoặc giữ phanh đúng cách", "Về N", "Tắt máy", "Không nhìn gương"], "Phối hợp ga/phanh/côn hoặc giữ phanh đúng cách", "Dốc yêu cầu kiểm soát lực kéo và giữ xe ổn định."),
        ("Bộ đề Final 2", "highway", "🛣️", "Trên cao tốc, hành vi nào giúp an toàn nhất?", ["Giữ làn và giữ khoảng cách ổn định", "Chuyển làn liên tục", "Dừng tùy ý", "Bám sát để tiết kiệm đường"], "Giữ làn và giữ khoảng cách ổn định", "Tốc độ cao cần sự ổn định và khoảng cách nhiều hơn."),
    ]
    extra = []
    licenses = ["Tất cả", "B", "C1/C", "D/E/FC"]
    for i in range(1, 7):
        for set_name, topic, icon, q, choices, ans, exp in templates:
            nq = {
                "set": f"{set_name} - Vòng {i}",
                "license": licenses[i % len(licenses)] if topic not in ["urban","emergency","defensive"] else "Tất cả",
                "topic": topic,
                "icon": icon,
                "q": q if i == 1 else f"{q} (biến thể {i})",
                "choices": choices,
                "a": ans,
                "e": exp + f" Đây là biến thể ôn tập số {i} để tăng độ phủ ngân hàng đề.",
            }
            extra.append(nq)
    return base + extra

# Bổ sung label và SVG fallback cho topic mới
TOPIC_LABELS.update({
    "emergency": "🚨 Xử lý khẩn cấp",
    "urban": "🏙️ Lái xe trong phố đông",
    "eco_smooth": "🍃 Lái mượt & tiết kiệm",
})
