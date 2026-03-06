import streamlit as st
import requests

API_URL = "http://localhost:5001/api"

# --- API Helper Functions ---
def analyze_error(error_input):
    resp = requests.post(f"{API_URL}/analyze", json={"error_input": error_input}, timeout=60)
    resp.raise_for_status()
    return resp.json()

def reevaluate_error(payload):
    resp = requests.post(f"{API_URL}/reevaluate", json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()

# --- UI Component Helpers ---
def display_analysis(analysis):
    st.subheader("Root Cause")
    st.error(analysis.get('root_cause', ''))
    
    st.subheader("Recommendations")
    for rec in analysis.get("recommendations", []):
        st.markdown(f"- {rec}")
        
    st.subheader("Preventive Suggestions")
    for sug in analysis.get("preventive_suggestions", []):
        st.markdown(f"- {sug}")

def display_metadata(metadata):
    st.subheader("Metadata")
    cols = st.columns(2)
    with cols[0]:
        st.write(f"**Language:** `{metadata.get('detected_language', '')}`")
        st.write(f"**Confidence:** `{metadata.get('language_confidence', '')}`")
        st.write(f"**Platform:** `{metadata.get('detected_platform', '')}`")
    with cols[1]:
        st.write(f"**Severity:** `{metadata.get('severity', '')}`")
        st.write(f"**Error Type:** `{metadata.get('error_type', '')}`")
        st.write(f"**Error Message:** `{metadata.get('error_message', '')}`")

# --- Main App ---
def main():
    st.set_page_config(page_title="AI Bug & Error Root Cause Analyzer", layout="centered")
    st.title("AI Bug & Error Root Cause Analyzer")

    # 1. Initial Analysis Form
    with st.form("analyze_form"):
        error_input = st.text_area("Paste your error log, stack trace, or CI/CD output here:", height=180)
        submitted = st.form_submit_button("Analyze")
        
    if submitted and error_input.strip():
        with st.spinner("Analyzing..."):
            try:
                result = analyze_error(error_input)
                # Store results in session state
                st.session_state.update({
                    "last_input": error_input,
                    "metadata": result.get("metadata", {}),
                    "analysis": result.get("analysis", {}),
                    "is_reevaluated": False
                })
            except Exception as e:
                st.error(f"Analysis Error: {e}")

    # 2. Display Results if available
    if "analysis" in st.session_state:
        st.divider()
        
        display_analysis(st.session_state["analysis"])
        st.divider()
        display_metadata(st.session_state["metadata"])
        st.divider()

        # 3. Re-evaluation UI
        st.subheader("Re-evaluate / Ask for More")
        
        if st.session_state.get("is_reevaluated"):
            st.success("Re-evaluation complete! Results updated above.")

        # Key trick to clear the text area after submission
        if "user_key" not in st.session_state:
            st.session_state["user_key"] = 0

        user_message = st.text_area(
            "Ask a follow-up, challenge the result, or request more detail:",
            key=f"user_message_{st.session_state['user_key']}"
        )

        if st.button("Re-evaluate") and user_message.strip():
            with st.spinner("Re-evaluating..."):
                try:
                    payload = {
                        "error_input": st.session_state["last_input"],
                        "metadata": st.session_state["metadata"],
                        "analysis": st.session_state["analysis"],
                        "user_message": user_message
                    }
                    result = reevaluate_error(payload)
                    
                    # Update session state with new results
                    st.session_state.update({
                        "analysis": result.get("analysis", {}),
                        "metadata": result.get("metadata", st.session_state["metadata"]),
                        "is_reevaluated": True
                    })
                    st.session_state["user_key"] += 1
                    try:
                        st.rerun()
                    except AttributeError:
                        st.experimental_rerun()
                except Exception as e:
                    st.error(f"Re-evaluation Error: {e}")

if __name__ == "__main__":
    main()
