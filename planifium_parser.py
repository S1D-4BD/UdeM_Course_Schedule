import requests

def get_full_data(cours, session):
    url = f"https://planifium-api.onrender.com/api/v1/courses/{cours}?include_schedule=true&schedule_semester={session}"
    
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            all_events = []
            sections_tp = []
            sections_th = []

            for schedule in data.get("schedules", []):
                for section in schedule.get("sections", []):
                    for volet in section["volets"]:
                        if volet["name"] == "TP":
                            if section["name"] not in sections_tp:
                                sections_tp.append(section["name"])
                        if volet["name"] == "TH":
                            if section["name"] not in sections_th:
                                sections_th.append(section["name"])
                        
                        for act in volet["activities"]:
                            for day in act["days"]:
                                all_events.append({
                                    "section": section["name"],
                                    "type": volet["name"],
                                    "jour": day,
                                    "start_time": act["start_time"],
                                    "end_time": act["end_time"],
                                    "start_date": act["start_date"],
                                    "end_date": act["end_date"],
                                })
            

            return all_events, sorted(sections_tp), sorted(sections_th)
    
    except Exception as e:
        print(f"Erreur lors du fetch : {e}")
        
    return [], [], []