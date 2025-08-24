import streamlit as st

st.set_page_config(page_title="Course Cards UI", layout="wide")

st.markdown('<h1 class="centered-title">One Nation One Document - ONOD</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="centered-title">User Dashboard</h3>', unsafe_allow_html=True)

# Example Courses Data
courses = [
    {"category": "Identity", "title": "Digital ID & Records", "color": "#1f77b4"},  # Blue
    {"category": "Education", "title": "School & College Enrollment", "color": "#ff7f0e"},  # Orange
    {"category": "Finance", "title": "Banking & Loans", "color": "#2ca02c"},  # Green
    {"category": "Employment", "title": "Job history and contracts", "color": "#d62728"},  # Red
    {"category": "Healthcare", "title": "Medical Records & Appointments", "color": "#9467bd"},  # Purple
    {"category": "Housing and Property", "title": "Property & Rent Records", "color": "#8c564b"},  # Brown
    {"category": "Utility and Telecom", "title": "Electricity, Water, Internet", "color": "#e377c2"},  # Pink
    {"category": "Legal and Judicial", "title": "Court & Legal Services", "color": "#7f7f7f"}  # Gray
]

# CSS Styling
st.markdown("""
    <style>
        .course-card {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 30px;
            margin-bottom: 20px;
            height: 180px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .course-card:hover {
            background-color: #f0f8ff;
            transform: translateY(-5px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.2);
        }
        .stApp {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .centered-title {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Display cards in rows of 4 with colored text
cards_per_row = 4
for i in range(0, len(courses), cards_per_row):
    cols = st.columns(cards_per_row)
    for idx, course in enumerate(courses[i:i+cards_per_row]):
        with cols[idx]:
            st.markdown(f"""
                <div class="course-card">
                    <div style="font-weight:bold; font-size:18px; color:{course['color']};">{course['category']}</div>
                    <div style="font-size:14px; color:{course['color']};">{course.get('title','')}</div>
                </div>
            """, unsafe_allow_html=True)
