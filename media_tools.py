import os
import tempfile
import time

import streamlit as st

from . import config


def render_veo() -> None:
    st.title("🎬 Google Veo")
    st.caption("Tạo video từ ảnh. Nhập API key ở Streamlit Secrets hoặc nhập tạm bên dưới.")
    try:
        from google import genai
        from google.genai import types
    except Exception:
        st.error("Chưa cài google-genai."); return
    api_key = st.text_input("Google API Key", value=config.GOOGLE_API_KEY, type="password")
    img = st.file_uploader("Ảnh JPG/PNG", type=["jpg","jpeg","png"])
    prompt = st.text_area("Prompt", value="Animate this image naturally, cinematic movement, smooth camera motion.")
    if img: st.image(img, use_container_width=True)
    if st.button("Tạo video"):
        if not api_key or not img: st.warning("Cần API key và ảnh."); return
        client=genai.Client(api_key=api_key); tmp_path=None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(img.getvalue()); tmp_path=tmp.name
            with st.spinner("Đang tạo video..."):
                uploaded=client.files.upload(file=tmp_path)
                op=client.models.generate_videos(model="veo-2.0-generate-001", prompt=prompt, image=uploaded, config=types.GenerateVideosConfig(aspect_ratio="16:9"))
                while not op.done:
                    time.sleep(5); op=client.operations.get(operation=op.name)
            vids=[]
            if getattr(op, "result", None): vids = getattr(op.result, "videos", []) or []
            if vids:
                v=vids[0]
                if hasattr(v, "video_bytes") and v.video_bytes: st.video(v.video_bytes); st.download_button("Tải MP4", v.video_bytes, "veo_video.mp4", "video/mp4")
                elif hasattr(v, "uri"): st.video(v.uri); st.link_button("Mở video", v.uri)
            else: st.error("Không thấy video trong response.")
        except Exception as exc: st.error(str(exc))
        finally:
            if tmp_path and os.path.exists(tmp_path): os.remove(tmp_path)


def render_tiktok() -> None:
    st.title("📥 TikTok Downloader")
    st.caption("Chỉ dùng để tải video bạn sở hữu hoặc được phép tải. Không dùng để vi phạm bản quyền/quyền riêng tư/điều khoản nền tảng.")
    url=st.text_input("Dán link TikTok")
    if st.button("Lấy và tải video"):
        if not url: st.warning("Chưa có link."); return
        try:
            import yt_dlp
        except Exception:
            st.error("Chưa cài yt-dlp."); return
        ydl_opts={"format":"mp4/best","outtmpl": tempfile.gettempdir()+"/%(id)s.%(ext)s", "quiet": True, "noplaylist": True}
        with st.spinner("Đang xử lý link..."):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info=ydl.extract_info(url, download=True)
                    path=ydl.prepare_filename(info)
                st.success(info.get("title", "Đã tải video"))
                st.write({"title":info.get("title"), "uploader":info.get("uploader"), "duration":info.get("duration")})
                data=open(path,"rb").read()
                if len(data)<80_000_000: st.video(data)
                st.download_button("⬇️ Tải video", data, os.path.basename(path), "video/mp4")
            except Exception as exc:
                st.error(f"Không tải được: {exc}")
