from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


RECITATION_HOURS = {"a": "09:00~09:50", "b": "10:00~10:50",
                    "c": "11:00~11:50", "d": "12:00~12:50"}
MICROSERVICE_LINK = "https://whos-my-ta.fly.dev/section_id/"


@app.get("/section_info/{section_id}")
def get_section_info(section_id: str):

    if section_id is None:
        raise HTTPException(status_code=404, detail="Missing section id")

    section_id = section_id.lower()

    response = requests.get(MICROSERVICE_LINK + section_id)
    data = response.json()

    ta_name_list = data["ta_names"]
    ta1_name = ta_name_list[0]["fname"] + " " + ta_name_list[0]["lname"]
    ta2_name = ta_name_list[1]["fname"] + " " + ta_name_list[1]["lname"]

    # Define recitation start and end times based on the section_id
    if section_id in RECITATION_HOURS:
        recitation_time = RECITATION_HOURS[section_id]
    else:
        raise HTTPException(status_code=404, detail="Invalid section id")

    # Prepare the response JSON
    response_data = {
        "section": section_id,
        "start_time": recitation_time.split("~")[0],
        "end_time": recitation_time.split("~")[1],
        "ta": [ta1_name, ta2_name]
    }

    return response_data
