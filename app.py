import os
import streamlit as st

from agent import client, tools, execute_tool
from memory import add_message, get_memory
from sticker_tool import get_sticker, classify_question


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="AURA",
    page_icon="✦",
    layout="centered"
)


# ==================================================
# CLEAR OLD UI MESSAGES ONCE
# ==================================================

if "old_ui_cleared" not in st.session_state:
    st.session_state.messages = []
    st.session_state.old_ui_cleared = True


# ==================================================
# CUSTOM AURA UI
# ==================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f5f5f2;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    .aura-heading {
        font-size: 46px;
        font-weight: 750;
        letter-spacing: -2px;
        color: #1e293b;
        margin-bottom: 0px;
    }

    .aura-full-name {
        font-size: 15px;
        font-weight: 500;
        letter-spacing: 0.3px;
        color: #64748b;
        margin-top: 2px;
        margin-bottom: 28px;
    }

    .aura-status {
        display: flex;
        align-items: center;
        gap: 8px;
        width: fit-content;
        padding: 7px 12px;
        margin-bottom: 24px;

        border: 1px solid #d6d8d5;
        border-radius: 20px;

        background: #fafaf8;

        color: #475569;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.4px;
    }

    

    div[data-testid="stChatMessage"] {
        background: transparent;
        border: none;
        padding: 8px 4px;
    }

    div[data-testid="stChatInput"] {
        border: 1px solid #aeb5bd !important;
        border-radius: 14px !important;
        background: #ffffff !important;

        box-shadow:
            0 3px 12px rgba(15, 23, 42, 0.06) !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border: 1px solid #475569 !important;

        box-shadow:
            0 0 0 2px rgba(70, 85, 105, 0.10),
            0 3px 12px rgba(15, 23, 42, 0.06) !important;
    }

    div[data-testid="stChatInput"] textarea {
        font-size: 15px !important;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }


    /* ---------------------------------
       Message + Sticker
       --------------------------------- */

    .aura-message-row {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 10px;
        width: fit-content;
        max-width: 100%;
    }

    .aura-message-text {
        display: inline-block;
        max-width: 700px;
        font-size: 16px;
        line-height: 1.55;
        color: #1e293b;
        word-wrap: break-word;
        white-space: pre-wrap;
    }

    .aura-sticker {
        width: 65px;
        height: 65px;
        object-fit: contain;
        flex-shrink: 0;
    }


    /* ---------------------------------
       Agent Activity
       --------------------------------- */

    .agent-activity {
        width: fit-content;
        max-width: 720px;

        margin-top: 6px;
        margin-bottom: 14px;

        padding: 14px 18px;

        border: 1px solid #d6d8d5;
        border-radius: 12px;

        background: #fafaf8;

        color: #475569;

        font-size: 13px;
    }

    .activity-title {
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 12px;
    }

    .workflow {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 7px;
    }

    .workflow-step {
        display: flex;
        align-items: center;
        gap: 5px;
        white-space: nowrap;
    }

    .workflow-step.completed {
        color: #475569;
    }

    .workflow-step.active {
        color: #1e293b;
        font-weight: 700;
    }

    .workflow-line {
        width: 18px;
        height: 1px;
        background: #cbd0d5;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# AURA HEADER
# ==================================================

st.markdown(
    """
    <div class="aura-heading">✦ AURA</div>

    <div class="aura-full-name">
        AI Utility & Research Assistant
    </div>

    <div class="aura-status">
        <span class="status-dot"></span>
        UTILITY • RESEARCH • TOOLS
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# DISPLAY MESSAGE + STICKER
# ==================================================

def display_message_with_sticker(role, message, sticker_path):

    with st.chat_message(role):

        message_col, sticker_col = st.columns([5.5, 1])

        with message_col:
            st.markdown(message)

        with sticker_col:

            if sticker_path and os.path.exists(sticker_path):

                st.image(
                    sticker_path,
                    width=65
                )


# ==================================================
# AGENT ACTIVITY
# ==================================================

def show_agent_activity(tool_name):

    with st.expander(
        "⚙️ Agent Activity",
        expanded=False
    ):

        st.write("✓ Request received")
        st.write("✓ Understanding the request")
        st.write(
            f"✓ Selecting tool: `{tool_name}`"
        )
        st.write("✓ Executing tool")
        st.write("✓ Preparing final answer")


# ==================================================
# RUN AI AGENT
# ==================================================

def run_agent(user_input):

    messages = get_memory().copy()

    messages.append({
        "role": "user",
        "content": user_input
    })

    used_tools = []

    while True:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message


        # ------------------------------------------
        # AURA HAS FINISHED
        # ------------------------------------------

        if not message.tool_calls:

            return message.content, used_tools


        # ------------------------------------------
        # SAVE TOOL CALL
        # ------------------------------------------

        assistant_message = {
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": []
        }


        for tool_call in message.tool_calls:

            assistant_message["tool_calls"].append({
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                }
            })


        messages.append(assistant_message)


        # ------------------------------------------
        # EXECUTE TOOLS
        # ------------------------------------------

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            used_tools.append(tool_name)

            result = execute_tool(tool_call)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })


# ==================================================
# DISPLAY PREVIOUS CHAT
# ==================================================

for message in st.session_state.messages:

    display_message_with_sticker(
        message["role"],
        message["content"],
        message.get("sticker")
    )


# ==================================================
# CHAT INPUT
# DOCUMENT UPLOAD IS INSIDE CHATBOX
# ==================================================

chat_input = st.chat_input(
    "Ask AURA anything...",
    accept_file=True,
    file_type=["txt", "pdf", "docx"]
)


# ==================================================
# PROCESS CHAT INPUT
# ==================================================

if chat_input:

    # ------------------------------------------
    # GET TEXT
    # ------------------------------------------

    user_input = chat_input.text.strip()


    # ------------------------------------------
    # GET ATTACHED FILES
    # ------------------------------------------

    attached_files = chat_input.files

    uploaded_filenames = []


    # ------------------------------------------
    # SAVE ATTACHED DOCUMENTS
    # ------------------------------------------

    if attached_files:

        os.makedirs(
            "documents",
            exist_ok=True
        )

        for uploaded_file in attached_files:

            safe_filename = os.path.basename(
                uploaded_file.name
            )

            document_path = os.path.join(
                "documents",
                safe_filename
            )

            with open(
                document_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )

            uploaded_filenames.append(
                safe_filename
            )


    # ------------------------------------------
    # CREATE DOCUMENT REQUEST
    # ------------------------------------------

    if uploaded_filenames:

        if user_input:

            user_input = (
                f"{user_input}\n\n"
                f"The user attached the following "
                f"document(s): "
                f"{', '.join(uploaded_filenames)}. "
                f"Use the read_document tool to read "
                f"the relevant document before answering."
            )

        else:

            user_input = (
                f"Please read and explain the following "
                f"document(s): "
                f"{', '.join(uploaded_filenames)}. "
                f"Use the read_document tool."
            )


    # ------------------------------------------
    # PROCESS ONLY IF THERE IS CONTENT
    # ------------------------------------------

    if user_input:

        # --------------------------------------
        # CLASSIFY USER QUESTION
        # --------------------------------------

        question_category = classify_question(
            user_input
        )


        # --------------------------------------
        # GET USER STICKER
        # --------------------------------------

        question_sticker = get_sticker(
            question_category
        )


        # --------------------------------------
        # SAVE USER MESSAGE
        # --------------------------------------

        user_message = {
            "role": "user",
            "content": user_input,
            "sticker": question_sticker
        }

        st.session_state.messages.append(
            user_message
        )


        # --------------------------------------
        # SAVE USER MESSAGE TO MEMORY
        # --------------------------------------

        add_message(
            "user",
            user_input
        )


        # --------------------------------------
        # DISPLAY USER MESSAGE
        # --------------------------------------

        display_message_with_sticker(
            "user",
            user_input,
            question_sticker
        )


        # --------------------------------------
        # RUN AURA
        # --------------------------------------

        try:

            with st.spinner(
                "AURA is thinking..."
            ):

                answer, used_tools = run_agent(
                    user_input
                )


            # ----------------------------------
            # AGENT ACTIVITY
            # ----------------------------------

            if used_tools:

                for tool_name in used_tools:

                    show_agent_activity(
                        tool_name
                    )


            # ----------------------------------
            # AURA STICKER
            # ALWAYS HAPPY.PNG
            # ----------------------------------

            answer_sticker = get_sticker(
                "happy"
            )


            # ----------------------------------
            # SAVE AURA MESSAGE
            # ----------------------------------

            assistant_message = {
                "role": "assistant",
                "content": answer,
                "sticker": answer_sticker
            }

            st.session_state.messages.append(
                assistant_message
            )


            # ----------------------------------
            # SAVE AURA RESPONSE TO MEMORY
            # ----------------------------------

            add_message(
                "assistant",
                answer
            )


            # ----------------------------------
            # DISPLAY AURA RESPONSE
            # ----------------------------------

            display_message_with_sticker(
                "assistant",
                answer,
                answer_sticker
            )


        except Exception as error:

            error_text = str(error)


            # ----------------------------------
            # HANDLE RATE LIMIT
            # ----------------------------------

            if "429" in error_text:

                answer = (
                    "The AI service has temporarily "
                    "reached its free usage limit. "
                    "Please wait a little and try again."
                )

            else:

                answer = (
                    "Sorry, something went wrong "
                    "while processing your request."
                )


            # ----------------------------------
            # ERROR STICKER
            # ----------------------------------

            answer_sticker = get_sticker(
                "happy"
            )


            # ----------------------------------
            # SAVE ERROR MESSAGE
            # ----------------------------------

            assistant_message = {
                "role": "assistant",
                "content": answer,
                "sticker": answer_sticker
            }

            st.session_state.messages.append(
                assistant_message
            )


            add_message(
                "assistant",
                answer
            )


            # ----------------------------------
            # DISPLAY ERROR
            # ----------------------------------

            display_message_with_sticker(
                "assistant",
                answer,
                answer_sticker
            )