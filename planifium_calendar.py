#!/usr/bin/env python3
import streamlit as st
from streamlit_calendar import calendar

from planifium_parser import get_full_data

st.sidebar.title("planifium_wetrying")
sigle = st.sidebar.text_input("Sigle du cours").upper()
session = st.sidebar.selectbox("Session", options=["H26", "A25", "E26"])

if sigle:
    data_calendar, tp_noms, th_noms = get_full_data(sigle, session)

    if data_calendar:
        with st.form("course_selection"):
            my_choice_tp = st.selectbox("Section de TP", options=tp_noms)
            my_choice_th = st.selectbox("Section de TH", options=th_noms)
            submit = st.form_submit_button("Générer l'horaire")

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

        calendar_events = []
        mapping_jours = {"Lu": 1, "Ma": 2, "Me": 3, "Je": 4, "Ve": 5, "Sa": 6, "Di": 0}

        for cours in data_calendar:
            if cours["section"] == my_choice_tp or cours["section"] == my_choice_th:
                calendar_events.append(
                    {
                        "title": f"{cours['section']} - {cours['type']}",
                        "startTime": cours["start_time"],
                        "endTime": cours["end_time"],
                        "startRecur": cours["start_date"],
                        "endRecur": cours["end_date"],
                        "daysOfWeek": [mapping_jours[cours["jour"]]],
                    }
                )

        mon_style = ".fc-event { font-size: 10px !important; }"

        calendar(events=calendar_events, options=calendar_options, custom_css=mon_style)

    else:
        st.warning("Aucun horaire existant")

else:
    st.info("Entrez un sigle pour commencer")
