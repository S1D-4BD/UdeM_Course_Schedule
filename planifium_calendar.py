#!/usr/bin/env python3

import streamlit as st
from streamlit_calendar import calendar

from planifium_parser import get_full_data

if "panier" not in st.session_state:
    st.session_state.panier = []

st.sidebar.title("planifium_wetrying")

sigle_input = st.sidebar.text_input("sigle du cours").upper()
session_input = st.sidebar.selectbox("session", options=["H26", "A25", "E26"])

if st.sidebar.button("ajouter au panier"):
    if sigle_input:
        with st.sidebar:
            with st.spinner("recherche..."):
                data, tps, ths = get_full_data(sigle_input, session_input)
                if data:
                    st.session_state.panier.append(
                        {"sigle": sigle_input, "data": data, "tps": tps, "ths": ths}
                    )
                    st.rerun()
                else:
                    st.error("cours introuvable")
    else:
        st.sidebar.warning("entrez un sigle")

calendar_options = {
    "initialView": "timeGridWeek",
    "slotMinTime": "08:00:00",
    "slotMaxTime": "22:00:00",
    "allDaySlot": False,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "timeGridWeek,timeGridDay",
    },
}
mon_style = ".fc-event { font-size: 10px !important; }"

calendar_events = []
mapping_jours = {"Lu": 1, "Ma": 2, "Me": 3, "Je": 4, "Ve": 5, "Sa": 6, "Di": 0}

if st.session_state.panier:
    for i, item in enumerate(st.session_state.panier):
        with st.expander(f"options pour {item['sigle']}", expanded=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                choix_tp = st.selectbox(
                    f"section tp", options=item["tps"], key=f"tp_{i}"
                )
            with col2:
                choix_th = st.selectbox(
                    f"section th", options=item["ths"], key=f"th_{i}"
                )
            with col3:
                st.write("")
                if st.button("supprimer", key=f"del_{i}"):
                    st.session_state.panier.pop(i)
                    st.rerun()

        for cours in item["data"]:
            if cours["section"] in [choix_tp, choix_th]:
                calendar_events.append(
                    {
                        "title": f"{item['sigle']} ({cours['type']})",
                        "startTime": cours["start_time"],
                        "endTime": cours["end_time"],
                        "startRecur": cours["start_date"],
                        "endRecur": cours["end_date"],
                        "daysOfWeek": [mapping_jours[cours["jour"]]],
                    }
                )

    calendar(events=calendar_events, options=calendar_options, custom_css=mon_style)
else:
    st.info("votre panier est vide entrez un sigle pour commencer")
