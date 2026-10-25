import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# Optional ReportLab import for PDF generation
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="AI Travel Itinerary Architect",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0px; }
    .sub-header { font-size: 1.2rem; color: #4B5563; margin-bottom: 20px; }
    .card { background-color: #F3F4F6; padding: 20px; border-radius: 10px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("## 🧭 Trip Parameters")
destination = st.sidebar.text_input("🌍 Destination City/Country", "Kyoto, Japan")
num_days = st.sidebar.slider("📅 Days of Stay", min_value=1, max_value=14, value=5)
budget_level = st.sidebar.selectbox("💰 Budget Level", ["Backpacker (Budget)", "Mid-Range (Comfort)", "Luxury (High-End)"])
travel_interests = st.sidebar.multiselect(
    "🎯 Travel Interests",
    ["Local Food & Nightlife", "History & Architecture", "Nature & Adventure", "Shopping & Markets", "Art & Museums", "Relaxation & Spa"],
    default=["Local Food & Nightlife", "History & Architecture"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 AI Engine Settings")
use_ai_api = st.sidebar.checkbox("Use Custom LLM API Key (OpenAI)", value=False)
api_key = ""
if use_ai_api:
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

generate_btn = st.sidebar.button("🚀 Generate Itinerary", type="primary")

# Main Title Area
st.markdown('<p class="main-header">✈️ AI Travel Itinerary Architect</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your intelligent assistant for personalized travel planning, local cuisine, and cultural guides.</p>', unsafe_allow_html=True)

def generate_mock_itinerary(dest, days, budget, interests):
    """Generates structured day-by-day plans, food, and etiquette based on inputs."""
    itinerary = []
    start_date = datetime.now() + timedelta(days=10)
    
    # Budget multiplier
    mult = 1.0 if "Backpacker" in budget else (2.5 if "Mid-Range" in budget else 6.0)
    
    for i in range(1, days + 1):
        day_date = (start_date + timedelta(days=i-1)).strftime("%B %d, %Y")
        itinerary.append({
            "Day": i,
            "Date": day_date,
            "Morning": f"Explore iconic historical landmarks in {dest}. Walking tour of old town highlights.",
            "Afternoon": f"Immersive experience focusing on {', '.join(interests[:2])}. Visit top-rated galleries or scenic viewpoints.",
            "Evening": f"Dinner at a recommended local hotspot featuring regional specialties. Evening stroll.",
            "Est. Daily Cost (INR)": f"₹{int(3000 * mult):,}",
            "Est. Daily Cost (USD)": f"${int(35 * mult):,}"
        })
        
    food_recs = [
        {"Dish": "Signature Street Bite", "Vibe": "Local night market stall", "Why Try": "Unfiltered authentic flavors loved by locals for generations."},
        {"Dish": "Traditional Heritage Meal", "Vibe": "Family-run hidden tavern", "Why Try": "Prepared using secret family recipes passed down decades."},
        {"Dish": "Artisanal Cafe Special", "Vibe": "Quiet alleyway hideout", "Why Try": "Great ambiance with locally sourced ingredients and specialty coffee."}
    ]
    
    etiquette = {
        "Dos": [
            "Learn at least 5 basic phrases in the local language (Hello, Thank you, Please).",
            "Respect local dress codes when entering temples, shrines, or religious sites.",
            "Always ask permission before taking close-up photos of local residents."
        ],
        "Donts": [
            "Don't tip excessively if tipping is not part of the local service culture.",
            "Avoid speaking loudly on public transit or in quiet cultural spaces.",
            "Don't touch sacred artifacts or displays unless explicitly permitted."
        ],
        "Emergency": {
            "Police / General Emergency": "112 / Local equivalent",
            "Tourist Helpline": "Available via local embassy portal",
            "Key Phrase": "'Where is the nearest hospital?' / 'Help me please'"
        }
    }
    
    packing = [
        "Comfortable walking shoes (essential for daily exploration)",
        "Weather-appropriate layered clothing",
        "Universal power adapter & portable power bank",
        "Reusable water bottle & basic first-aid kit"
    ]
    
    return itinerary, food_recs, etiquette, packing

if generate_btn or 'itinerary_data' in st.session_state:
    if generate_btn:
        itinerary_data, food_data, etiquette_data, packing_data = generate_mock_itinerary(destination, num_days, budget_level, travel_interests)
        st.session_state['itinerary_data'] = itinerary_data
        st.session_state['food_data'] = food_data
        st.session_state['etiquette_data'] = etiquette_data
        st.session_state['packing_data'] = packing_data
        st.session_state['destination'] = destination
        st.session_state['budget_level'] = budget_level

    itinerary_data = st.session_state['itinerary_data']
    food_data = st.session_state['food_data']
    etiquette_data = st.session_state['etiquette_data']
    packing_data = st.session_state['packing_data']

    # Tabs for Organization
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗓️ Day-by-Day Itinerary", 
        "🍜 Local Food & Hidden Gems", 
        "📜 Cultural Etiquette", 
        "🎒 Smart Packing List", 
        "📥 Export & Share"
    ])

    with tab1:
        st.subheader(f"Your Custom Itinerary for {destination}")
        df = pd.DataFrame(itinerary_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("### 📊 Budget Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Estimated Total Budget (INR)", f"₹{num_days * 4500:,}")
        with col2:
            st.metric("Estimated Total Budget (USD)", f"${num_days * 55:,}")

    with tab2:
        st.subheader("🍜 Hidden Local Food Recommendations")
        for item in food_data:
            st.markdown(f"""
            <div class="card">
                <h4>🍽️ {item['Dish']}</h4>
                <p><b>Recommended Vibe:</b> {item['Vibe']}</p>
                <p><b>Why Try:</b> {item['Why Try']}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.subheader("📜 Cultural Etiquette & Do's / Don'ts Handbook")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ✅ Do's")
            for d in etiquette_data["Dos"]:
                st.markdown(f"- {d}")
        with col2:
            st.markdown("### ❌ Don'ts")
            for d in etiquette_data["Donts"]:
                st.markdown(f"- {d}")
                
        st.markdown("---")
        st.markdown("### 🚨 Emergency & Useful Phrases")
        for k, v in etiquette_data["Emergency"].items():
            st.markdown(f"- **{k}:** `{v}`")

    with tab4:
        st.subheader("🎒 Smart Packing Checklist")
        for item in packing_data:
            st.checkbox(item, value=False, key=f"pack_{item}")

    with tab5:
        st.subheader("📥 Export Your Itinerary")
        st.markdown("Download your complete travel plan to take it offline.")
        
        if REPORTLAB_AVAILABLE:
            def create_pdf():
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []
                
                title_style = ParagraphStyle(
                    'TitleStyle',
                    parent=styles['Heading1'],
                    fontSize=20,
                    textColor=colors.HexColor('#1E3A8A'),
                    spaceAfter=15
                )
                
                story.append(Paragraph(f"Travel Itinerary: {destination}", title_style))
                story.append(Paragraph(f"Generated for {num_days} Days | Budget: {budget_level}", styles['Normal']))
                story.append(Spacer(1, 15))
                
                for day in itinerary_data:
                    story.append(Paragraph(f"<b>Day {day['Day']} ({day['Date']})</b>", styles['Heading2']))
                    story.append(Paragraph(f"<b>Morning:</b> {day['Morning']}", styles['Normal']))
                    story.append(Paragraph(f"<b>Afternoon:</b> {day['Afternoon']}", styles['Normal']))
                    story.append(Paragraph(f"<b>Evening:</b> {day['Evening']}", styles['Normal']))
                    story.append(Spacer(1, 10))
                
                doc.build(story)
                buffer.seek(0)
                return buffer

            pdf_buffer = create_pdf()
            st.download_button(
                label="📄 Download Itinerary PDF",
                data=pdf_buffer,
                file_name=f"{destination.replace(', ', '_')}_Itinerary.pdf",
                mime="application/pdf",
                type="primary"
            )
        else:
            st.warning("ReportLab library not installed. Showing markdown download option instead.")
            txt_output = f"Travel Itinerary for {destination}\n\n"
            for day in itinerary_data:
                txt_output += f"Day {day['Day']} - {day['Date']}\nMorning: {day['Morning']}\nAfternoon: {day['Afternoon']}\nEvening: {day['Evening']}\n\n"
            st.download_button(
                label="📥 Download Itinerary (TXT)",
                data=txt_output,
                file_name=f"{destination}_Itinerary.txt",
                mime="text/plain"
            )
else:
    st.info("👈 Fill out your trip details in the sidebar and click **'Generate Itinerary'** to begin!")