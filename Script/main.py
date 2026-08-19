import streamlit as st



st.set_page_config(
    page_icon="🤖",
    page_title="El_3arrif",
    layout="centered"
)


if "exit" not in st.session_state:
    st.session_state.exit = False

if st.session_state.exit:
    st.stop()

# Animation for the app starting
st.markdown(
    """
    <style>
        .loading-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 60vh;
        }

        .loading-word {
            font-size: 1.4rem;
            font-weight: 600;
            animation: loading-pulse 1.2s ease-in-out infinite;
        }

        @keyframes loading-pulse {
            0% {
                opacity: 0.3;
                transform: scale(0.98);
            }

            50% {
                opacity: 1;
                transform: scale(1.05);
            }

            100% {
                opacity: 0.3;
                transform: scale(0.98);
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Animation for Model's Answer:

st.markdown("""
<style>
.thinking-container {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 0;
}

.thinking-text {
    font-size: 16px;
    font-weight: 600;
}

.thinking-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #aaa;
    animation: bounce 1.4s infinite ease-in-out;
}

.thinking-dot:nth-child(2) {
    animation-delay: 0.2s;
}

.thinking-dot:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes bounce {
    0%, 80%, 100% {
        transform: scale(0.6);
        opacity: 0.5;
    }
    40% {
        transform: scale(1);
        opacity: 1;
    }
}
</style>
""", unsafe_allow_html=True)

Loading_placeholder = st.empty()

Loading_placeholder.markdown(
    """
    <div class="loading-container">
        <div class="loading-word">Loading...</div>
    </div>
    """,
    unsafe_allow_html=True
)

import json
from pathlib import Path
from Embeddings import Embeddings
from DataBase_Connection import Connection
from Storage import Text_Storage
from RAG import Retrieval
from COPILOT import LLM



@st.cache_resource(show_spinner=False)
def initialize_application():
    Model = LLM()
    Model.start_chat()
    embedding_manager = Embeddings()
    embedder = embedding_manager.get_embedder()

    connection = Connection()
    collection = connection.get_collection()

    store = Text_Storage(
        embedder,
        collection
    )

    retrieve = Retrieval(
        embedder,
        collection
    )


    return (
        embedder,
        collection,
        store,
        retrieve,
        Model)



try:
    embedder,collection,store,retrieve, Model  = initialize_application()
    Loading_placeholder.empty()

except Exception as error:
    Loading_placeholder.empty()

    st.error("Application initialization failed.")
    st.stop()



st.markdown(
    """
    <style>
   
    section[data-testid="stSidebar"][aria-expanded="true"] {
        width: 320px !important;
        min-width: 320px !important;
        max-width: 320px !important;
        flex-shrink: 0 !important;
    }

    section[data-testid="stSidebar"][aria-expanded="true"] > div {
        width: 320px !important;
        min-width: 320px !important;
        max-width: 320px !important;
    }

    section[data-testid="stSidebar"][aria-expanded="false"] {
        width: 0px !important;
        min-width: 0px !important;
        max-width: 0px !important;
    }

    section[data-testid="stSidebar"][aria-expanded="false"] > div {
        width: 0px !important;
        min-width: 0px !important;
        max-width: 0px !important;
    }

   
    div[data-testid="stSidebarCollapsedControl"],
    button[data-testid="stSidebarCollapsedControl"] {
        position: fixed !important;
        top: 70px !important;
        left: 12px !important;
        right: auto !important;
        z-index: 999999 !important;
    }

   
    div[data-testid="stSidebarCollapsedControl"] button,
    button[data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    
    section[data-testid="stSidebar"] div.stButton > button {
        min-height: 38px;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }

    section[data-testid="stSidebar"] div.stButton > button p {
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }


    section[data-testid="stSidebar"] div[data-testid="column"]:last-child div.stButton > button {
        width: 38px !important;
        min-width: 38px !important;
        max-width: 38px !important;
        height: 38px !important;
        padding: 0 !important;
        font-size: 18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


if "notification" not in st.session_state:
    st.session_state.notification = None

if "renaming_chat" not in st.session_state:
    st.session_state.renaming_chat = None


if st.session_state.notification:
    st.toast(st.session_state.notification)
    st.session_state.notification = None

if 'thinking' not in st.session_state:
    st.session_state.thinking = False

if 'prompt' not in st.session_state:
    st.session_state.prompt = None


CHAT_FILE = (
    Path(__file__).resolve().parent
    / "chat_history.json"
)



def empty_history():
    """
    Return an empty chat-history structure.
    """

    return {
        "chats": {},
        "active_chat": None,
        "chat_counter": 0
    }


def load_chats():
    """
    Load saved chats from chat_history.json.
    """

    if not CHAT_FILE.exists():
        return empty_history()

    try:
        file_content = CHAT_FILE.read_text(
            encoding="utf-8"
        )

        saved_data = json.loads(file_content)

        chats = saved_data.get("chats", {})
        active_chat = saved_data.get("active_chat")
        chat_counter = saved_data.get(
            "chat_counter",
            0
        )

        if not isinstance(chats, dict):
            chats = {}

        if not isinstance(chat_counter, int):
            chat_counter = 0

        return {
            "chats": chats,
            "active_chat": active_chat,
            "chat_counter": chat_counter
        }

    except (
        json.JSONDecodeError,
        OSError,
        TypeError
    ):
        return empty_history()


def save_chats():
    """
    Save all chat names, messages, and the selected
    chat to chat_history.json.
    """

    saved_data = {
        "chats": st.session_state.chats,
        "active_chat": st.session_state.active_chat,
        "chat_counter": st.session_state.chat_counter
    }

    temporary_file = CHAT_FILE.with_suffix(".tmp")

    temporary_file.write_text(
        json.dumps(
            saved_data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    temporary_file.replace(CHAT_FILE)




if "chats" not in st.session_state:
    saved_history = load_chats()

    st.session_state.chats = saved_history["chats"]
    st.session_state.active_chat = saved_history["active_chat"]
    st.session_state.chat_counter = saved_history["chat_counter"]


def create_new_chat():
    """
    Create a new empty chat only when the user clicks
    the New chat button.
    """

    st.session_state.chat_counter += 1

    chat_id = f"chat_{st.session_state.chat_counter}"

    st.session_state.chats[chat_id] = {
        "name": "New chat",
        "messages": []
    }

    st.session_state.active_chat = chat_id
    st.session_state.renaming_chat = None

    st.session_state.notification = (
        "New chat created successfully"
    )

    save_chats()


def create_chat_name(message):
    """
    Use the first message as the sidebar chat name.
    """

    message = message.strip()

    st.session_state.notification = (
        "Chat is created successfully"
    )

    if len(message) <= 28:
        return message

    return message[:28].rstrip() + "..."


def delete_chat(chat_id):
    """
    Delete one chat while preserving all other chats.
    Does not auto-create a new chat when the last chat is deleted.
    """

    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]

        st.session_state.notification = (
            "Chat deleted successfully"
        )

    st.session_state.renaming_chat = None

    remaining_chat_ids = list(
        st.session_state.chats.keys()
    )

    if remaining_chat_ids:
        st.session_state.active_chat = (
            remaining_chat_ids[-1]
        )
    else:
        st.session_state.active_chat = None

    save_chats()


def rename_chat(chat_id, new_name):
    """
    Rename the selected chat.
    """

    cleaned_name = new_name.strip()

    if (
        cleaned_name
        and chat_id in st.session_state.chats
    ):
        st.session_state.chats[
            chat_id
        ]["name"] = cleaned_name

        st.session_state.notification = (
            "Chat is renamed successfully"
        )

    st.session_state.renaming_chat = None

    save_chats()


@st.dialog("Chat Options")
def chat_options(chat_id):
    """
    Show chat options in a dialog.
    """

    if st.button(
        "✏️ Rename",
        key=f"rename_{chat_id}",
        use_container_width=True
    ):
        st.session_state.renaming_chat = chat_id
        st.rerun()

    if st.button(
        "🗑️ Delete",
        key=f"delete_{chat_id}",
        use_container_width=True
    ):
        delete_chat(chat_id)
        st.rerun()

if (
    st.session_state.active_chat
    not in st.session_state.chats
):
    st.session_state.active_chat = None




with st.sidebar:
    if st.button("Exit", use_container_width=True, disabled= st.session_state.thinking):

        try:
            Model.quit_Copilot()
        except Exception:
            pass
        initialize_application.clear() 
        st.cache_resource.clear()
        st.session_state.exit = True       
        st.rerun()


            

    if st.button(
        "＋ New chat",
        use_container_width=True,
        disabled= st.session_state.thinking
    ):
        create_new_chat()
        st.rerun()

    st.divider()
    st.caption("Chats")

    chat_items = list(
        st.session_state.chats.items()
    )

    for menu_index, (chat_id, chat) in enumerate(
        reversed(chat_items)
    ):
        chat_name_column, menu_column = st.columns(
            [9, 1],
            vertical_alignment="center"
        )


        with chat_name_column:
            if st.button(
                chat["name"],
                key=f"open_{chat_id}",
                use_container_width=True,
                disabled= st.session_state.thinking
            ):
                st.session_state.active_chat = chat_id
                st.session_state.renaming_chat = None

                save_chats()
                st.rerun()


        with menu_column:
            if st.button(
                "⚙",
                key=f"menu_{chat_id}",
                use_container_width=True,
                disabled=st.session_state.thinking
            ):
                chat_options(chat_id)


        if (
            st.session_state.renaming_chat
            == chat_id
        ):
            with st.form(
                key=f"rename_form_{chat_id}"
            ):
                new_chat_name = st.text_input(
                    "Chat name",
                    value=chat["name"],
                    label_visibility="collapsed",
                    placeholder="Enter a new chat name"
                )

                save_column, cancel_column = st.columns(2)

                with save_column:
                    save_name_button = (
                        st.form_submit_button(
                            "Save",
                            use_container_width=True,
                            type="primary"
                        )
                    )

                with cancel_column:
                    cancel_name_button = (
                        st.form_submit_button(
                            "Cancel",
                            use_container_width=True
                        )
                    )

                if save_name_button:
                    rename_chat(
                        chat_id,
                        new_chat_name
                    )

                    st.rerun()

                if cancel_name_button:
                    st.session_state.renaming_chat = None
                    st.rerun()




active_chat_id = st.session_state.active_chat

active_chat = None

if (
    active_chat_id is not None
    and active_chat_id in st.session_state.chats
):
    active_chat = st.session_state.chats[
        active_chat_id
    ]


Welcome_Message = st.empty()

if active_chat is None:
    Welcome_Message.markdown(
        """
        <div style="margin-top:350px">
            <h3>Hi, How can I help you today</h3>
            <p>Click New chat from the sidebar to start a conversation</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    if len(active_chat["messages"]) == 0:
        Welcome_Message.markdown(
            """
            <div style="margin-top:350px">
                <h3>Hi, How can I help you today</h3>
                <p>Send a message to start the conversation</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for message in active_chat["messages"]:
        Welcome_Message.empty()

        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html= True)



prompt = st.chat_input("Message EL_3ariff...", disabled= st.session_state.thinking)

if prompt:
    st.session_state.thinking = True
    st.session_state.prompt = prompt
    # If there is no active chat, create one when user sends first message
    if active_chat is None:
                create_new_chat()
    
                active_chat_id = st.session_state.active_chat
                active_chat = st.session_state.chats[
                    active_chat_id
                ]
    
            # Set the sidebar chat name from
            # the first message
    if not active_chat["messages"] and active_chat['name'] == 'New chat':
                active_chat["name"] = (
                    create_chat_name(prompt)
                )
    
    active_chat["messages"].append(
            {
                "role": "user",
                "content": prompt
            }
        )
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.rerun()
prompt = st.session_state.prompt

if (prompt and  st.session_state.thinking == True):

        if prompt.startswith("info:"):

            answer = "I got it. Thanks for the info"

            store.store_text(prompt[6:].strip())

            with st.chat_message("assistant"):
                st.markdown(answer, unsafe_allow_html= True)

            active_chat["messages"].append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )
            st.session_state.thinking = False


        else:

            retrieved_context = retrieve.retrieve_chunks(prompt)

            thinking_placeholder = st.empty()
            
            thinking_placeholder.markdown(
                    """
                    <div class="thinking-container">
                        <span class="thinking-text">thinking</span>
                        <div class="thinking-dot"></div>
                        <div class="thinking-dot"></div>
                        <div class="thinking-dot"></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            answer = Model.get_answer(
                retrieved_context,
                prompt
            )

            thinking_placeholder.code(answer, language = None)
            st.session_state.thinking = False

            with st.chat_message("assistant"):
                st.markdown(answer, unsafe_allow_html= True)

            active_chat["messages"].append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )
       
        save_chats()
        st.rerun()