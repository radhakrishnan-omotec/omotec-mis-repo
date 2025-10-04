import streamlit as st
import pandas as pd
import os
import base64
import datetime
import streamlit.components.v1 as components

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
    try:
        df = fetch_data(file, list(data.keys()))
        data["S.No"] = len(df) + 1
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(file, index=False)
    except Exception as e:
        st.session_state.error_message = str(e)

def fetch_data(file, columns):
    try:
        return pd.read_csv(file) if os.path.isfile(file) else pd.DataFrame(columns=columns)
    except Exception as e:
        st.session_state.error_message = str(e)
        return pd.DataFrame(columns=columns)

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
        .popup {{
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: white;
            padding: 20px;
            border: 2px solid #333;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            z-index: 1000;
        }}
        .popup-content {{
            text-align: center;
        }}
        .close-btn {{
            margin-top: 10px;
            padding: 5px 10px;
            background-color: #ff4444;
            color: white;
            border: none;
            cursor: pointer;
        }}
        .close-btn:hover {{
            background-color: #cc0000;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

def disable_enter_key():
    components.html("""
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                form.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
                        e.preventDefault();
                    }
                });
            });
        });
    </script>
    """, height=0)

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
    if st.button("Login", key="login_button"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
        else:
            st.session_state.error_message = "❌ Invalid credentials"

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
            try:
                if member and task:
                    insert_data(DAILY_TASK_CSV, {
                        "Date": date, "Team Member": member, "Task Description": task,
                        "Time Spent (Hrs)": hours, "Status": status
                    })
                    st.success("✅ Task logged!")
                else:
                    st.session_state.error_message = "Please fill all required fields."
            except Exception as e:
                st.session_state.error_message = str(e)

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
            try:
                if member and training:
                    insert_data(TRAINING_CSV, {
                        "Date": date, "Team Member": member, "Training Name": training,
                        "Duration (Hrs)": duration, "Feedback": feedback
                    })
                    st.success("✅ Training record saved!")
                else:
                    st.session_state.error_message = "Please fill all required fields."
            except Exception as e:
                st.session_state.error_message = str(e)

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
            try:
                if member and document:
                    insert_data(AUDIT_CSV, {
                        "Date": date, "Team Member": member, "Document/Task": document,
                        "Error Type": error_type, "Correction Action": correction, "Remarks": remarks
                    })
                    st.success("✅ Audit log saved!")
                else:
                    st.session_state.error_message = "Please fill all required fields."
            except Exception as e:
                st.session_state.error_message = str(e)

    df = fetch_data(AUDIT_CSV, AUDIT_COLUMNS)
    st.markdown("### 🔍 Audit Records")
    st.dataframe(df, use_container_width=True)
    download_csv(df, "audit_logs.csv")

def Content_Audit_Tracker_Page():
    st.subheader("📋 Content Audit Tracker Page")
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
                try:
                    if course:  # Basic validation
                        insert_data(csv_path, {
                            "Course Name": course, "Category": category, "Last Updated": last_updated,
                            "Status": status, "Usage Analytics": usage, "QC Score (/5)": qc_score,
                            "Audit Due Date": due_date, "Action Required": action, "Remarks": remarks,
                            "Assigned To": assigned, "Reviewed By": reviewed, "Final Decision": final_decision
                        })
                        st.success("✅ Audit Entry Added Successfully")
                    else:
                        st.session_state.error_message = "Please fill at least the Course Name."
                except Exception as e:
                    st.session_state.error_message = str(e)

        df = fetch_data(csv_path, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "primary_audit_tracker.csv")

        # Delete section
        st.subheader("Delete Entry")
        s_no = st.number_input("S.No to Delete", min_value=1, step=1)
        if st.button("Delete", key="delete_primary_audit"):
            try:
                df = fetch_data(csv_path, columns)
                df = df[df["S.No"] != s_no]
                df["S.No"] = range(1, len(df) + 1)
                df.to_csv(csv_path, index=False)
                st.success(f"✅ Entry {s_no} Deleted!")
            except Exception as e:
                st.session_state.error_message = str(e)

    # ---------- Section ii: Audit Calendar ----------
    with tabs[1]:
        st.subheader("📆 Monthly Audit Calendar")
        csv_path = 'audit_calendar.csv'
        columns = [
            "S.No", "Month", "Courses for Audit", "Assigned To", "Deadline",
            "Progress (%)", "Status", "Notes"
        ]
        status_options = ["Planned", "In Progress", "Completed", "Delayed"]

        create_csv(csv_path, columns)

        with st.form("audit_calendar_form"):
            c1, c2 = st.columns(2)
            month = c1.date_input("Month")
            courses = c2.text_area("Courses for Audit (comma-separated)")
            assigned = c1.text_input("Assigned To")
            deadline = c2.date_input("Deadline", datetime.date.today())
            progress = c1.slider("Progress (%)", 0, 100, 0)
            status = c2.selectbox("Status", status_options)
            notes = st.text_area("Notes")

            if st.form_submit_button("Submit Calendar Entry"):
                try:
                    if courses:
                        insert_data(csv_path, {
                            "Month": month.strftime("%B %Y"), "Courses for Audit": courses,
                            "Assigned To": assigned, "Deadline": deadline,
                            "Progress (%)": progress, "Status": status, "Notes": notes
                        })
                        st.success("✅ Calendar Entry Added")
                    else:
                        st.session_state.error_message = "Please fill at least Courses for Audit."
                except Exception as e:
                    st.session_state.error_message = str(e)

        df = fetch_data(csv_path, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "audit_calendar.csv")

        # Delete section
        st.subheader("Delete Entry")
        s_no = st.number_input("S.No to Delete", min_value=1, step=1)
        if st.button("Delete", key="delete_audit_calendar"):
            try:
                df = fetch_data(csv_path, columns)
                df = df[df["S.No"] != s_no]
                df["S.No"] = range(1, len(df) + 1)
                df.to_csv(csv_path, index=False)
                st.success(f"✅ Entry {s_no} Deleted!")
            except Exception as e:
                st.session_state.error_message = str(e)

    # ---------- Section iii: Feedback Summary ----------
    with tabs[2]:
        st.subheader("📝 Feedback Summary")
        csv_path = 'feedback_summary.csv'
        columns = [
            "S.No", "Course Name", "Feedback Source", "Rating (1-5)", "Key Suggestions",
            "Action Taken", "Date Received", "Follow-up Date"
        ]

        create_csv(csv_path, columns)

        with st.form("feedback_summary_form"):
            c1, c2 = st.columns(2)
            course = c1.text_input("Course Name")
            source = c2.text_input("Feedback Source")
            rating = c1.slider("Rating (1-5)", 1, 5, 3)
            suggestions = st.text_area("Key Suggestions")
            action = st.text_area("Action Taken")
            received = c1.date_input("Date Received", datetime.date.today())
            followup = c2.date_input("Follow-up Date", datetime.date.today())

            if st.form_submit_button("Submit Feedback"):
                try:
                    if course:
                        insert_data(csv_path, {
                            "Course Name": course, "Feedback Source": source, "Rating (1-5)": rating,
                            "Key Suggestions": suggestions, "Action Taken": action,
                            "Date Received": received, "Follow-up Date": followup
                        })
                        st.success("✅ Feedback Added")
                    else:
                        st.session_state.error_message = "Please fill at least Course Name."
                except Exception as e:
                    st.session_state.error_message = str(e)

        df = fetch_data(csv_path, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "feedback_summary.csv")

        # Delete section
        st.subheader("Delete Entry")
        s_no = st.number_input("S.No to Delete", min_value=1, step=1)
        if st.button("Delete", key="delete_feedback_summary"):
            try:
                df = fetch_data(csv_path, columns)
                df = df[df["S.No"] != s_no]
                df["S.No"] = range(1, len(df) + 1)
                df.to_csv(csv_path, index=False)
                st.success(f"✅ Entry {s_no} Deleted!")
            except Exception as e:
                st.session_state.error_message = str(e)

def Content_QC_Page():
    st.header("📑 Content QC Page")
    tabs = st.tabs(["📄 Main Content QC", "📖 Textbook QC", "📝 Worksheet QC"])

    # ---------- Main Content QC (Lesson Plan) ----------
    with tabs[0]:
        st.subheader("📄 Main Content QC (Lesson Plan)")
        file = 'lesson_plan_qc.csv'
        columns = [
            "S.No", "COURSE NAME", "CONTENT SUBMITTED ON", "VERSION", "UPDATED DATE",
            "CURRICULUM ALIGNMENT", "CONCEPT CLARITY", "LANGUAGE & GRAMMAR",
            "INNOVATION & ENGAGEMENT", "ACTIVITY & EXPERIMENT QUALITY",
            "VISUALS & DIAGRAMS", "ASSESSMENT INTEGRATION", "FLOW OF CONTENT",
            "QC 1 FEEDBACK DATE", "QC 1 CONTENT RECEIVED ON",
            "QC 2 FEEDBACK DATE", "QC 2 CONTENT RECEIVED ON", "REMARKS"
        ]
        create_csv(file, columns)

        with st.form("form_lesson_plan_qc"):
            w1, w2, w3 = st.columns(3)
            course = w1.text_input("COURSE NAME")
            submitted = w2.date_input("CONTENT SUBMITTED ON")
            version = w3.text_input("VERSION")
            updated_date = w1.date_input("UPDATED DATE")
            curriculum = w2.text_area("CURRICULUM ALIGNMENT")
            concept = w3.text_area("CONCEPT CLARITY")
            language = w1.text_area("LANGUAGE & GRAMMAR")
            innovation = w2.text_area("INNOVATION & ENGAGEMENT")
            activity = w3.text_area("ACTIVITY & EXPERIMENT QUALITY")
            visuals = w1.text_area("VISUALS & DIAGRAMS")
            assessment = w2.text_area("ASSESSMENT INTEGRATION")
            flow = w3.text_area("FLOW OF CONTENT")
            qc1_date = w1.date_input("QC 1 FEEDBACK DATE")
            qc1_recv = w2.date_input("QC 1 CONTENT RECEIVED ON")
            qc2_date = w3.date_input("QC 2 FEEDBACK DATE")
            qc2_recv = w1.date_input("QC 2 CONTENT RECEIVED ON")
            remarks = st.text_area("REMARKS")

            if st.form_submit_button("Submit Lesson Plan QC"):
                try:
                    if course:
                        insert_data(file, {
                            "COURSE NAME": course, "CONTENT SUBMITTED ON": submitted, "VERSION": version,
                            "UPDATED DATE": updated_date, "CURRICULUM ALIGNMENT": curriculum,
                            "CONCEPT CLARITY": concept, "LANGUAGE & GRAMMAR": language,
                            "INNOVATION & ENGAGEMENT": innovation, "ACTIVITY & EXPERIMENT QUALITY": activity,
                            "VISUALS & DIAGRAMS": visuals, "ASSESSMENT INTEGRATION": assessment,
                            "FLOW OF CONTENT": flow, "QC 1 FEEDBACK DATE": qc1_date,
                            "QC 1 CONTENT RECEIVED ON": qc1_recv, "QC 2 FEEDBACK DATE": qc2_date,
                            "QC 2 CONTENT RECEIVED ON": qc2_recv, "REMARKS": remarks
                        })
                        st.success("✅ Lesson Plan QC Entry Saved!")
                    else:
                        st.session_state.error_message = "Please fill at least the Course Name."
                except Exception as e:
                    st.session_state.error_message = str(e)

        df = fetch_data(file, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "lesson_plan_qc.csv")

        # Delete section
        st.subheader("Delete Entry")
        s_no = st.number_input("S.No to Delete", min_value=1, step=1)
        if st.button("Delete", key="delete_lesson_plan"):
            try:
                df = fetch_data(file, columns)
                df = df[df["S.No"] != s_no]
                df["S.No"] = range(1, len(df) + 1)
                df.to_csv(file, index=False)
                st.success(f"✅ Entry {s_no} Deleted!")
            except Exception as e:
                st.session_state.error_message = str(e)

    # ---------- Textbook QC ----------
    with tabs[1]:
        st.subheader("📖 Textbook QC")
        file = 'textbook_qc.csv'
        columns = [
            "S.No", "COURSE NAME", "CONTENT SUBMITTED ON", "VERSION", "UPDATED DATE",
            "CURRICULUM ALIGNMENT", "CONCEPT ACCURACY", "LANGUAGE & GRAMMAR",
            "STRUCTURE & ORGANIZATION", "ILLUSTRATIONS & VISUALS",
            "EXERCISE & ASSESSMENT", "INNOVATION & ENGAGEMENT",
            "QC 1 FEEDBACK DATE", "QC 1 CONTENT RECEIVED ON",
            "QC 2 FEEDBACK DATE", "QC 2 CONTENT RECEIVED ON", "REMARKS"
        ]
        create_csv(file, columns)

        with st.form("form_textbook_qc"):
            w1, w2, w3 = st.columns(3)
            course = w1.text_input("COURSE NAME")
            submitted = w2.date_input("CONTENT SUBMITTED ON")
            version = w3.text_input("VERSION")
            updated_date = w1.date_input("UPDATED DATE")
            curriculum = w2.text_area("CURRICULUM ALIGNMENT")
            concept = w3.text_area("CONCEPT ACCURACY")
            language = w1.text_area("LANGUAGE & GRAMMAR")
            structure = w2.text_area("STRUCTURE & ORGANIZATION")
            illustrations = w3.text_area("ILLUSTRATIONS & VISUALS")
            exercise = w1.text_area("EXERCISE & ASSESSMENT")
            innovation = w2.text_area("INNOVATION & ENGAGEMENT")
            qc1_date = w3.date_input("QC 1 FEEDBACK DATE")
            qc1_recv = w1.date_input("QC 1 CONTENT RECEIVED ON")
            qc2_date = w2.date_input("QC 2 FEEDBACK DATE")
            qc2_recv = w3.date_input("QC 2 CONTENT RECEIVED ON")
            remarks = st.text_area("REMARKS")

            if st.form_submit_button("Submit Textbook QC"):
                try:
                    if course:
                        insert_data(file, {
                            "COURSE NAME": course, "CONTENT SUBMITTED ON": submitted, "VERSION": version,
                            "UPDATED DATE": updated_date, "CURRICULUM ALIGNMENT": curriculum,
                            "CONCEPT ACCURACY": concept, "LANGUAGE & GRAMMAR": language,
                            "STRUCTURE & ORGANIZATION": structure, "ILLUSTRATIONS & VISUALS": illustrations,
                            "EXERCISE & ASSESSMENT": exercise, "INNOVATION & ENGAGEMENT": innovation,
                            "QC 1 FEEDBACK DATE": qc1_date, "QC 1 CONTENT RECEIVED ON": qc1_recv,
                            "QC 2 FEEDBACK DATE": qc2_date, "QC 2 CONTENT RECEIVED ON": qc2_recv,
                            "REMARKS": remarks
                        })
                        st.success("✅ Textbook QC Entry Saved!")
                    else:
                        st.session_state.error_message = "Please fill at least the Course Name."
                except Exception as e:
                    st.session_state.error_message = str(e)

        df = fetch_data(file, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "textbook_qc.csv")

        # Delete section
        st.subheader("Delete Entry")
        s_no = st.number_input("S.No to Delete", min_value=1, step=1)
        if st.button("Delete", key="delete_textbook"):
            try:
                df = fetch_data(file, columns)
                df = df[df["S.No"] != s_no]
                df["S.No"] = range(1, len(df) + 1)
                df.to_csv(file, index=False)
                st.success(f"✅ Entry {s_no} Deleted!")
            except Exception as e:
                st.session_state.error_message = str(e)

    # ---------- Worksheet QC ----------
    with tabs[2]:
        st.subheader("📝 Worksheet QC")
        file = 'worksheet_qc.csv'
        columns = [
            "S.No", "COURSE NAME", "CONTENT SUBMITTED ON", "VERSION", "UPDATED DATE",
            "CURRICULUM ALIGNMENT", "CONCEPT ACCURACY", "LANGUAGE",
            "STRUCTURE OF OPTIONS", "DISTRACTOR QUALITY", "VARIETY & COVERAGE",
            "LANGUAGE & GRAMMAR", "FORMATTING & NUMBERING", "ANSWER KEY ACCURACY",
            "QC 1 FEEDBACK DATE", "QC 1 CONTENT RECEIVED ON",
            "QC 2 FEEDBACK DATE", "QC 2 CONTENT RECEIVED ON", "REMARKS"
        ]
        create_csv(file, columns)

        with st.form("form_worksheet_qc"):
            w1, w2, w3 = st.columns(3)
            course = w1.text_input("COURSE NAME")
            submitted = w2.date_input("CONTENT SUBMITTED ON")
            version = w3.text_input("VERSION")
            updated_date = w1.date_input("UPDATED DATE")
            curriculum = w2.text_area("CURRICULUM ALIGNMENT")
            concept = w3.text_area("CONCEPT ACCURACY")
            language = w1.text_area("LANGUAGE")
            options = w2.text_area("STRUCTURE OF OPTIONS")
            distractors = w3.text_area("DISTRACTOR QUALITY")
            variety = w1.text_area("VARIETY & COVERAGE")
            grammar = w2.text_area("LANGUAGE & GRAMMAR")
            formatting = w3.text_area("FORMATTING & NUMBERING")
            answer_key = w1.text_area("ANSWER KEY ACCURACY")
            qc1_date = w2.date_input("QC 1 FEEDBACK DATE")
            qc1_recv = w3.date_input("QC 1 CONTENT RECEIVED ON")
            qc2_date = w1.date_input("QC 2 FEEDBACK DATE")
            qc2_recv = w2.date_input("QC 2 CONTENT RECEIVED ON")
            remarks = st.text_area("REMARKS")

            if st.form_submit_button("Submit Worksheet QC"):
                try:
                    if course:
                        insert_data(file, {
                            "COURSE NAME": course, "CONTENT SUBMITTED ON": submitted, "VERSION": version,
                            "UPDATED DATE": updated_date, "CURRICULUM ALIGNMENT": curriculum,
                            "CONCEPT ACCURACY": concept, "LANGUAGE": language,
                            "STRUCTURE OF OPTIONS": options, "DISTRACTOR QUALITY": distractors,
                            "VARIETY & COVERAGE": variety, "LANGUAGE & GRAMMAR": grammar,
                            "FORMATTING & NUMBERING": formatting, "ANSWER KEY ACCURACY": answer_key,
                            "QC 1 FEEDBACK DATE": qc1_date, "QC 1 CONTENT RECEIVED ON": qc1_recv,
                            "QC 2 FEEDBACK DATE": qc2_date, "QC 2 CONTENT RECEIVED ON": qc2_recv,
                            "REMARKS": remarks
                        })
                        st.success("✅ Worksheet QC Entry Saved!")
                    else:
                        st.session_state.error_message = "Please fill at least the Course Name."
                except Exception as e:
                    st.session_state.error_message = str(e)

        df = fetch_data(file, columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "worksheet_qc.csv")

        # Delete section
        st.subheader("Delete Entry")
        s_no = st.number_input("S.No to Delete", min_value=1, step=1)
        if st.button("Delete", key="delete_worksheet"):
            try:
                df = fetch_data(file, columns)
                df = df[df["S.No"] != s_no]
                df["S.No"] = range(1, len(df) + 1)
                df.to_csv(file, index=False)
                st.success(f"✅ Entry {s_no} Deleted!")
            except Exception as e:
                st.session_state.error_message = str(e)

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
    disable_enter_key()  # Prevent Enter submission
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
                try:
                    if built or revised:  # Example validation, adjust as needed
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
                    else:
                        st.session_state.error_message = "Please fill at least one metric field."
                except Exception as e:
                    st.session_state.error_message = str(e)

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
                try:
                    insert_data(kpi_file, {"KPI": kpi, "Target": target, "Owner": owner})
                    st.success("✅ KPI Record Added")
                except Exception as e:
                    st.session_state.error_message = str(e)

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
                try:
                    insert_data(kpi_team_file, {
                        "Content Creation": creation,
                        "Content Quality & Improvement": quality,
                        "Quality & Accuracy": accuracy
                    })
                    st.success("✅ Content Team KPI Submitted")
                except Exception as e:
                    st.session_state.error_message = str(e)

        df = fetch_data(kpi_team_file, kpi_team_columns)
        st.dataframe(df, use_container_width=True)
        download_csv(df, "content_team_kpis.csv")

# ----------------- App Config and Error Handling -----------------
st.set_page_config(page_title="Content Team Dashboard", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "error_message" not in st.session_state:
    st.session_state.error_message = ""

try:
    if not st.session_state.logged_in:
        login_screen()
    else:
        sidebar_navigation()
except Exception as e:
    # Sanitize the error message to remove newlines and special characters
    sanitized_error = str(e).replace('\n', ' ').replace('\r', ' ')
    st.session_state.error_message = sanitized_error
    components.html(f"""
    <div id="error-message" style="display:none;">{sanitized_error}</div>
    <div id="popup" class="popup">
        <div class="popup-content">
            <h3>Error</h3>
            <p id="error-text"></p>
            <button class="close-btn" onclick="document.getElementById('popup').style.display='none'">Close</button>
        </div>
    </div>
    <script>
        // Get the error message from the hidden div
        const errorMessage = document.getElementById('error-message').innerText;
        if (errorMessage) {{
            document.getElementById('error-text').innerText = errorMessage;
            document.getElementById('popup').style.display = 'block';
        }}
        // Clear the error message after displaying
        document.getElementById('error-message').innerText = '';
    </script>
    """, height=0)