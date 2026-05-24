import streamlit as st

def apply_theme():

    st.markdown("""
    <style>

    /* BUTTONS */
    div.stButton > button:first-child {

        border-radius: 15px !important;

        border: 1px solid #7B2CBF !important;

        box-shadow:
            0 0 12px rgba(123, 44, 191, 0.6) !important;

        transition: 0.3s !important;

        font-weight: bold !important;
    }

    /* BUTTON HOVER */
    div.stButton > button:first-child:hover {

        box-shadow:
            0 0 10px #C77DFF,
            0 0 20px #9D4EDD,
            0 0 30px #7B2CBF !important;

        transform: scale(1.03) !important;
    }

    /* HEADERS */
    h1, h2, h3 {

        color: white !important;

        text-shadow:
            0 0 8px rgba(199, 125, 255, 0.7),
            0 0 16px rgba(123, 44, 191, 0.5);;
    }

    /* TEXT INPUTS */
    .stTextInput input {

        border-radius: 12px !important;

        border: 1px solid #7B2CBF !important;

        box-shadow:
            0 0 10px rgba(123, 44, 191, 0.3) !important;
    }

    /* SELECT BOXES */
    .stSelectbox div[data-baseweb="select"] {

        border-radius: 12px !important;

        border: 1px solid #7B2CBF !important;

        box-shadow:
            0 0 10px rgba(123, 44, 191, 0.3) !important;
    }

    /* RADIO BUTTONS */
    div[role="radiogroup"] {

        padding: 10px;

        border-radius: 15px;

        border: 1px solid rgba(123, 44, 191, 0.4);

        box-shadow:
            0 0 10px rgba(123, 44, 191, 0.2);
    }

    /* CONTAINERS */
    div[data-testid="stVerticalBlock"] {

        border-radius: 20px !important;
    }

    </style>
    """, unsafe_allow_html=True)