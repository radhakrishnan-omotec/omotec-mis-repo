import streamlit as st
import pandas as pd
import os
import base64
import datetime

# ----------------- Constants -----------------
DAILY_TASK_CSV = 'content_team_daily_tasks.csv'
TRAINING_CSV = 'content_team_training_tracker.csv'
AUDIT_CSV = 'content_team_audit_logs.csv'
MIS_CSV = 'content_team_mis_kpis.csv'

USERNAME = "omotec"
PASSWORD = "omotec"

DAILY_TASK_COLUMNS = ["S.No", "Date", "Team Member", "Task Description", "Time Spent (Hrs)", "Status"]
TRAINING_COLUMNS = ["S.No", "Date", "Team Member", "Training Name", "Duration (Hrs)", "Feedback"]
AUDIT_COLUMNS = ["S.No", "Date", "Team Member", "Document/Task", "Error Type", "Correction Action", "Remarks"]
MIS_COLUMNS = [
    "S.No", "Month", "Curriculum Modules Built", "Modules Revised", "Quality Checks Done",
    "Average QC Score (%)", "Turnaround Time (Days)", "Content Feedback Items",
    "Content Updated Based on Feedback", "Pending Requests", "Notes/Challenges"
]

# ----------------- Helper Functions -----------------
def create_csv(file, columns):
    if not os.path.exists(file):
        pd.DataFrame(columns=columns).to_csv(file, index=False)

def insert_data(file, data):
    df = fetch_data(file, list(data.keys()))
    data["S.No"] = len(df) + 1
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(file, index=False)

def fetch_data(file, columns):
    return pd.read_csv(file) if os.path.isfile(file) else pd.DataFrame(columns=columns)

def download_csv(df, filename):
    if not df.empty:
        csv = df.to_csv(index=False).encode()
        st.download_button("📥 Download CSV", csv, filename, "text/csv")

def set_background_image(image_file_path):
    if os.path.exists(image_file_path):
        with open(image_file_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# ----------------- Login -----------------
def login_screen():
    set_background_image("back.jpg")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 0;'>CONTENT MIS PROJECT</h2>", unsafe_allow_html=True)
    with col2:
        if os.path.exists("NEW LOGO - OMOTEC.png"):
            st.image("NEW LOGO - OMOTEC.png", use_column_width=True)

    st.markdown("📚 STUDENT ASSESSMENT LOGIN")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
        else:
            st.error("❌ Invalid credentials")

# ----------------- Pages -----------------
def Daily_Task_Logger_Page():
    st.header("📅 Daily Task Logger")
    create_csv(DAILY_TASK_CSV, DAILY_TASK_COLUMNS)

    with st.form("form_daily"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date")
            member = st.text_input("Team Member")
        with col2:
            hours = st.number_input("Time Spent (Hrs)", min_value=0.0, step=0.5)
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
        task = st.text_area("Task Description")

        if st.form_submit_button("Submit"):
            if member and task:
                insert_data(DAILY_TASK_CSV, {
                    "Date": date, "Team Member": member, "Task Description": task,
                    "Time Spent (Hrs)": hours, "Status": status
                })
                st.success("✅ Task logged!")
            else:
                st.error("Please fill all required fields.")

    df = fetch_data(DAILY_TASK_CSV, DAILY_TASK_COLUMNS)
    st.markdown("### 🗂️ Records")
    st.dataframe(df, use_container_width=True)
    download_csv(df, "daily_tasks.csv")

def Training_Tracker_Page():
    st.header("📚 Training Tracker")
    create_csv(TRAINING_CSV, TRAINING_COLUMNS)

    with st.form("form_training"):
        date = st.date_input("Date")
        member = st.text_input("Team Member")
        training = st.text_input("Training Name")
        duration = st.number_input("Duration (Hrs)", min_value=0.0, step=0.5)
        feedback = st.text_area("Feedback")

        if st.form_submit_button("Submit"):
            if member and training:
                insert_data(TRAINING_CSV, {
                    "Date": date, "Team Member": member, "Training Name": training,
                    "Duration (Hrs)": duration, "Feedback": feedback
                })
                st.success("✅ Training record saved!")
            else:
                st.error("Please fill all required fields.")

    df = fetch_data(TRAINING_CSV, TRAINING_COLUMNS)
    st.markdown("### 📈 Records")
    st.dataframe(df, use_container_width=True)
    download_csv(df, "training_tracker.csv")

def Audit_Error_Logs_Page():
    st.header("📋 Audit & Error Logs")
    create_csv(AUDIT_CSV, AUDIT_COLUMNS)

    with st.form("form_audit"):
        date = st.date_input("Date")
        member = st.text_input("Team Member")
        document = st.text_input("Document/Task")
        error_type = st.selectbox("Error Type", ["Formatting", "Grammar", "Content", "Incorrect Data", "Other"])
        correction = st.text_area("Correction Action Taken")
        remarks = st.text_area("Remarks")

        if st.form_submit_button("Submit"):
            if member and document:
                insert_data(AUDIT_CSV, {
                    "Date": date, "Team Member": member, "Document/Task": document,
                    "Error Type": error_type, "Correction Action": correction, "Remarks": remarks
                })
                st.success("✅ Audit log saved!")
            else:
                st.error("Please fill all required fields.")

    df = fetch_data(AUDIT_CSV, AUDIT_COLUMNS)
    st.markdown("### 🔍 Audit Records")
    st.dataframe(df, use_container_width=True)
    download_csv(df, "audit_logs.csv")



def Content_Audit_Tracker_Page():
    tabs = st.tabs(["📌 Primary Audit Tracker", "📆 Audit Calendar", "📝 Feedback Summary"])

    # ---------- Section i: Primary Content Audit Tracker ----------
    with tabs[0]:
        st.subheader("📌 Primary Content Audit Tracker")
        csv_path = 'primary_content_audit.csv'
        columns = [
            "S.No", "Course Name", "Category", "Last Updated", "Status", "Usage Analytics",
            "QC Score (/5)", "Audit Due Date", "Action Required", "Remarks",
            "Assigned To", "Reviewed By", "Final Decision"
        ]
        status_options = ["Outdated", "Active", "Archived"]
        analytics_options = ["Low", "Medium", "Very Low"]
        action_options = ["Revise", "Keep Active", "Archive"]
        remark_options = ["Tools outdated", "Aligns with curriculum", "Replaced by new module"]

        create_csv(csv_path, columns)

        with st.form("primary_audit_form"):
            c1, c2, c3 = st.columns(3)
            course = c1.text_input("Course Name")
            category = c2.text_input("Category")
            last_updated = c3.date_input("Last Updated", datetime.date.today())
            status = c1.selectbox("Status", status_options)
            usage = c2.selectbox("Usage Analytics", analytics_options)
            qc_score = c3.slider("QC Score (/5)", 1, 5, 3)
            due_date = c1.date_input("Audit Due Date", datetime.date.today())
            action = c2.selectbox("Action Required", action_options)
            remarks = c3.selectbox("Remarks", remark_options)
            assigned = c1.text_input("Assigned To")
            reviewed = c2.text_input("Reviewed By")
            final_decision = c3.date_input("Final Decision", datetime.date.today())

            if st.form_submit_button("Submit Audit Entry"):
                insert_data(csv_path, {
                    "Course Name": course, "Category": category, "Last Updated": last_updated,
                    "Status": status, "Usage Analytics": usage, "QC Score (/5)": qc_score,
                    "Audit Due Date": due_date, "Action Required": action, "Remarks": remarks,
                    "Assigned To": assigned, "Reviewed By": reviewed, "Final Decision": final_decision
                })
                st.success("✅ Audit Entry Added Successfully")

        df = fetch_data(csv_path, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "primary_audit_tracker.csv")

    # ---------- Section ii: Audit Calendar ----------
    with tabs[1]:
        st.subheader("📆 Monthly Audit Calendar")
        csv_path = 'audit_calendar.csv'
        columns = ["S.No", "Month", "Courses for Audit", "Auditor", "Deadline", "Review Meeting Date", "Comments"]

        create_csv(csv_path, columns)

        with st.form("audit_calendar_form"):
            m1, m2, m3 = st.columns(3)
            month = m1.date_input("Month (select any date in that month)", datetime.date.today())
            course_list = m2.text_input("Courses for Audit")
            auditor = m3.text_input("Auditor")
            deadline = m1.date_input("Audit Deadline", datetime.date.today())
            review_meet = m2.date_input("Review Meeting Date", datetime.date.today())
            comments = st.text_area("Comments")

            if st.form_submit_button("Submit Calendar Entry"):
                insert_data(csv_path, {
                    "Month": month.strftime("%B %Y"), "Courses for Audit": course_list,
                    "Auditor": auditor, "Deadline": deadline, "Review Meeting Date": review_meet,
                    "Comments": comments
                })
                st.success("✅ Calendar Entry Added Successfully")

        df = fetch_data(csv_path, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "audit_calendar.csv")

    # ---------- Section iii: Feedback Summary ----------
    with tabs[2]:
        st.subheader("📝 Feedback Summary Page")
        csv_path = 'feedback_summary.csv'
        columns = ["S.No", "Course Name", "Source", "Rating", "Issue Reported", "Suggestions", "Date Received"]
        source_options = ["Trainer", "Student"]

        create_csv(csv_path, columns)

        with st.form("feedback_form"):
            f1, f2, f3 = st.columns(3)
            course = f1.text_input("Course Name")
            source = f2.selectbox("Feedback Source", source_options)
            rating = f3.slider("Rating", 1, 5, 3)
            issue = f1.text_input("Issue Reported")
            suggestions = f2.text_area("Suggestions")
            date_recv = f3.date_input("Date Received", datetime.date.today())

            if st.form_submit_button("Submit Feedback"):
                insert_data(csv_path, {
                    "Course Name": course, "Source": source, "Rating": rating,
                    "Issue Reported": issue, "Suggestions": suggestions, "Date Received": date_recv
                })
                st.success("✅ Feedback Submitted Successfully")

        df = fetch_data(csv_path, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "feedback_summary.csv")


def Content_QC_Page():
    st.sidebar.title("📂 Navigation")
    st.header("📑 Content QC Page")
    tabs = st.tabs(["🧪 Main Content QC", "📚 Textbook QC", "📄 Worksheet QC"])
    st.sidebar.markdown("---")
    st.sidebar.markdown("Navigate to other pages from the sidebar")

    # ---------- i) MAIN CONTENT QC PAGE ----------
    with tabs[0]:
        st.subheader("🧪 Main Content QC")
        file = "main_content_qc.csv"
        columns = [
            "S.No", "COURSE NAME", "CONTENT SUBMITTED ON", "LEARNING OUTCOMES - BT", "FLOW OF CONTENT",
            "GIF", "IMAGES", "LANGUAGE - PRIMARY / SECONDARY", "FONT FAMILY /FONT SIZE",
            "CURRICULUM STANDARD ALLIGNMENT", "TEACHERS NOTES / SUPPORT MATERIAL", "INTERACTIVITY LEVEL (MCQ)",
            "VERSION / UPDATE DATE", "QC 1 FEEDBACK DATE", "QC 1 CONTENT RECEIVED ON",
            "QC 2 FEEDBACK DATE", "QC 2 CONTENT RECEIVED ON", "REMARKS"
        ]
        create_csv(file, columns)

        with st.form("form_main_qc"):
            col1, col2, col3 = st.columns(3)
            course = col1.text_input("COURSE NAME")
            submitted = col2.text_input("CONTENT SUBMITTED ON")
            outcome = col3.text_input("LEARNING OUTCOMES - BT")
            flow = col1.text_input("FLOW OF CONTENT")
            gif = col2.text_input("GIF")
            images = col3.text_input("IMAGES")
            lang = col1.text_input("LANGUAGE - PRIMARY / SECONDARY")
            font = col2.text_input("FONT FAMILY /FONT SIZE")
            curriculum = col3.text_input("CURRICULUM STANDARD ALLIGNMENT")
            notes = col1.text_input("TEACHERS NOTES / SUPPORT MATERIAL")
            interactivity = col2.text_input("INTERACTIVITY LEVEL (MCQ)")
            version = col3.text_input("VERSION / UPDATE DATE")
            qc1_date = col1.text_input("QC 1 FEEDBACK DATE")
            qc1_recv = col2.text_input("QC 1 CONTENT RECEIVED ON")
            qc2_date = col3.text_input("QC 2 FEEDBACK DATE")
            qc2_recv = col1.text_input("QC 2 CONTENT RECEIVED ON")
            remarks = st.text_area("REMARKS")

            if st.form_submit_button("Submit QC Entry"):
                insert_data(file, {
                    "COURSE NAME": course,
                    "CONTENT SUBMITTED ON": submitted,
                    "LEARNING OUTCOMES - BT": outcome,
                    "FLOW OF CONTENT": flow,
                    "GIF": gif,
                    "IMAGES": images,
                    "LANGUAGE - PRIMARY / SECONDARY": lang,
                    "FONT FAMILY /FONT SIZE": font,
                    "CURRICULUM STANDARD ALLIGNMENT": curriculum,
                    "TEACHERS NOTES / SUPPORT MATERIAL": notes,
                    "INTERACTIVITY LEVEL (MCQ)": interactivity,
                    "VERSION / UPDATE DATE": version,
                    "QC 1 FEEDBACK DATE": qc1_date,
                    "QC 1 CONTENT RECEIVED ON": qc1_recv,
                    "QC 2 FEEDBACK DATE": qc2_date,
                    "QC 2 CONTENT RECEIVED ON": qc2_recv,
                    "REMARKS": remarks
                })
                st.success("✅ Main Content QC Entry Saved!")

        df = fetch_data(file, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "main_content_qc.csv")

    # ---------- ii) TEXTBOOK QC PAGE ----------
    with tabs[1]:
        st.subheader("📚 Textbook QC")
        file = "textbook_qc.csv"
        columns = [
            "S.No", "COURSE NAME", "CONTENT SUBMITTED ON", "CURRICULUM ALIGNMENT", "CONCEPT CLARITY AND ACCURACY",
            "LANGUAGE", "STRUCTURE AND ORGANIZATION", "ILLUSTRATION AND VISUALS", "EXERCISE AND ASSESSMENT",
            "PRESENTATION AND FORMALITY", "QC 1 FEEDBACK DATE", "QC 1 CONTENT RECEIVED ON",
            "QC 2 FEEDBACK DATE", "QC 2 CONTENT RECEIVED ON", "REMARKS"
        ]
        create_csv(file, columns)

        with st.form("form_textbook_qc"):
            c1, c2, c3 = st.columns(3)
            course = c1.text_input("COURSE NAME")
            submitted = c2.date_input("CONTENT SUBMITTED ON")
            curriculum = c3.text_area("CURRICULUM ALIGNMENT")
            concept = c1.text_area("CONCEPT CLARITY AND ACCURACY")
            language = c2.text_area("LANGUAGE")
            structure = c3.text_area("STRUCTURE AND ORGANIZATION")
            visuals = c1.text_area("ILLUSTRATION AND VISUALS")
            assessment = c2.text_area("EXERCISE AND ASSESSMENT")
            presentation = c3.text_area("PRESENTATION AND FORMALITY")
            qc1_date = c1.text_input("QC 1 FEEDBACK DATE")
            qc1_recv = c2.text_input("QC 1 CONTENT RECEIVED ON")
            qc2_date = c3.text_input("QC 2 FEEDBACK DATE")
            qc2_recv = c1.text_input("QC 2 CONTENT RECEIVED ON")
            remarks = st.text_area("REMARKS")

            if st.form_submit_button("Submit Textbook QC"):
                insert_data(file, {
                    "COURSE NAME": course,
                    "CONTENT SUBMITTED ON": submitted,
                    "CURRICULUM ALIGNMENT": curriculum,
                    "CONCEPT CLARITY AND ACCURACY": concept,
                    "LANGUAGE": language,
                    "STRUCTURE AND ORGANIZATION": structure,
                    "ILLUSTRATION AND VISUALS": visuals,
                    "EXERCISE AND ASSESSMENT": assessment,
                    "PRESENTATION AND FORMALITY": presentation,
                    "QC 1 FEEDBACK DATE": qc1_date,
                    "QC 1 CONTENT RECEIVED ON": qc1_recv,
                    "QC 2 FEEDBACK DATE": qc2_date,
                    "QC 2 CONTENT RECEIVED ON": qc2_recv,
                    "REMARKS": remarks
                })
                st.success("✅ Textbook QC Entry Saved!")

        df = fetch_data(file, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "textbook_qc.csv")

    # ---------- iii) WORKSHEET QC PAGE ----------
    with tabs[2]:
        st.subheader("📄 Worksheet QC")
        file = "worksheet_qc.csv"
        columns = [
            "S.No", "COURSE NAME", "CONTENT SUBMITTED ON", "CURRICULUM ALIGNMENT", "CONCEPT ACCURACY",
            "LANGUAGE", "STRUCTURE OF OPTIONS", "DISTRACTOR QUALITY", "VARIETY & COVERAGE",
            "LANGUAGE & GRAMMAR", "FORMATTING & NUMBERING", "ANSWER KEY ACCURACY",
            "QC 1 FEEDBACK DATE", "QC 1 CONTENT RECEIVED ON",
            "QC 2 FEEDBACK DATE", "QC 2 CONTENT RECEIVED ON", "REMARKS"
        ]
        create_csv(file, columns)

        with st.form("form_worksheet_qc"):
            w1, w2, w3 = st.columns(3)
            course = w1.text_input("COURSE NAME")
            submitted = w2.date_input("CONTENT SUBMITTED ON")
            curriculum = w3.text_area("CURRICULUM ALIGNMENT")
            concept = w1.text_area("CONCEPT ACCURACY")
            language = w2.text_area("LANGUAGE")
            options = w3.text_area("STRUCTURE OF OPTIONS")
            distractors = w1.text_area("DISTRACTOR QUALITY")
            variety = w2.text_area("VARIETY & COVERAGE")
            grammar = w3.text_area("LANGUAGE & GRAMMAR")
            formatting = w1.text_area("FORMATTING & NUMBERING")
            answer_key = w2.text_area("ANSWER KEY ACCURACY")
            qc1_date = w3.text_input("QC 1 FEEDBACK DATE")
            qc1_recv = w1.text_input("QC 1 CONTENT RECEIVED ON")
            qc2_date = w2.text_input("QC 2 FEEDBACK DATE")
            qc2_recv = w3.text_input("QC 2 CONTENT RECEIVED ON")
            remarks = st.text_area("REMARKS")

            if st.form_submit_button("Submit Worksheet QC"):
                insert_data(file, {
                    "COURSE NAME": course,
                    "CONTENT SUBMITTED ON": submitted,
                    "CURRICULUM ALIGNMENT": curriculum,
                    "CONCEPT ACCURACY": concept,
                    "LANGUAGE": language,
                    "STRUCTURE OF OPTIONS": options,
                    "DISTRACTOR QUALITY": distractors,
                    "VARIETY & COVERAGE": variety,
                    "LANGUAGE & GRAMMAR": grammar,
                    "FORMATTING & NUMBERING": formatting,
                    "ANSWER KEY ACCURACY": answer_key,
                    "QC 1 FEEDBACK DATE": qc1_date,
                    "QC 1 CONTENT RECEIVED ON": qc1_recv,
                    "QC 2 FEEDBACK DATE": qc2_date,
                    "QC 2 CONTENT RECEIVED ON": qc2_recv,
                    "REMARKS": remarks
                })
                st.success("✅ Worksheet QC Entry Saved!")

        df = fetch_data(file, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "worksheet_qc.csv")


def sidebar_navigation():
    tabs = {

        "📋 Content Audit Tracker Page": Content_Audit_Tracker_Page,
        "📊 MIS & KPIs Page": Mis_KPIs_Page,
        "📑 Content QC Page": Content_QC_Page,
        "🧾 Audit & Error Logs Page": Audit_Error_Logs_Page,
        "📚 TEMPLATE Training Tracker": Training_Tracker_Page,
        "📅 TEMPLATE Daily Task Logger": Daily_Task_Logger_Page
    }
    selection = st.sidebar.radio("📘 Select Section", list(tabs.keys()))
    tabs[selection]()

def Mis_KPIs_Page():
    st.header("📊 MIS & KPIs Overview")
    tabs = st.tabs(["📁 MIS Template Page", "📌 KPIs Page", "👥 Content Team KPI Page"])

    # --- i) MIS TEMPLATE PAGE ---
    with tabs[0]:
        st.subheader("📁 MIS Template")
        mis_file = "mis_template.csv"
        mis_columns = [
            "S.No", "Month", "Curriculum Modules Built", "Modules Revised", "Quality Checks Done",
            "Average QC Score (%)", "Turnaround Time (Days)", "Content Feedback Items",
            "Content Updated Based on Feedback", "Pending Requests", "Notes/Challenges"
        ]
        create_csv(mis_file, mis_columns)

        with st.form("form_mis_template"):
            col1, col2 = st.columns(2)
            month = col1.date_input("Month")
            built = col2.text_input("Curriculum Modules Built")
            revised = col1.text_input("Modules Revised")
            qcs = col2.text_input("Quality Checks Done")
            avg_score = col1.text_input("Average QC Score (%)")
            tat = col2.text_input("Turnaround Time (Days)")
            feedback_items = col1.text_input("Content Feedback Items")
            updates = col2.text_input("Content Updated Based on Feedback")
            pending = col1.text_input("Pending Requests")
            notes = st.text_area("Notes / Challenges")

            if st.form_submit_button("Submit Entry"):
                insert_data(mis_file, {
                    "Month": month.strftime("%B %Y"),
                    "Curriculum Modules Built": built,
                    "Modules Revised": revised,
                    "Quality Checks Done": qcs,
                    "Average QC Score (%)": avg_score,
                    "Turnaround Time (Days)": tat,
                    "Content Feedback Items": feedback_items,
                    "Content Updated Based on Feedback": updates,
                    "Pending Requests": pending,
                    "Notes/Challenges": notes
                })
                st.success("✅ MIS Template Entry Saved!")

        df = fetch_data(mis_file, mis_columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "mis_template.csv")

    # --- ii) KPIs PAGE ---
    with tabs[1]:
        st.subheader("📌 KPI Tracker")
        kpi_file = "kpi_page.csv"
        kpi_columns = ["S.No", "KPI", "Target", "Owner"]

        create_csv(kpi_file, kpi_columns)

        with st.form("form_kpis"):
            kpi = st.selectbox("KPI", [
                "Number of curriculum modules built per quarter",
                "Average quality check score (%)",
                "Average turnaround time for content delivery (days)",
                "% of content updated based on relevance feedback",
                "Number of inter-departmental content collaborations",
                "Number of innovative content formats introduced"
            ])
            target = st.selectbox("Target", [
                "12 modules/quarter", ">= 90%", "<= 5 days",
                ">= 70%", "2 per month", "1 per quarter"
            ])
            owner = st.selectbox("Owner", [
                "Content Lead", "QC Team", "Content Coordinator", "Innovation Officer"
            ])

            if st.form_submit_button("Add KPI"):
                insert_data(kpi_file, {"KPI": kpi, "Target": target, "Owner": owner})
                st.success("✅ KPI Record Added")

        df = fetch_data(kpi_file, kpi_columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "kpi_page.csv")

    # --- iii) CONTENT TEAM KPI PAGE ---
    with tabs[2]:
        st.subheader("👥 Content Team KPI Overview")
        kpi_team_file = "content_team_kpis.csv"
        kpi_team_columns = ["S.No", "Content Creation", "Content Quality & Improvement", "Quality & Accuracy"]

        create_csv(kpi_team_file, kpi_team_columns)

        with st.form("form_team_kpi"):
            creation = st.selectbox("Content Creation", [
                "Total lessons, worksheets, blog posts, or videos created monthly.",
                "If content is delivered as per the academic calendar or release schedule.",
                "Ensures content aligns with STEM curriculum standards(NCERT)"
            ])
            quality = st.selectbox("Content Quality & Improvement", [
                "Based on internal or external reviews of accuracy, clarity, and engagement.",
                "Number of outdated lessons or activities that have been revised.",
                "Rating from internal teams (academics, outreach, etc.) on how helpful the content is.",
                "Content Pieces Drafted or Edited Today	(e.g., worksheets, lesson plans, blog posts, video scripts)",
                "Curriculum/Topic Mapping Done	(e.g., aligned new content with STEM standards"
            ])
            accuracy = st.selectbox("Quality & Accuracy", [
                "Proofreading and Fact-Checking Completed",
                "Peer or Expert Review Coordinated"
            ])

            if st.form_submit_button("Submit Team KPI"):
                insert_data(kpi_team_file, {
                    "Content Creation": creation,
                    "Content Quality & Improvement": quality,
                    "Quality & Accuracy": accuracy
                })
                st.success("✅ Content Team KPI Submitted")

        df = fetch_data(kpi_team_file, kpi_team_columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "content_team_kpis.csv")

# ----------------- App Config -----------------
st.set_page_config(page_title="Content Team Dashboard", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_screen()
else:
    sidebar_navigation()