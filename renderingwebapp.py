import io
import time
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter

# Page setup
st.set_page_config(page_title="Pro Image Renderer", page_icon="🚀", layout="wide")

st.title("🚀 منصة الرندرة الاحترافية للصور (Pro Image Renderer)")
st.markdown("ارفع صورتك واضبط إعدادات الإضاءة والتفاصيل للحصول على رندرة عالية الجودة.")

# Sidebar controls for rendering parameters
st.sidebar.header("⚙️ إعدادات الرندرة (Render Settings)")
brightness = st.sidebar.slider("الإضاءة (Brightness)", 0.5, 2.5, 1.15, 0.05)
contrast = st.sidebar.slider("التباين (Contrast)", 0.5, 2.5, 1.15, 0.05)
sharpness = st.sidebar.slider("حدة التفاصيل (Sharpness)", 0.0, 3.0, 1.3, 0.1)
color = st.sidebar.slider("تشبع الألوان (Color Vibrance)", 0.0, 2.5, 1.1, 0.05)
apply_detail = st.sidebar.checkbox("تفعيل تحسين التفاصيل الدقيقة (Detail Pass)", value=True)

# File uploader
uploaded_file = st.file_uploader("اختر صورة للرندرة (PNG, JPG, WEBP)", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    original_image = Image.open(uploaded_file).convert("RGB")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("الصورة الأصلية (Original)")
        st.image(original_image, use_container_width=True)

    # Render button
    if st.button("✨ ابدأ الرندرة الآن (Start Render)", type="primary"):
        with st.spinner("جاري معالجة الإضاءة والظلال والتفاصيل..."):
            time.sleep(1)  # Simulating heavy render pass
            
            # 1. Color & Lighting passes
            rendered = ImageEnhance.Brightness(original_image).enhance(brightness)
            rendered = ImageEnhance.Contrast(rendered).enhance(contrast)
            rendered = ImageEnhance.Color(rendered).enhance(color)
            rendered = ImageEnhance.Sharpness(rendered).enhance(sharpness)
            
            # 2. Detail pass
            if apply_detail:
                rendered = rendered.filter(ImageFilter.DETAIL)

            # Save high-quality output to memory buffer
            buf = io.BytesIO()
            rendered.save(buf, format="PNG", optimize=True)
            byte_im = buf.getvalue()

        with col2:
            st.subheader("النتيجة النهائية (Rendered)")
            st.image(rendered, use_container_width=True)
            
            st.download_button(
                label="📥 تحميل الصورة المرندرة بأعلى جودة (Download PNG)",
                data=byte_im,
                file_name=f"rendered_{uploaded_file.name.rsplit('.', 1)[0]}.png",
                mime="image/png"
            )
else:
    st.info("يرجى رفع صورة من الأعلى للبدء في عملية الرندرة.")
