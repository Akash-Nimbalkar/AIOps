import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import re
from groq import Groq
from serpapi import GoogleSearch


organization = "akashnimbalkar"
project = "AIOps"
pat = "Eib4WxkG9Lbbcmw9eGfnDpfGOlvXPhJOFxcvL85tTlFSSK3jN2f9JQQJ99BFACAAAAAAAAAAAAASAZDO3CSi"
auth = HTTPBasicAuth('', pat)
groq_api_key = "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"
serpapi_key = "4b2705be353d02ff094cd5f90aa2c34ccf66a76e3162ea914870060e6e050e4d"


def extract_error(log_text):
    lines = log_text.splitlines()
    error_lines = []
    capture = False
    for line in lines:
        line = re.sub(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z ", "", line)
        if any(prefix in line for prefix in ["##[section]", "##[command]", "##[error]", "##[warning]", "Task :", "Description"]):
            continue
        if "Traceback (most recent call last):" in line:
            capture = True
            error_lines = [line]
            continue
        if capture:
            error_lines.append(line)
            if re.search(r"\w*Error[:]", line):
                break
    if error_lines:
        return "\n".join(error_lines)
    for line in reversed(lines):
        clean_line = re.sub(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z ", "", line)
        if "error" in clean_line.lower():
            return clean_line.strip()
    return "No specific error snippet found."


def call_groq_ai(error_snippet, task_name):
    client = Groq(api_key=groq_api_key)
    messages = [
        {"role": "system", "content": "You're a DevOps AI assistant. Give a structured analysis with:\n1. Error Summary\n2. Root Cause Analysis\n3. Suggested Fixes\n4. Verification Steps"},
        {"role": "user", "content": f"Analyze the following error:\n\nTask: {task_name}\nError:\n{error_snippet}"}
    ]
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return completion.choices[0].message.content.strip()


def fetch_reference_links(error_message, max_results=5):
    search = GoogleSearch({
        "q": error_message,
        "api_key": serpapi_key,
        "num": max_results
    })
    results = search.get_dict()
    links = []
    for result in results.get("organic_results", []):
        title = result.get("title", "")
        link = result.get("link", "")
        links.append(f"[{title}]({link})")
    return links if links else ["No useful reference links found."]



def render():
    st.markdown("""
        <style>
            .title { font-size: 40px; font-weight: bold; text-align: center; color: #0055aa; }
            .section { font-size: 24px; font-weight: 600; margin-top: 30px; color: #333; border-bottom: 2px solid #ccc; padding-bottom: 6px; }
            .footer { text-align: center; color: #aaa; margin-top: 40px; font-size: 13px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'>🚨 AI Pipeline Doctor</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Gen AI Powered Real-time Error Detetction & Resolution in DevOps Pipelines</p>", unsafe_allow_html=True)

    run_id = st.number_input("Enter Pipeline Run ID", min_value=1, step=1, format="%d")

    if st.button("🔍 Analyze This Pipeline"):
        timeline_url = f"https://dev.azure.com/{organization}/{project}/_apis/build/builds/{run_id}/timeline?api-version=7.0"

        with st.spinner("Fetching pipeline data and analyzing errors..."):
            response = requests.get(timeline_url, auth=auth)

            if response.status_code == 200:
                records = response.json().get('records', [])
                failed_tasks = [r for r in records if r.get("result", "").lower() == "failed" and r.get("name", "").lower() not in ("__default", "job")]

                if not failed_tasks:
                    st.success("✅ Pipeline run completed successfully. No errors found.")
                    return

                for task in failed_tasks:
                    task_name = task.get("name")
                    log_url = task.get('log', {}).get('url')
                    if log_url:
                        log_response = requests.get(log_url, auth=auth)
                        if log_response.status_code == 200:
                            error_snippet = extract_error(log_response.text)

                           
                            st.markdown(f"<div class='section' style='color:#FF3F00;'>Task Failed: {task_name}</div>", unsafe_allow_html=True)
                            st.markdown("<div class='section' style='color:#FFFDD0;'>1. Extracted Error Log</div>", unsafe_allow_html=True)
                            st.code(error_snippet, language="python")

                            
                            ai_response = call_groq_ai(error_snippet, task_name)
                            st.markdown("<div class='section' style='color:#FFFDD0;'>2. AI-Powered Analysis</div>", unsafe_allow_html=True)
                            st.markdown(ai_response, unsafe_allow_html=True)

                            
                            reference_links = fetch_reference_links(error_snippet)
                            st.markdown("<div class='section' style='color:#FFFDD0;'>3. Reference Links</div>", unsafe_allow_html=True)
                            for link in reference_links:
                                st.markdown(f"- {link}")
                        else:
                            st.error("❌ Failed to fetch task log.")
            else:
                st.error("❌ Failed to fetch pipeline timeline data.")

        st.markdown("<div class='footer'>© 2025 AI Pipeline Doctor</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    render()


























































































# import streamlit as st
# import requests
# from requests.auth import HTTPBasicAuth
# import re
# from groq import Groq
# from serpapi import GoogleSearch

# # Configuration
# organization = "akashnimbalkar"
# project = "AIOps"
# pat = "Eib4WxkG9Lbbcmw9eGfnDpfGOlvXPhJOFxcvL85tTlFSSK3jN2f9JQQJ99BFACAAAAAAAAAAAAASAZDO3CSi"
# auth = HTTPBasicAuth('', pat)
# groq_api_key = "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"
# serpapi_key = "4b2705be353d02ff094cd5f90aa2c34ccf66a76e3162ea914870060e6e050e4d"

# # Extract error snippet from log
# def extract_error(log_text):
#     lines = log_text.splitlines()
#     error_lines = []
#     capture = False
#     for line in lines:
#         line = re.sub(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z ", "", line)
#         if any(prefix in line for prefix in ["##[section]", "##[command]", "##[error]", "##[warning]", "Task :", "Description"]):
#             continue
#         if "Traceback (most recent call last):" in line:
#             capture = True
#             error_lines = [line]
#             continue
#         if capture:
#             error_lines.append(line)
#             if re.search(r"\w*Error[:]", line):
#                 break
#     if error_lines:
#         return "\n".join(error_lines)
#     for line in reversed(lines):
#         clean_line = re.sub(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z ", "", line)
#         if "error" in clean_line.lower():
#             return clean_line.strip()
#     return "No specific error snippet found."

# # Generate explanation using Groq AI
# def call_groq_ai(error_snippet, task_name):
#     client = Groq(api_key=groq_api_key)
#     messages = [
#         {"role": "system", "content": "You're a DevOps AI assistant. Give a structured analysis with: Error Summary, Root Cause Analysis, Suggested Fixes, Verification Steps"},
#         {"role": "user", "content": f"Analyze this Azure DevOps task error:\n\nTask: {task_name}\nError:\n{error_snippet}"}
#     ]
#     completion = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=messages
#     )
#     return completion.choices[0].message.content.strip()

# # Search related resources via SerpAPI
# def fetch_reference_links(error_message, max_results=5):
#     search = GoogleSearch({
#         "q": error_message,
#         "api_key": serpapi_key,
#         "num": max_results
#     })
#     results = search.get_dict()
#     links = []
#     for result in results.get("organic_results", []):
#         title = result.get("title", "")
#         link = result.get("link", "")
#         links.append(f"[{title}]({link})")
#     return links if links else ["No useful reference links found."]

# # Main Streamlit App

# def render():
#     st.markdown("""
#         <style>
#             .title { font-size: 40px; font-weight: bold; text-align: center; color: #0055aa; }
#             .section { font-size: 24px; font-weight: 600; margin-top: 30px; color: #333; border-bottom: 2px solid #ccc; padding-bottom: 6px; }
#             .footer { text-align: center; color: #aaa; margin-top: 40px; font-size: 13px; }
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown("<div class='title'>🚨 Smart Log Assistant</div>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align:center;'>Real-time error diagnosis powered by Groq AI</p>", unsafe_allow_html=True)

#     run_id = st.number_input("🔢 Enter Pipeline Run ID", min_value=1, step=1, format="%d")

#     if run_id:
#         timeline_url = f"https://dev.azure.com/{organization}/{project}/_apis/build/builds/{run_id}/timeline?api-version=7.0"

#         with st.spinner("Fetching pipeline data and analyzing errors..."):
#             response = requests.get(timeline_url, auth=auth)

#             if response.status_code == 200:
#                 records = response.json().get('records', [])
#                 failed_tasks = [r for r in records if r.get("result", "").lower() == "failed" and r.get("name", "").lower() not in ("__default", "job")]

#                 if not failed_tasks:
#                     st.success("✅ Pipeline run completed successfully. No errors found.")
#                     return

#                 for task in failed_tasks:
#                     task_name = task.get("name")
#                     log_url = task.get('log', {}).get('url')
#                     if log_url:
#                         log_response = requests.get(log_url, auth=auth)
#                         if log_response.status_code == 200:
#                             error_snippet = extract_error(log_response.text)

#                             # Display Error Section
#                             st.markdown(f"<div class='section'>❌ Task Failed: {task_name}</div>", unsafe_allow_html=True)
#                             st.markdown("<div class='section'>1. Extracted Error Log</div>", unsafe_allow_html=True)
#                             st.code(error_snippet, language="python")

#                             # Groq AI Analysis
#                             ai_response = call_groq_ai(error_snippet, task_name)
#                             st.markdown("<div class='section'>2. AI-Powered Analysis</div>", unsafe_allow_html=True)
#                             st.markdown(ai_response, unsafe_allow_html=True)

#                             # References
#                             reference_links = fetch_reference_links(error_snippet)
#                             st.markdown("<div class='section'>6. Reference Links</div>", unsafe_allow_html=True)
#                             for link in reference_links:
#                                 st.markdown(f"- {link}")
#                         else:
#                             st.error("❌ Failed to fetch task log.")
#             else:
#                 st.error("❌ Failed to fetch pipeline timeline data.")

#         st.markdown("<div class='footer'>© 2025 Smart Log Assistant | Powered by Groq AI</div>", unsafe_allow_html=True)

# # Run the app
# if __name__ == "__main__":
#     render()







































# import streamlit as st
# import requests
# from requests.auth import HTTPBasicAuth
# import re
# from groq import Groq
# from serpapi import GoogleSearch

# # Configuration
# organization = "akashnimbalkar"
# project = "AIOps"
# pat = "Eib4WxkG9Lbbcmw9eGfnDpfGOlvXPhJOFxcvL85tTlFSSK3jN2f9JQQJ99BFACAAAAAAAAAAAAASAZDO3CSi"
# auth = HTTPBasicAuth('', pat)
# groq_api_key = "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"
# serpapi_key = "4b2705be353d02ff094cd5f90aa2c34ccf66a76e3162ea914870060e6e050e4d"

# # Extract error snippet from log
# def extract_error(log_text):
#     lines = log_text.splitlines()
#     error_lines = []
#     capture = False
#     for line in lines:
#         line = re.sub(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z ", "", line)
#         if any(prefix in line for prefix in ["##[section]", "##[command]", "##[error]", "##[warning]", "Task :", "Description"]):
#             continue
#         if "Traceback (most recent call last):" in line:
#             capture = True
#             error_lines = [line]
#             continue
#         if capture:
#             error_lines.append(line)
#             if re.search(r"\w*Error[:]", line):
#                 break
#     if error_lines:
#         return "\n".join(error_lines)
#     for line in reversed(lines):
#         clean_line = re.sub(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z ", "", line)
#         if "error" in clean_line.lower():
#             return clean_line.strip()
#     return "No specific error snippet found."

# # Generate explanation using Groq AI
# def call_groq_ai(error_snippet, task_name):
#     client = Groq(api_key=groq_api_key)
#     messages = [
#         {"role": "system", "content": "You are a professional DevOps assistant. Provide structured, intuitive error analysis with headings."},
#         {"role": "user", "content": f"Analyze this Azure DevOps task error:\n\nTask: {task_name}\nError:\n{error_snippet}"}
#     ]
#     completion = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=messages
#     )
#     return completion.choices[0].message.content.strip()

# # Search related resources via SerpAPI
# def fetch_reference_links(error_message, max_results=5):
#     search = GoogleSearch({
#         "q": error_message,
#         "api_key": serpapi_key,
#         "num": max_results
#     })
#     results = search.get_dict()
#     links = []
#     for result in results.get("organic_results", []):
#         title = result.get("title", "")
#         link = result.get("link", "")
#         links.append(f"[{title}]({link})")
#     return links if links else ["No useful reference links found."]

# # Main Streamlit App

# def render():
#     st.markdown("""
#         <style>
#             .title { font-size: 40px; font-weight: bold; text-align: center; color: #0055aa; }
#             .section { font-size: 24px; font-weight: 600; margin-top: 30px; color: #333; border-bottom: 2px solid #ccc; padding-bottom: 6px; }
#             .footer { text-align: center; color: #aaa; margin-top: 40px; font-size: 13px; }
#         </style>
#     """, unsafe_allow_html=True)

#     st.markdown("<div class='title'>🚨 Smart Log Assistant</div>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align:center;'>Real-time error diagnosis powered by Groq AI</p>", unsafe_allow_html=True)

#     run_id = st.number_input("🔢 Enter Pipeline Run ID", min_value=1, step=1, format="%d")

#     if run_id:
#         timeline_url = f"https://dev.azure.com/{organization}/{project}/_apis/build/builds/{run_id}/timeline?api-version=7.0"

#         with st.spinner("Fetching pipeline data and analyzing errors..."):
#             response = requests.get(timeline_url, auth=auth)

#             if response.status_code == 200:
#                 records = response.json().get('records', [])
#                 failed_tasks = [r for r in records if r.get("result", "").lower() == "failed" and r.get("name", "").lower() not in ("__default", "job")]

#                 if not failed_tasks:
#                     st.success("✅ Pipeline run completed successfully. No errors found.")
#                     return

#                 for task in failed_tasks:
#                     task_name = task.get("name")
#                     log_url = task.get('log', {}).get('url')
#                     if log_url:
#                         log_response = requests.get(log_url, auth=auth)
#                         if log_response.status_code == 200:
#                             error_snippet = extract_error(log_response.text)

#                             # Display Error Section
#                             st.markdown(f"<div class='section'>❌ Task Failed: {task_name}</div>", unsafe_allow_html=True)
#                             with st.expander("📄 View Extracted Error Snippet"):
#                                 st.code(error_snippet, language="python")

#                             # Groq AI Analysis
#                             ai_response = call_groq_ai(error_snippet, task_name)
#                             st.markdown("<div class='section'>💡 Pipeline Error Breakdown</div>", unsafe_allow_html=True)
#                             st.markdown(ai_response, unsafe_allow_html=True)

#                             # References
#                             reference_links = fetch_reference_links(error_snippet)
#                             st.markdown("<div class='section'>🔗 Helpful Reference Links</div>", unsafe_allow_html=True)
#                             for link in reference_links:
#                                 st.markdown(f"- {link}")
#                         else:
#                             st.error("❌ Failed to fetch task log.")
#             else:
#                 st.error("❌ Failed to fetch pipeline timeline data.")

#         st.markdown("<div class='footer'>© 2025 Smart Log Assistant | Powered by Groq AI</div>", unsafe_allow_html=True)

# # Run the app
# if __name__ == "__main__":
#     render()
