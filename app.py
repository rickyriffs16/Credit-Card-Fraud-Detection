"""
app.py — Main Entry Point for Fraud Detection System
Handles: Authentication UI, Session Management, Page Navigation.
Styled with Bonsai-inspired clean SaaS UI.
"""

import streamlit as st
from datetime import datetime
import sys
import os
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))

from src.auth import (
    init_database, login_user, register_user,
    check_session_timeout, log_activity, get_user_settings,
    get_user_by_id
)

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Initialize Database
# ---------------------------------------------------------------------------
init_database()

# ---------------------------------------------------------------------------
# Bonsai-Inspired CSS — Clean Light Theme
# ---------------------------------------------------------------------------
def inject_bonsai_css():
    st.markdown("""
    <style>
        /* ===== Google Font ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ===== Global ===== */
        html, body, [class*="css"] {
            font-family: 'Inter', system-ui, sans-serif;
        }

        /* ===== Light Background ===== */
        .stApp {
            background-color: #F3F4F6 !important;
        }

        /* ===== Hide Streamlit defaults (keep sidebar toggle visible) ===== */
        #MainMenu {display: none !important;}
        footer {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        [data-testid="stDecoration"] {display: none !important;}
        [data-testid="stStatusWidget"] {display: none !important;}

        /* Header: minimal but visible for sidebar toggle */
        header[data-testid="stHeader"] {
            background: transparent !important;
            border: none !important;
            height: 2.5rem !important;
            min-height: 2.5rem !important;
        }

        /* Reduce default top padding on main content */
        .stMainBlockContainer,
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 2rem !important;
        }

        /* ===== Sidebar — Bonsai Collapsible ===== */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E5E7EB !important;
            transition: margin-left 0.3s ease, transform 0.3s ease !important;
        }

        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 260px !important;
            width: 260px !important;
        }

        /* Hide Streamlit's native toggle buttons - we use custom JS button */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }

        /* Custom toggle button (injected via JS) */
        #bonsai-sidebar-toggle {
            position: fixed !important;
            left: 14px !important;
            top: 14px !important;
            z-index: 999999 !important;
            background: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 8px !important;
            width: 38px !important;
            height: 38px !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
            font-size: 16px !important;
            color: #4B5563 !important;
            transition: all 0.2s ease !important;
        }

        #bonsai-sidebar-toggle:hover {
            background: #F9FAFB !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08) !important;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdown"] {
            color: #111111;
        }

        /* Hide the collapsed radio label ('nav') */
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
            display: none !important;
        }

        /* ===== Sidebar Nav Links ===== */
        [data-testid="stSidebar"] [data-testid="stRadio"] > div {
            gap: 4px !important;
            padding: 0 !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] > label {
            display: flex !important;
            width: 100% !important;
            box-sizing: border-box !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            margin: 2px 0 !important;
            cursor: pointer !important;
            transition: all 0.15s ease !important;
            background: transparent !important;
            border: none !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background-color: #F9FAFB !important;
        }

        /* Active State: Full width green pill */
        [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
            background-color: #EAF7EE !important;
        }

        /* Radio circle removal */
        [data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"],
        [data-testid="stSidebar"] div[role="radiogroup"] label > div > div:first-child,
        [data-testid="stSidebar"] div[role="radiogroup"] label div:has(input[type="radio"]),
        [data-testid="stSidebar"] div[role="radiogroup"] label div[data-baseweb="radio"],
        [data-testid="stSidebar"] .stRadio > div > label > div:first-child {
            display: none !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label > div {
            display: flex !important;
            align-items: center !important;
            width: 100% !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
            width: 100% !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label p {
            font-size: 14px !important;
            font-weight: 500 !important;
            color: #4B5563 !important;
            -webkit-text-fill-color: #4B5563 !important;
            display: flex !important;
            align-items: center !important;
            width: 100% !important;
            margin: 0 !important;
            font-family: 'Inter', system-ui, sans-serif !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
            color: #16A34A !important;
            -webkit-text-fill-color: #16A34A !important;
            font-weight: 600 !important;
        }

        /* SVG Vector Icon Before Each Sidebar Nav Item */
        [data-testid="stSidebar"] [data-testid="stRadio"] label p::before {
            content: '' !important;
            display: inline-block !important;
            width: 18px !important;
            height: 18px !important;
            margin-right: 12px !important;
            flex-shrink: 0 !important;
            background-color: transparent !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
            background-size: contain !important;
        }

        /* 1. Dashboard — Home icon */
        [data-testid="stSidebar"] label[data-nav="Dashboard"] p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%234B5563'%3E%3Cpath d='M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z'/%3E%3C/svg%3E") !important;
        }
        [data-testid="stSidebar"] label[data-nav="Dashboard"]:has(input:checked) p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2316A34A'%3E%3Cpath d='M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z'/%3E%3C/svg%3E") !important;
        }

        /* 2. Dataset — Database cylinder icon */
        [data-testid="stSidebar"] label[data-nav="Dataset"] p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cellipse cx='12' cy='5' rx='9' ry='3'/%3E%3Cpath d='M21 12c0 1.66-4 3-9 3s-9-1.34-9-3'/%3E%3Cpath d='M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5'/%3E%3C/svg%3E") !important;
        }
        [data-testid="stSidebar"] label[data-nav="Dataset"]:has(input:checked) p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2316A34A' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cellipse cx='12' cy='5' rx='9' ry='3'/%3E%3Cpath d='M21 12c0 1.66-4 3-9 3s-9-1.34-9-3'/%3E%3Cpath d='M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5'/%3E%3C/svg%3E") !important;
        }

        /* 3. Models — 3D Cube icon */
        [data-testid="stSidebar"] label[data-nav="Models"] p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z'/%3E%3Cpolyline points='3.27 6.96 12 12.01 20.73 6.96'/%3E%3Cline x1='12' y1='22.08' x2='12' y2='12'/%3E%3C/svg%3E") !important;
        }
        [data-testid="stSidebar"] label[data-nav="Models"]:has(input:checked) p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2316A34A' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z'/%3E%3Cpolyline points='3.27 6.96 12 12.01 20.73 6.96'/%3E%3Cline x1='12' y1='22.08' x2='12' y2='12'/%3E%3C/svg%3E") !important;
        }

        /* 4. Predictor — Play triangle icon */
        [data-testid="stSidebar"] label[data-nav="Predictor"] p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolygon points='5 3 19 12 5 21 5 3'/%3E%3C/svg%3E") !important;
        }
        [data-testid="stSidebar"] label[data-nav="Predictor"]:has(input:checked) p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2316A34A' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolygon points='5 3 19 12 5 21 5 3'/%3E%3C/svg%3E") !important;
        }

        /* 5. Profile — User icon */
        [data-testid="stSidebar"] label[data-nav="Profile"] p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E") !important;
        }
        [data-testid="stSidebar"] label[data-nav="Profile"]:has(input:checked) p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2316A34A' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E") !important;
        }

        /* 6. Settings — Gear icon */
        [data-testid="stSidebar"] label[data-nav="Settings"] p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3Cpath d='M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z'/%3E%3C/svg%3E") !important;
        }
        [data-testid="stSidebar"] label[data-nav="Settings"]:has(input:checked) p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2316A34A' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3Cpath d='M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z'/%3E%3C/svg%3E") !important;
        }

        /* 7. Reports — Document icon */
        [data-testid="stSidebar"] label[data-nav="Reports"] p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/%3E%3Cpolyline points='14 2 14 8 20 8'/%3E%3Cline x1='16' y1='13' x2='8' y2='13'/%3E%3Cline x1='16' y1='17' x2='8' y2='17'/%3E%3Cpolyline points='10 9 9 9 8 9'/%3E%3C/svg%3E") !important;
        }
        [data-testid="stSidebar"] label[data-nav="Reports"]:has(input:checked) p::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2316A34A' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/%3E%3Cpolyline points='14 2 14 8 20 8'/%3E%3Cline x1='16' y1='13' x2='8' y2='13'/%3E%3Cline x1='16' y1='17' x2='8' y2='17'/%3E%3Cpolyline points='10 9 9 9 8 9'/%3E%3C/svg%3E") !important;
        }

        /* Sidebar Logout button styling */
        [data-testid="stSidebar"] .stButton > button {
            background-color: #16A34A !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 20px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            width: 100% !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
            transition: all 0.15s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 8px !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #15803D !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        }

        /* ===== Form Container (White Card with Subtle Border and Shadow) ===== */
        [data-testid="stForm"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 14px !important;
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.02) !important;
            padding: 32px 36px 32px 36px !important;
        }

        /* ===== Input Styling & Rounded Fields ===== */
        [data-testid="stTextInputRootElement"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 8px !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
            overflow: hidden !important;
        }

        [data-testid="stTextInputRootElement"]:focus-within {
            border-color: #16A34A !important;
            box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.12) !important;
        }

        [data-testid="stTextInputRootElement"] input {
            background-color: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            padding: 11px 14px !important;
            font-size: 14px !important;
            box-shadow: none !important;
            outline: none !important;
            font-family: 'Inter', system-ui, sans-serif !important;
        }

        [data-testid="stTextInputRootElement"] input::placeholder {
            color: #9CA3AF !important;
            -webkit-text-fill-color: #9CA3AF !important;
            opacity: 1 !important;
        }

        /* Password Visibility Toggle with vertical separator line */
        [data-testid="stTextInputRootElement"] button {
            border: none !important;
            border-left: 1px solid #E5E7EB !important;
            background: transparent !important;
            color: #4B5563 !important;
            border-radius: 0 !important;
            width: 44px !important;
            padding: 0 !important;
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
            transition: background-color 0.15s ease, color 0.15s ease !important;
        }

        [data-testid="stTextInputRootElement"] button:hover {
            background-color: #F9FAFB !important;
            color: #111827 !important;
            transform: none !important;
        }

        .stSelectbox > div > div, [data-testid="stSelectbox"] > div > div {
            background-color: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 8px !important;
            color: #111111 !important;
        }

        /* Remove searchable input from selectbox — make it a simple dropdown */
        [data-baseweb="select"] input {
            caret-color: transparent !important;
            color: transparent !important;
            width: 1px !important;
            min-width: 1px !important;
            padding: 0 !important;
            cursor: pointer !important;
        }

        [data-baseweb="select"],
        [data-baseweb="select"] * {
            cursor: pointer !important;
        }

        /* ===== Label Styling ===== */
        .stTextInput > label,
        .stSelectbox > label,
        [data-testid="stWidgetLabel"] label,
        [data-testid="stWidgetLabel"] p {
            color: #1F2937 !important;
            -webkit-text-fill-color: #1F2937 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            margin-bottom: 6px !important;
            font-family: 'Inter', system-ui, sans-serif !important;
        }

        /* Email * label green accent */
        [data-testid="stTextInput"]:has(input[aria-label*="Email"]) label p,
        [data-testid="stTextInput"]:has(input[aria-label*="Email"]) label {
            color: #16A34A !important;
            -webkit-text-fill-color: #16A34A !important;
            font-weight: 600 !important;
        }

        /* ===== ALL Primary Green Buttons ===== */
        .stButton > button,
        .stFormSubmitButton > button,
        [data-testid="stFormSubmitButton"] > button,
        button[kind="primaryFormSubmit"],
        button[kind="primary"] {
            width: 100%;
            background-color: #16A34A !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            letter-spacing: 0.3px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.15s ease !important;
            -webkit-text-fill-color: white !important;
            cursor: pointer !important;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover,
        [data-testid="stFormSubmitButton"] > button:hover {
            background-color: #15803D !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
            color: white !important;
        }

        .stButton > button:active,
        .stFormSubmitButton > button:active,
        [data-testid="stFormSubmitButton"] > button:active {
            transform: translateY(0px) !important;
        }

        /* ===== Tabs Styling (Underline Indicators) ===== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 28px !important;
            background-color: transparent !important;
            border-radius: 0px !important;
            padding: 0px !important;
            border: none !important;
            border-bottom: 1px solid #E5E7EB !important;
            justify-content: flex-start !important;
            margin-bottom: 24px !important;
            width: 100% !important;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 0px !important;
            color: #4B5563 !important;
            -webkit-text-fill-color: #4B5563 !important;
            font-weight: 500 !important;
            padding: 8px 2px 12px 2px !important;
            font-size: 15px !important;
            background-color: transparent !important;
            border: none !important;
            border-bottom: 3px solid transparent !important;
            margin-bottom: -1px !important;
            transition: color 0.15s ease, border-color 0.15s ease !important;
            cursor: pointer !important;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            background-color: transparent !important;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: transparent !important;
            color: #16A34A !important;
            -webkit-text-fill-color: #16A34A !important;
            font-weight: 600 !important;
            border-bottom: 3px solid #16A34A !important;
        }

        /* Tab bottom indicator — hide baseweb default */
        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }

        /* ===== Hide 'Press Enter to submit' ===== */
        [data-testid="stForm"] small,
        [data-testid="InputInstructions"],
        .st-emotion-cache-1n76uvr {
            display: none !important;
        }

        /* ===== Metric cards override ===== */
        [data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 16px 20px;
        }
    </style>
    """, unsafe_allow_html=True)



# ---------------------------------------------------------------------------
# Sidebar Toggle (only for authenticated pages)
# ---------------------------------------------------------------------------
def inject_sidebar_toggle(user_id: int = 0):
    import streamlit.components.v1 as components
    components.html("""
    <script>
    (function() {
        var parent = window.parent.document;
        if (parent.getElementById('bonsai-sidebar-toggle')) return;

        function createToggle() {
            var btn = parent.createElement('div');
            btn.id = 'bonsai-sidebar-toggle';
            btn.innerHTML = '&#9776;';
            btn.title = 'Toggle sidebar';
            parent.body.appendChild(btn);

            var appView = parent.querySelector('[data-testid="stAppViewContainer"]');
            if (appView) appView.style.transition = 'margin-left 0.3s ease';
            var mainBlock = parent.querySelector('.main');
            if (mainBlock) mainBlock.style.transition = 'margin-left 0.3s ease';

            btn.addEventListener('click', function() {
                var sidebar = parent.querySelector('[data-testid="stSidebar"]');
                if (!sidebar) return;

                var expanded = sidebar.getAttribute('aria-expanded');
                if (expanded === 'true') {
                    sidebar.setAttribute('aria-expanded', 'false');
                    sidebar.style.marginLeft = '-260px';
                    sidebar.style.transform = 'translateX(-260px)';
                    sidebar.style.width = '260px';
                    sidebar.style.minWidth = '260px';
                    btn.innerHTML = '&#9776;';
                    if (appView) appView.style.marginLeft = '0px';
                    if (mainBlock) mainBlock.style.marginLeft = '0px';
                } else {
                    sidebar.setAttribute('aria-expanded', 'true');
                    sidebar.style.marginLeft = '0px';
                    sidebar.style.transform = 'translateX(0)';
                    sidebar.style.width = '260px';
                    sidebar.style.minWidth = '260px';
                    btn.innerHTML = '&#10005;';
                    if (appView) appView.style.marginLeft = '';
                    if (mainBlock) mainBlock.style.marginLeft = '';
                }
            });

            var sidebar = parent.querySelector('[data-testid="stSidebar"]');
            if (sidebar && sidebar.getAttribute('aria-expanded') === 'true') {
                btn.innerHTML = '&#10005;';
            }
        }

        // Tag each sidebar nav label with data-nav attribute from its text content
        function tagNavLabels() {
            var sidebar = parent.querySelector('[data-testid="stSidebar"]');
            if (!sidebar) return;
            var labels = sidebar.querySelectorAll('[data-testid="stRadio"] label');
            labels.forEach(function(label) {
                var p = label.querySelector('p');
                if (p) {
                    var text = p.textContent.trim();
                    if (text) label.setAttribute('data-nav', text);
                }
            });
        }

        // Session persistence via localStorage
        (function persistSession() {
            var uid = """ + str(user_id) + """;
            if (uid && uid !== '0') {
                window.parent.localStorage.setItem('ccfd_uid', uid);
            }
        })();

        setTimeout(createToggle, 800);
        // Run on load and then periodically to handle Streamlit re-renders
        setTimeout(tagNavLabels, 1000);
        setInterval(tagNavLabels, 1500);
    })();
    </script>
    """, height=0)


# ---------------------------------------------------------------------------
# Session Persistence via localStorage (parent-frame bridge)
# ---------------------------------------------------------------------------
def inject_cookie_session():
    """When unauthenticated: read ccfd_uid from localStorage via parent frame and reload with it as query param."""
    import streamlit.components.v1 as components
    components.html("""
    <script>
    (function() {
        // This iframe shares origin with parent (same localhost:8501)
        // so we CAN access window.parent.localStorage
        try {
            var uid = window.parent.localStorage.getItem('ccfd_uid');
            if (uid && uid !== '0') {
                var url = new URL(window.parent.location.href);
                if (!url.searchParams.get('ccfd_uid')) {
                    url.searchParams.set('ccfd_uid', uid);
                    window.parent.history.replaceState({}, '', url.toString());
                    window.parent.location.reload();
                }
            }
        } catch(e) { console.warn('Session restore failed:', e); }
    })();
    </script>
    """, height=0)


def write_session_cookie(user_id: int):
    """No-op: session is written by inject_sidebar_toggle via localStorage."""
    pass


def clear_session_cookie():
    """Clear session from localStorage via component iframe."""
    import streamlit.components.v1 as components
    components.html("""
    <script>
    (function() {
        try {
            window.parent.localStorage.removeItem('ccfd_uid');
            var url = new URL(window.parent.location.href);
            url.searchParams.delete('ccfd_uid');
            window.parent.history.replaceState({}, '', url.toString());
        } catch(e) {}
    })();
    </script>
    """, height=0)


# ---------------------------------------------------------------------------
# Session State
# ---------------------------------------------------------------------------
def init_session_state():
    defaults = {
        "authenticated": False,
        "user": None,
        "last_activity": None,
        "current_page": "Dashboard",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # --- Restore session from cookie (via query param bridge) ---
    if not st.session_state["authenticated"]:
        uid_str = st.query_params.get("ccfd_uid")
        if uid_str:
            try:
                user = get_user_by_id(int(uid_str))
                if user:
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = user
                    st.session_state["last_activity"] = datetime.now()
                    # Clean the param from URL without triggering reload
                    st.query_params.clear()
            except (ValueError, TypeError):
                pass


# ---------------------------------------------------------------------------
# Auth Screen — Clean Reference Redesign
# ---------------------------------------------------------------------------
def render_auth_screen():
    # Subtle top spacing and center column layout
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    _, col_center, _ = st.columns([1, 1.25, 1])

    with col_center:
        tab_login, tab_register = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                # Clean minimal typography heading matching reference image
                st.markdown(
                    '<div style="font-size: 32px; font-weight: 600; color: #111827; margin: 4px 0 24px 0; '
                    'letter-spacing: -0.5px; font-family: \'Inter\', system-ui, sans-serif;">Login</div>',
                    unsafe_allow_html=True
                )

                login_user_input = st.text_input(
                    "Email *", placeholder="example@site.com", key="login_username"
                )
                st.markdown(
                    '<div style="font-size: 12px; color: #6B7280; margin-top: -8px; margin-bottom: 20px; '
                    'font-family: \'Inter\', system-ui, sans-serif;">Use the following format: example@site.com</div>',
                    unsafe_allow_html=True
                )

                login_pass_input = st.text_input(
                    "Password *", placeholder="Enter your password",
                    type="password", key="login_password"
                )

                st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

                col_forgot, col_submit = st.columns([1.35, 1])
                with col_forgot:
                    st.markdown(
                        '<div style="display: flex; align-items: center; height: 100%; min-height: 44px;">'
                        '<a href="?action=forgot_password" target="_self" '
                        'style="color: #16A34A; text-decoration: underline; font-size: 14px; font-weight: 500; cursor: pointer;">'
                        'Forgot your password?</a></div>',
                        unsafe_allow_html=True
                    )
                with col_submit:
                    login_submitted = st.form_submit_button("LOGIN", use_container_width=True)

            # "Forgot your password?" recovery assistance info (on Sign In page only)
            if st.query_params.get("action") == "forgot_password":
                st.markdown("""
                <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; 
                            padding: 16px 20px; margin-top: 16px; font-size: 13px; color: #166534;">
                    <div style="font-weight: 600; font-size: 14px; margin-bottom: 6px;">Password Recovery Assistance</div>
                    <div>Default administrator account: <strong>admin</strong> / <strong>admin123</strong></div>
                    <div style="margin-top: 4px; color: #374151;">If you are an analyst or forgot your personal password, please contact the system administrator to reset your credentials.</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Close Notice", key="close_forgot_notice", use_container_width=True):
                    st.query_params.clear()
                    st.rerun()

            if login_submitted:
                result = login_user(login_user_input, login_pass_input)
                if result["success"]:
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = result["user"]
                    st.session_state["last_activity"] = datetime.now()
                    log_activity(result["user"]["id"], "Login")
                    write_session_cookie(result["user"]["id"])
                    st.rerun()
                else:
                    st.markdown(
                        f'<div style="background: #FEF2F2; border: 1px solid #FECACA; border-radius: 8px; '
                        f'padding: 12px 16px; color: #DC2626; font-size: 13px; font-weight: 500; '
                        f'text-align: center; margin-top: 14px;">⚠️ {result["message"]}</div>',
                        unsafe_allow_html=True
                    )

        with tab_register:
            with st.form("register_form", clear_on_submit=False):
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                reg_name = st.text_input(
                    "Full Name", placeholder="Enter your full name", key="reg_name"
                )
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                reg_user = st.text_input(
                    "Username", placeholder="Choose a username", key="reg_username"
                )
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                reg_pass = st.text_input(
                    "Password", placeholder="Min 6 characters",
                    type="password", key="reg_password"
                )
                st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
                reg_submitted = st.form_submit_button("Create Account", use_container_width=True)

            if reg_submitted:
                # Default all new open registrations to 'Analyst'
                result = register_user(reg_name, reg_user, reg_pass, "Analyst")
                if result["success"]:
                    st.markdown(
                        f'<div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; '
                        f'padding: 12px 16px; color: #16A34A; font-size: 13px; font-weight: 500; '
                        f'text-align: center; margin-top: 14px;">✓ {result["message"]} You can now sign in.</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div style="background: #FEF2F2; border: 1px solid #FECACA; border-radius: 8px; '
                        f'padding: 12px 16px; color: #DC2626; font-size: 13px; font-weight: 500; '
                        f'text-align: center; margin-top: 14px;">⚠️ {result["message"]}</div>',
                        unsafe_allow_html=True
                    )


# ---------------------------------------------------------------------------
# Sidebar — Clean Reference Redesign
# ---------------------------------------------------------------------------
def render_sidebar():
    user = st.session_state["user"]

    with st.sidebar:
        # Brand
        st.markdown("""
        <div style="padding: 16px 12px 24px 12px;">
            <div style="font-size: 15px; font-weight: 700; color: #111111; letter-spacing: -0.3px; line-height: 1.3;">
                Credit Card Fraud Detection
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        pages = [
            "Dashboard",
            "Dataset",
            "Models",
            "Predictor",
            "Profile",
            "Settings",
            "Reports"
        ]

        selected = st.radio(
            "nav",
            pages,
            index=pages.index(st.session_state['current_page']) if st.session_state['current_page'] in pages else 0,
            label_visibility="collapsed",
            key="nav_radio"
        )

        st.session_state["current_page"] = selected

        st.markdown("<div style='height: 120px'></div>", unsafe_allow_html=True)

        # Logout
        if st.button("[→  Logout", use_container_width=True, key="logout_btn"):
            log_activity(user["id"], "Logout")
            st.session_state["authenticated"] = False
            st.session_state["user"] = None
            st.session_state["last_activity"] = None
            clear_session_cookie()
            st.rerun()


# ---------------------------------------------------------------------------
# Dashboard — Full Data-Driven Page
# ---------------------------------------------------------------------------
def render_dashboard():
    import json
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go

    user = st.session_state["user"]
    st.session_state["last_activity"] = datetime.now()

    # --- Header ---
    st.markdown("""
    <div style="padding: 0 0 20px 0;">
        <h1 style="font-size: 30px; font-weight: 800; color: #111111; margin: 0 0 4px 0; letter-spacing: -0.5px;">
            Dashboard
        </h1>
        <p style="font-size: 14px; color: #6B7280; margin: 0;">
            Welcome back! Here's your system overview.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Load data ---
    DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "sample_data.csv")
    METRICS_PATH = os.path.join(os.path.dirname(__file__), "models", "model_metrics.json")

    has_data = os.path.exists(DATA_PATH)
    has_metrics = os.path.exists(METRICS_PATH)

    df = None
    metrics = None

    if has_data:
        df = pd.read_csv(DATA_PATH)
    if has_metrics:
        with open(METRICS_PATH, "r") as f:
            metrics = json.load(f)

    # --- KPI Cards Template Matching Reference Image ---
    def render_kpi(badge_bg, badge_svg, label, value, value_color, sub):
        return f"""
        <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px;
                    padding: 18px 20px; display: flex; align-items: center; gap: 16px;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03); min-height: 96px;">
            <div style="width: 44px; height: 44px; border-radius: 50%; background: {badge_bg};
                        display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                {badge_svg}
            </div>
            <div style="flex: 1; min-width: 0;">
                <div style="font-size: 11px; font-weight: 700; color: #374151; text-transform: uppercase;
                            letter-spacing: 0.6px; margin-bottom: 2px;">{label}</div>
                <div style="font-size: 24px; font-weight: 700; color: {value_color}; line-height: 1.2;
                            margin-bottom: 2px;">{value}</div>
                <div style="font-size: 12px; color: #6B7280;">{sub}</div>
            </div>
        </div>
        """

    svg_txn = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><line x1="10" y1="9" x2="8" y2="9"></line></svg>"""
    svg_shield = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>"""
    svg_chart = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>"""
    svg_trend = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg>"""

    if df is not None and metrics is not None:
        total_txn = len(df)
        fraud_count = int(df["Class"].sum())
        legit_count = total_txn - fraud_count
        fraud_rate = (fraud_count / total_txn * 100) if total_txn > 0 else 0
        avg_amount = df["Amount"].mean()

        best_model = metrics.get("_metadata", {}).get("best_model", "Random Forest")
        best_metrics = metrics.get(best_model, {})
        accuracy = best_metrics.get("accuracy", 0)
        f1 = best_metrics.get("f1_score", 0)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(render_kpi("#EAF7EE", svg_txn, "TRANSACTIONS", f"{total_txn:,}", "#111111", "In dataset"), unsafe_allow_html=True)
        with col2:
            st.markdown(render_kpi("#FEE2E2", svg_shield, "FRAUD BLOCKED", f"{fraud_count}", "#DC2626", f"{fraud_rate:.1f}% of total"), unsafe_allow_html=True)
        with col3:
            st.markdown(render_kpi("#EAF7EE", svg_chart, "ACCURACY", f"{accuracy:.1f}%", "#16A34A", f"Best: {best_model}"), unsafe_allow_html=True)
        with col4:
            st.markdown(render_kpi("#FEF3C7", svg_trend, "F1 SCORE", f"{f1:.1f}%", "#D97706", f"{best_model}"), unsafe_allow_html=True)
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(render_kpi("#EAF7EE", svg_txn, "TRANSACTIONS", "--", "#111111", "No data loaded"), unsafe_allow_html=True)
        with col2:
            st.markdown(render_kpi("#FEE2E2", svg_shield, "FRAUD BLOCKED", "--", "#DC2626", "Awaiting analysis"), unsafe_allow_html=True)
        with col3:
            st.markdown(render_kpi("#EAF7EE", svg_chart, "ACCURACY", "--", "#16A34A", "Train model first"), unsafe_allow_html=True)
        with col4:
            st.markdown(render_kpi("#FEF3C7", svg_trend, "F1 SCORE", "--", "#D97706", "No data yet"), unsafe_allow_html=True)

    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

    # --- Charts Section ---
    if df is not None:
        chart_col1, chart_col2 = st.columns([2, 1])

        with chart_col1:
            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 20px;">
                <div style="font-size: 16px; font-weight: 600; color: #111111; margin-bottom: 4px;">
                    Transaction Volume Over Time
                </div>
                <div style="font-size: 12px; color: #6B6B6B; margin-bottom: 12px;">
                    Distribution of transactions across time periods
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Create time bins
            df_chart = df.copy()
            df_chart["Time_Hour"] = (df_chart["Time"] / 3600).astype(int)
            time_dist = df_chart.groupby(["Time_Hour", "Class"]).size().reset_index(name="Count")
            time_dist["Label"] = time_dist["Class"].map({0: "Legitimate", 1: "Fraud"})

            fig_line = px.area(
                time_dist, x="Time_Hour", y="Count", color="Label",
                color_discrete_map={"Legitimate": "rgba(22,163,74,0.5)", "Fraud": "rgba(220,38,38,0.5)"},
                labels={"Time_Hour": "Hour", "Count": "Transactions"}
            )
            fig_line.update_layout(
                plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                font=dict(family="Inter, sans-serif", color="#6B6B6B", size=12),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=40, r=10, t=10, b=40),
                height=300,
                xaxis=dict(gridcolor="#F5F5F5", title="Hour", showline=False),
                yaxis=dict(gridcolor="#F5F5F5", title="Count", showline=False)
            )
            st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})

        with chart_col2:
            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 20px;">
                <div style="font-size: 16px; font-weight: 600; color: #111111; margin-bottom: 4px;">
                    Fraud Distribution
                </div>
                <div style="font-size: 12px; color: #6B6B6B; margin-bottom: 12px;">
                    Class imbalance overview
                </div>
            </div>
            """, unsafe_allow_html=True)

            fraud_counts = df["Class"].value_counts().reset_index()
            fraud_counts.columns = ["Class", "Count"]
            fraud_counts["Label"] = fraud_counts["Class"].map({0: "Legitimate", 1: "Fraud"})

            fig_donut = px.pie(
                fraud_counts, values="Count", names="Label",
                color="Label",
                color_discrete_map={"Legitimate": "#22C55E", "Fraud": "#EF4444"},
                hole=0.6
            )
            fig_donut.update_traces(textposition="outside", textinfo="label+percent",
                                     marker=dict(line=dict(color='#FFFFFF', width=2)))
            fig_donut.update_layout(
                plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                font=dict(family="Inter, sans-serif", color="#6B6B6B", size=12),
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10),
                height=300
            )
            st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})

        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

        # --- Hourly Fraud Bar Chart ---
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 20px;">
            <div style="font-size: 16px; font-weight: 600; color: #111111; margin-bottom: 4px;">
                Fraud vs Legitimate by Hour
            </div>
            <div style="font-size: 12px; color: #6B6B6B; margin-bottom: 12px;">
                Hourly comparison of transaction types
            </div>
        </div>
        """, unsafe_allow_html=True)

        hourly = df_chart.groupby(["Time_Hour", "Class"]).size().reset_index(name="Count")
        hourly["Label"] = hourly["Class"].map({0: "Legitimate", 1: "Fraud"})

        fig_bar = px.bar(
            hourly, x="Time_Hour", y="Count", color="Label",
            barmode="group",
            color_discrete_map={"Legitimate": "rgba(22,163,74,0.7)", "Fraud": "rgba(220,38,38,0.7)"},
            labels={"Time_Hour": "Hour", "Count": "Transactions"}
        )
        fig_bar.update_layout(
            plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
            font=dict(family="Inter, sans-serif", color="#6B6B6B", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=10, t=10, b=40),
            height=280,
            xaxis=dict(gridcolor="#F5F5F5", showline=False),
            yaxis=dict(gridcolor="#F5F5F5", showline=False),
            bargap=0.3
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

        # --- Data Feed Table ---
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 20px;">
            <div style="font-size: 16px; font-weight: 600; color: #111111; margin-bottom: 4px;">
                Transaction Feed
            </div>
            <div style="font-size: 12px; color: #6B6B6B; margin-bottom: 12px;">
                Recent transactions with fraud indicators
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Filters
        filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])

        with filter_col1:
            search_term = st.text_input("Search by amount", placeholder="e.g. 150.00", key="dash_search")
        with filter_col2:
            class_filter = st.selectbox("Class", ["All", "Fraud", "Legitimate"], key="dash_class_filter")
        with filter_col3:
            n_rows = st.selectbox("Show rows", [25, 50, 100, 200], index=0, key="dash_n_rows")

        display_df = df[["Time", "Amount", "Class"]].copy()
        display_df["Status"] = display_df["Class"].map({0: "Legitimate", 1: "Fraud"})
        display_df["Time_Formatted"] = (display_df["Time"] / 3600).round(1).astype(str) + "h"
        display_df["Amount"] = display_df["Amount"].round(2)
        display_df = display_df[["Time_Formatted", "Amount", "Status"]]
        display_df.columns = ["Time", "Amount ($)", "Status"]

        if class_filter == "Fraud":
            display_df = display_df[display_df["Status"] == "Fraud"]
        elif class_filter == "Legitimate":
            display_df = display_df[display_df["Status"] == "Legitimate"]

        if search_term:
            try:
                amt = float(search_term)
                display_df = display_df[display_df["Amount ($)"].between(amt - 10, amt + 10)]
            except ValueError:
                pass

        st.dataframe(
            display_df.head(n_rows),
            use_container_width=True,
            height=400,
            column_config={
                "Time": st.column_config.TextColumn("Time", width="small"),
                "Amount ($)": st.column_config.NumberColumn("Amount ($)", format="$%.2f", width="medium"),
                "Status": st.column_config.TextColumn("Status", width="small")
            }
        )

        st.markdown(f"""
        <div style="font-size: 12px; color: #9CA3AF; margin-top: 8px; text-align: right;">
            Showing {min(n_rows, len(display_df))} of {len(display_df)} transactions
        </div>
        """, unsafe_allow_html=True)

    else:
        # No data state — System Standing By card matching reference image
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px;
                    padding: 56px 32px; text-align: center; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
                    margin-top: 10px;">
            <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
                <svg width="74" height="64" viewBox="0 0 74 64" fill="none">
                    <!-- Left radiating green rays -->
                    <line x1="10" y1="26" x2="18" y2="28" stroke="#86EFAC" stroke-width="2.5" stroke-linecap="round" />
                    <line x1="10" y1="38" x2="18" y2="36" stroke="#86EFAC" stroke-width="2.5" stroke-linecap="round" />
                    <!-- Right radiating green rays -->
                    <line x1="64" y1="26" x2="56" y2="28" stroke="#86EFAC" stroke-width="2.5" stroke-linecap="round" />
                    <line x1="64" y1="38" x2="56" y2="36" stroke="#86EFAC" stroke-width="2.5" stroke-linecap="round" />
                    <!-- Main rounded terminal card -->
                    <rect x="23" y="10" width="28" height="44" rx="8" stroke="#9CA3AF" stroke-width="2.5" fill="#FFFFFF" />
                    <!-- Terminal inner lines -->
                    <circle cx="29" cy="24" r="1.5" fill="#9CA3AF" />
                    <line x1="34" y1="24" x2="44" y2="24" stroke="#9CA3AF" stroke-width="2.5" stroke-linecap="round" />
                    <circle cx="29" cy="34" r="1.5" fill="#9CA3AF" />
                    <line x1="34" y1="34" x2="44" y2="34" stroke="#9CA3AF" stroke-width="2.5" stroke-linecap="round" />
                </svg>
            </div>
            <div style="font-size: 22px; font-weight: 700; color: #111111; margin-bottom: 8px; font-family: 'Inter', system-ui, sans-serif;">
                System Standing By
            </div>
            <div style="font-size: 14px; color: #6B7280; max-width: 520px; margin: 0 auto; line-height: 1.6; font-family: 'Inter', system-ui, sans-serif;">
                Navigate to <strong style="color: #16A34A; font-weight: 700;">Dataset</strong> to load your transaction data, or use the <strong style="color: #16A34A; font-weight: 700;">Predictor</strong> to test individual transactions.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Dataset Page — Upload, Preview, EDA
# ---------------------------------------------------------------------------
def render_dataset():
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from src.data_engine import load_dataset, validate_dataset

    st.session_state["last_activity"] = datetime.now()

    st.markdown("""
    <div style="padding: 8px 0 20px;">
        <h1 style="font-size: 28px; font-weight: 700; color: #111111; margin-bottom: 4px;">Dataset</h1>
        <p style="font-size: 14px; color: #6B6B6B; margin-top: 0;">Upload, preview, and explore your transaction data.</p>
    </div>
    """, unsafe_allow_html=True)

    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    DATA_PATH = os.path.join(DATA_DIR, "sample_data.csv")
    os.makedirs(DATA_DIR, exist_ok=True)

    # --- Upload Section ---
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 24px 28px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);">
        <div style="font-size: 16px; font-weight: 700; color: #111111; margin-bottom: 4px;">Upload Dataset</div>
        <div style="font-size: 13px; color: #6B7280;">Upload a CSV file with columns: Time, V1-V28, Amount, Class</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Choose a CSV file", type=["csv"], key="dataset_upload", label_visibility="collapsed")

    if uploaded is not None:
        df_uploaded = pd.read_csv(uploaded)
        df_uploaded.to_csv(DATA_PATH, index=False)
        st.markdown('<div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 12px 16px; color: #16A34A; font-size: 13px; font-weight: 500; margin-bottom: 16px;">✓ Dataset uploaded and saved successfully.</div>', unsafe_allow_html=True)

    # --- Load data ---
    if not os.path.exists(DATA_PATH):
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 48px 32px; text-align: center; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);">
            <div style="font-size: 18px; font-weight: 700; color: #111111; margin-bottom: 8px;">No Dataset Loaded</div>
            <div style="font-size: 14px; color: #6B7280;">Upload a CSV file above to get started.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    df = pd.read_csv(DATA_PATH)
    report = validate_dataset(df)

    # --- Validation Report ---
    status_color = "#16A34A" if report["valid"] else "#DC2626"
    status_text = "Valid" if report["valid"] else "Invalid"

    info_card = """
    <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px;
                padding: 16px 18px; height: 100px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <div style="font-size: 10px; color: #6B6B6B; text-transform: uppercase;
                    letter-spacing: 0.8px; font-weight: 600; white-space: nowrap;">{label}</div>
        <div style="font-size: 22px; font-weight: 700; color: {color}; margin-top: 6px;
                    white-space: nowrap;">{value}</div>
        <div style="font-size: 11px; color: #9CA3AF; margin-top: 3px;">{sub}</div>
    </div>
    """

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(info_card.format(label="Status", value=status_text, color=status_color, sub="Validation"), unsafe_allow_html=True)
    with c2:
        st.markdown(info_card.format(label="Rows", value=f"{report['total_rows']:,}", color="#111111", sub=f"{report['total_columns']} columns"), unsafe_allow_html=True)
    with c3:
        st.markdown(info_card.format(label="Fraud", value=f"{report['fraud_count']:,}", color="#DC2626", sub=f"{report['fraud_percentage']}%"), unsafe_allow_html=True)
    with c4:
        st.markdown(info_card.format(label="Legitimate", value=f"{report['legit_count']:,}", color="#16A34A", sub=f"{100 - report['fraud_percentage']:.1f}%"), unsafe_allow_html=True)
    with c5:
        st.markdown(info_card.format(label="Missing Values", value=f"{report['missing_values']}", color="#F59E0B" if report['missing_values'] > 0 else "#16A34A", sub="Null cells"), unsafe_allow_html=True)
    with c6:
        st.markdown(info_card.format(label="Duplicates", value=f"{report['duplicate_rows']}", color="#F59E0B" if report['duplicate_rows'] > 0 else "#16A34A", sub="Duplicate rows"), unsafe_allow_html=True)

    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

    # --- Charts Row ---
    chart_c1, chart_c2 = st.columns(2)

    with chart_c1:
        st.markdown('<div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);"><div style="font-size: 16px; font-weight: 600; color: #111111; margin-bottom: 4px;">Class Distribution</div><div style="font-size: 12px; color: #6B6B6B; margin-bottom: 12px;">Fraud vs Legitimate breakdown</div></div>', unsafe_allow_html=True)

        class_data = df["Class"].value_counts().reset_index()
        class_data.columns = ["Class", "Count"]
        class_data["Label"] = class_data["Class"].map({0: "Legitimate", 1: "Fraud"})

        fig_class = px.bar(
            class_data, x="Label", y="Count", color="Label",
            color_discrete_map={"Legitimate": "rgba(22,163,74,0.7)", "Fraud": "rgba(220,38,38,0.7)"},
            text="Count"
        )
        fig_class.update_layout(
            plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
            font=dict(family="Inter, sans-serif", color="#6B6B6B", size=12),
            showlegend=False, margin=dict(l=40, r=10, t=10, b=40), height=280,
            xaxis=dict(showline=False, gridcolor="#F5F5F5"),
            yaxis=dict(showline=False, gridcolor="#F5F5F5")
        )
        fig_class.update_traces(textposition="outside")
        st.plotly_chart(fig_class, use_container_width=True, config={'displayModeBar': False})

    with chart_c2:
        st.markdown('<div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);"><div style="font-size: 16px; font-weight: 600; color: #111111; margin-bottom: 4px;">Transaction Amount Distribution</div><div style="font-size: 12px; color: #6B6B6B; margin-bottom: 12px;">Amount spread across all transactions</div></div>', unsafe_allow_html=True)

        fig_amt = px.histogram(
            df, x="Amount", nbins=50,
            color_discrete_sequence=["rgba(22,163,74,0.5)"]
        )
        fig_amt.update_layout(
            plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
            font=dict(family="Inter, sans-serif", color="#6B6B6B", size=12),
            showlegend=False, margin=dict(l=40, r=10, t=10, b=40), height=280,
            xaxis=dict(title="Amount ($)", showline=False, gridcolor="#F5F5F5"),
            yaxis=dict(title="Frequency", showline=False, gridcolor="#F5F5F5")
        )
        st.plotly_chart(fig_amt, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

    # --- Statistical Summary ---
    st.markdown('<div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 20px;"><div style="font-size: 16px; font-weight: 600; color: #111111; margin-bottom: 4px;">Statistical Summary</div><div style="font-size: 12px; color: #6B6B6B; margin-bottom: 12px;">Key statistics for Amount and Time features</div></div>', unsafe_allow_html=True)

    stats_df = df[["Time", "Amount"]].describe().round(2).T
    stats_df.insert(0, "Feature", stats_df.index)
    stats_df = stats_df.reset_index(drop=True)
    st.dataframe(stats_df, use_container_width=True, height=120)

    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

    # --- Data Preview ---
    st.markdown('<div style="background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 12px; padding: 20px;"><div style="font-size: 16px; font-weight: 600; color: #111111; margin-bottom: 4px;">Data Preview</div><div style="font-size: 12px; color: #6B6B6B; margin-bottom: 12px;">First rows of the loaded dataset</div></div>', unsafe_allow_html=True)

    preview_rows = st.selectbox("Rows to show", [10, 25, 50, 100], index=0, key="ds_preview_rows")
    st.dataframe(df.head(preview_rows), use_container_width=True, height=400)

    st.markdown(f'<div style="font-size: 12px; color: #9CA3AF; margin-top: 8px; text-align: right;">Showing {min(preview_rows, len(df))} of {len(df):,} rows</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Page Placeholder (for pages not yet built)
# ---------------------------------------------------------------------------
def render_placeholder(page_name):
    st.markdown(f"""
    <div style="padding: 8px 0 24px;">
        <h1 style="font-size: 28px; font-weight: 700; color: #111111; margin-bottom: 4px;">
            {page_name}
        </h1>
        <p style="font-size: 14px; color: #6B6B6B;">
            This page will be built in the next phase.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E5E5E5;
                border-radius: 12px; padding: 48px; text-align: center;">
        <div style="font-size: 16px; color: #6B6B6B;">Coming soon</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Session Timeout
# ---------------------------------------------------------------------------
def check_timeout():
    if st.session_state["authenticated"]:
        if check_session_timeout(st.session_state.get("last_activity")):
            st.session_state["authenticated"] = False
            st.session_state["user"] = None
            st.warning("Session expired due to inactivity. Please log in again.")
            st.rerun()


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    inject_bonsai_css()
    init_session_state()

    if st.session_state["authenticated"]:
        check_timeout()
        render_sidebar()
        inject_sidebar_toggle(user_id=st.session_state["user"]["id"])

        page = st.session_state["current_page"]
        if page == "Dashboard":
            render_dashboard()
        elif page == "Dataset":
            render_dataset()
        elif page == "Models":
            from views.models_page import render_models
            render_models()
        elif page == "Predictor":
            from views.predictor_page import render_predictor
            render_predictor()
        elif page == "Profile":
            from views.profile_page import render_profile
            render_profile()
        elif page == "Settings":
            from views.settings_page import render_settings
            render_settings()
        elif page == "Reports":
            from views.reports_page import render_reports
            render_reports()
        else:
            render_placeholder(page)
    else:
        inject_cookie_session()
        render_auth_screen()


if __name__ == "__main__":
    main()
