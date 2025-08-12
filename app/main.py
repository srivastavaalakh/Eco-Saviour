import streamlit as st
from PIL import Image
import os
import sys
from io import BytesIO
import base64
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.gemini_agents.receipt_parser import parse_receipt_image
from agents.gemini_agents.image_classifier import classify_waste_image
from agents.gemini_agents.sustainability_advisor import suggest_sustainable_alternatives

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

# Streamlit Page Config 
st.set_page_config(page_title="EcoSaviour", layout="wide")

# Dark Mode Toggle 
dark_mode = st.sidebar.checkbox("🌙 Enable Dark Mode")

if dark_mode:
    primary_color = "#1B5E20"
    bg_color = "#212121"
    text_color = "#FAF9F6"
    card_bg = "#333333"
    button_color = "#388E3C"
    hover_color = "#66BB6A"
else:
    primary_color = "#2E7D32"
    bg_color = "#EFE6DD"
    text_color = "#424242"
    card_bg = "#FAF9F6"
    button_color = "#2E7D32"
    hover_color = "#006400"

# Custom Themed CSS 
st.markdown(f"""
    <style>
    body, .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {{
        color: {primary_color};
    }}
    .stButton > button {{
        background-color: {button_color};
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }}
    .stButton > button:hover {{
        background-color: {hover_color};
        color: white;
    }}
    .stDownloadButton > button {{
        background-color: #FBC02D;
        color: #212121;
        font-weight: 600;
        border-radius: 6px;
    }}
    .stDownloadButton > button:hover {{
        background-color: #FFD54F;
        color: #212121;
    }}
    .stCheckbox > label {{
        color: {primary_color};
        font-weight: 500;
    }}
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-thumb {{
        background: #A3B18A;
        border-radius: 10px;
    }}
    .stMarkdown, .stDataFrame, .stImage {{
        border-radius: 10px;
        background-color: {card_bg};
        padding: 1rem;
    }}
    </style>
""", unsafe_allow_html=True)

# Helper: Compact image preview 
def render_image_thumbnail(image: Image.Image, max_height=350):
    buf = BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"""
    <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
        <img src="data:image/png;base64,{b64}" style="max-height: {max_height}px; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.2);" />
    </div>
    """

# Helper: Generate PDF 
def generate_pdf(recommendations):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm)
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle('Header', parent=styles['Title'], textColor=colors.HexColor("#2E7D32"))
    subheader_style = ParagraphStyle('Subheader', parent=styles['Heading2'], textColor=colors.HexColor("#C49A48"))
    body_style = ParagraphStyle('Body', fontSize=10, leading=14, textColor=colors.HexColor("#333333"))

    elements = []
    elements.append(Paragraph("EcoSaviourAI", header_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "Your waste analysis and sustainable alternatives below promote better consumption choices.",
        subheader_style
    ))
    elements.append(Spacer(1, 18))

    table_data = [["SNo", "Original Item", "Alternative", "Reason", "Impact Score"]]
    for idx, rec in enumerate(recommendations, start=1):
        table_data.append([
            str(idx),
            Paragraph(rec.get("original", "N/A"), body_style),
            Paragraph(rec.get("alternative", "N/A"), body_style),
            Paragraph(rec.get("reason", "N/A"), body_style),
            str(rec.get("impact_score", "N/A"))
        ])

    table = Table(table_data, colWidths=[2*cm, 3.5*cm, 4*cm, 6.5*cm, 2*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F1F8E9"), colors.white])
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("♻️ Thank you for making sustainable choices.", body_style))
    doc.build(elements)
    return temp_file.name

# App UI
st.title("🌱 EcoSaviour — AI for Responsible Consumption")
st.markdown("Upload a **receipt** or **trash image** to analyze your consumption and get **eco-friendly alternatives** using **Gemini AI**.")

uploaded_file = st.file_uploader("📎 Upload an image (Receipt or Trash)", type=["jpg", "jpeg", "png"])
image_type = st.selectbox("🔍 What type of image is this?", ["Receipt", "Trash/Waste"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.markdown(render_image_thumbnail(image), unsafe_allow_html=True)

    if st.checkbox("🔎 View full-size image"):
        buf = BytesIO()
        image.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        st.markdown(f"""
        <div style="overflow-x: auto; text-align: center; margin-bottom: 2rem;">
            <img src="data:image/png;base64,{b64}" style="max-width: 90%; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.3);" />
        </div>
        """, unsafe_allow_html=True)

    extracted_items = []

    if st.button("♻ Analyze & Suggest Alternatives"):
        with st.spinner("🔍 Processing image with Gemini..."):

            if image_type == "Receipt":
                result = parse_receipt_image(image)
                items = result.get("items", [])
                extracted_items = [item.get("name") for item in items]

                st.subheader("🧾 Parsed Receipt Items")
                for item in items:
                    st.markdown(f"- **{item.get('name', 'Unknown')}** ({item.get('category', 'n/a')} — {item.get('packaging', 'n/a')})")

            elif image_type == "Trash/Waste":
                result = classify_waste_image(image)
                items = result.get("items", [])
                extracted_items = [item.get("name") for item in items]

                st.subheader("🗑️ Detected Trash Items")
                for item in items:
                    st.markdown(f"- **{item.get('name', 'Unknown')}** ({item.get('material', 'n/a')} — Recyclable: {item.get('recyclable', 'n/a')})")

        if extracted_items:
            with st.spinner("💡 Generating sustainable alternatives..."):
                suggestions = suggest_sustainable_alternatives(extracted_items)

            st.subheader("✅ Suggested Eco-Friendly Alternatives")

            if "recommendations" in suggestions:
                for rec in suggestions["recommendations"]:
                    st.markdown(f"""
                    <div style="padding: 1rem; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 1rem;">
                        <b>🧾 Original Item:</b> {rec.get("original", "N/A")}<br>
                        <b>🌱 Alternative:</b> {rec.get("alternative", "N/A")}<br>
                        <b>💡 Reason:</b> {rec.get("reason", "N/A")}<br>
                        <b>📊 Impact Score:</b> {rec.get("impact_score", "N/A")} / 5
                    </div>
                    """, unsafe_allow_html=True)

                pdf_path = generate_pdf(suggestions["recommendations"])
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=f,
                        file_name="ecosaviour_report.pdf",
                        mime="application/pdf"
                    )
            else:
                st.warning("❌ No structured recommendations found. Try a simpler input.")
        else:
            st.warning("⚠️ No usable items found in the image.")
