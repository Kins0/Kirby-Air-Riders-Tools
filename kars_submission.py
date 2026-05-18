import time
from urllib.parse import urlencode, quote
import requests
import yt_dlp
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv("config.env")

FORM_RESPONSE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf_iiJyL8PbvwKx0JtCtyMjDnVAza4dD5y7r_3lYQWGJoGfaA/formResponse"
SRC_URL = "https://www.speedrun.com/api/v1/runs"
SRC_API_KEY = os.getenv("SRC_API_KEY")

GAMERTAG = os.getenv("GAMERTAG")
TWITTER = os.getenv("TWITTER")
GAME_TYPE = "Air Ride"

# Speedrun.com specific information
GAME_ID = "w6jgm776"
AIR_RIDE_ID = "vdo995vd"
TOP_RIDE_ID = "wkp445wk" # No use yet, just for future proofing
AIR_RIDE_TA_ID = "z27qqvgk"
AIR_RIDE_FR_ID = "zdnjjyqk"

def now_ms() -> str:
    return str(int(time.time() * 1000))

def make_partial_response() -> str:
    return f'[[[null,208317302,["{GAMERTAG}"],0],[null,35900060,["{TWITTER}"],0],[null,514129756,["{GAME_TYPE}"],0]],null,"423242341241234"]'

def get_youtube_upload_date(url: str) -> date:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "simulate": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    raw = info.get("upload_date")
    if not raw:
        raise ValueError("Could not extract upload date from YouTube video.")
    
    return date(
        int(raw[0:4]),
        int(raw[4:6]),
        int(raw[6:8]),
    )

def validate_mode(mode: str) -> str:
    valid_modes = ["Free Run", "Time Attack"]

    alias_groups = {
        ("fr", "free", "freerun", "free run"): "Free Run",
        ("ta", "time", "timeattack", "time attack"): "Time Attack",
    }

    aliases = {}
    for keys, value in alias_groups.items():
        for k in keys:
            aliases[k] = value

    normalized = mode.strip().lower()
    if normalized in aliases:
        return aliases[normalized]

    if mode in valid_modes:
        return mode

    raise ValueError("Mode must be 'Free Run' or 'Time Attack'.")


def validate_course(course: str) -> str:
    valid_courses = [
        "Floria Fields",
        "Waveflow Waters",
        "Cavernous Corners",
        "Cyberion Highway",
        "Mount Amberfalls",
        "Steamgust Forge",
        "Airtopia Ruins",
        "Crystalline Fissure",
        "Galactic Nova",
        "Fantasy Meadows",
        "Celestial Valley",
        "Sky Sands",
        "Frozen Hillside",
        "Magma Flows",
        "Beanstalk Park",
        "Machine Passage",
        "Checker Knights",
        "Nebula Belt",
    ]

    alias_groups = {
        ("ff", "florida", "floria", "floriafields", "floria fields"): "Floria Fields",
        ("ww", "waveflow", "dougwater", "doug", "dugwater", "waveflowwaters", "waveflow waters"): "Waveflow Waters",
        ("cc", "cavern", "cavernous", "cavernouscorners", "cavernous corners"): "Cavernous Corners",
        ("ch", "cyberion", "cyberionhighway", "cyberion highway"): "Cyberion Highway",
        ("ma", "amber", "mount", "amberfalls", "mountamberfalls", "mount amberfalls", "foris"): "Mount Amberfalls",
        ("sf", "steam", "forge", "george", "steamgust", "steamgustforge", "steamgust forge"): "Steamgust Forge",
        ("ar", "airtopia", "airtopiaruins", "airtopia ruins"): "Airtopia Ruins",
        ("cf", "crystalline", "fissure", "crystallinefissure", "crystalline fissure"): "Crystalline Fissure",
        ("gn", "nova", "galactic", "galacticnova", "galactic nova"): "Galactic Nova",
        ("fm", "meadows", "fantasy", "ohio", "fantasymeadows", "fantasy meadows"): "Fantasy Meadows",
        ("cv", "celestial", "celestialvalley", "celestial valley"): "Celestial Valley",
        ("ss", "skands", "sands", "sky", "skysands", "sky sands"): "Sky Sands",
        ("fh", "frozen", "hillside", "hillslide", "frozenhillside", "frozenhillslide", "frozen hillside", "frozen hillslide", "corda"): "Frozen Hillside",
        ("mf", "magma", "magmaflows", "magma flows"): "Magma Flows",
        ("bp", "beans", "beanstalk", "park", "beanstalk park", "beanstalkpark"): "Beanstalk Park",
        ("mp", "machine", "passage", "machinepassage", "machine passage"): "Machine Passage",
        ("ck", "checker", "knights", "checkerknights", "checker knights"): "Checker Knights",
        ("nb", "nebula", "belt", "nebulabelt", "nebula belt"): "Nebula Belt",
    }

    aliases = {}
    for keys, value in alias_groups.items():
        for k in keys:
            aliases[k] = value

    normalized = course.strip().lower()
    if normalized in aliases:
        return aliases[normalized]

    if course in valid_courses:
        return course

    raise ValueError("Invalid course.")

def validate_machine(machine: str) -> str:
    valid_machines = [
        "Warp Star",
        "Winged Star",
        "Shadow Star",
        "Wagon Star",
        "Slick Star",
        "Bulk Star",
        "Rocket Star",
        "Swerve Star",
        "Turbo Star",
        "Wheelie Bike",
        "Rex Wheelie",
        "Paper Star",
        "Chariot",
        "Battle Chariot",
        "Tank Star",
        "Formula Star",
        "Jet Star",
        "Hop Star",
        "Wheelie Scooter",
        "Transform Star",
        "Bull Tank",
        "Vampire Star",
        "Dragoon",
        "Hydra",
        "Leo",
    ]

    alias_groups = {
        ("warp", "warpstar", "warp star"): "Warp Star",
        ("wing", "winged", "wingedstar", "winged star", "wingstar", "wingstar"): "Winged Star",
        ("shadow", "shadowstar", "shadow star", "devil", "devilstar", "devil star"): "Shadow Star",
        ("wagon", "fnord", "wagonstar", "wagon star"): "Wagon Star",
        ("slick", "soap", "slickstar", "slick star"): "Slick Star",
        ("bulk", "bulkstar", "bulk star"): "Bulk Star",
        ("rocket", "rocketstar", "rocket star"): "Rocket Star",
        ("swerve", "swervestar", "swerve star"): "Swerve Star",
        ("turbo", "turbostar", "turbo star"): "Turbo Star",
        ("bike", "wheeliebike", "wheelie bike"): "Wheelie Bike",
        ("rex", "rexwheelie", "rex wheelie"): "Rex Wheelie",
        ("paper", "paperstar", "paper star"): "Paper Star",
        ("chariot",): "Chariot",
        ("battlechariot", "battle chariot"): "Battle Chariot",
        ("tank", "tankstar", "tank star"): "Tank Star",
        ("formula", "formulastar", "formula star"): "Formula Star",
        ("jet", "jetstar", "jet star"): "Jet Star",
        ("hop", "hopstar", "hop star"): "Hop Star",
        ("scooter", "wheeliescooter", "wheelie scooter"): "Wheelie Scooter",
        ("transform", "trans", "henshin", "transformstar", "transform star", "henshinstar", "henshin star"): "Transform Star",
        ("bull", "bulltank", "bull tank"): "Bull Tank",
        ("vampire", "vampirestar", "vampire star"): "Vampire Star",
        ("dragoon", "dragon"): "Dragoon",
        ("hydra",): "Hydra",
        ("leo",): "Leo",
    }

    aliases = {}
    for keys, value in alias_groups.items():
        for k in keys:
            aliases[k] = value

    normalized = machine.strip().lower()
    if normalized in aliases:
        return aliases[normalized]

    if machine in valid_machines:
        return machine

    raise ValueError("Invalid machine.")

def validate_rider(rider: str) -> str:
    valid_riders = [
        "Kirby (Pink)",
        "Kirby (Yellow or Green)",
        "Kirby (Red or Purple)",
        "Kirby (Blue or White)",
        "King Dedede",
        "Meta Knight",
        "Bandana Waddle Dee",
        "Waddle Doo",
        "Chef Kawasaki",
        "Knuckle Joe",
        "Gooey",
        "Cappy",
        "Star Man",
        "Magolor",
        "Susie",
        "Waddle Dee",
        "Rick",
        "Rocky",
        "Scarfy",
        "Lololo & Lalala",
        "Marx",
        "Daroach",
        "Taranza",
        "Noir Dedede",
    ]

    alias_groups = {
        ("pink", "pinkkirby", "pink kirby", "kirby pink", "kirby (pink)"): "Kirby (Pink)",
        ("yellow", "green", "yellow kirby", "green kirby", "kirby green", "kirby yellow", "kirby (yellow or green)"): "Kirby (Yellow or Green)",
        ("red", "purple", "kirby red", "kirby purple", "red kirby", "purple kirby", "kirby (red or purple)"): "Kirby (Red or Purple)",
        ("blue", "white", "kirby blue", "kirby white", "blue kirby", "white kirby", "kirby (blue or white)"): "Kirby (Blue or White)",
        ("ddd", "dedede", "king", "king dedede"): "King Dedede",
        ("mk", "meta", "knight", "meta knight", "metaknight"): "Meta Knight",
        ("bandee", "dana", "bandana", "bandana dee", "bandana waddle dee"): "Bandana Waddle Dee",
        ("doo", "waddle doo"): "Waddle Doo",
        ("chef", "kawasaki", "chef kawasaki"): "Chef Kawasaki",
        ("knuckle", "joe", "knuckle joe"): "Knuckle Joe",
        ("goo", "gooey"): "Gooey",
        ("cap", "cappy"): "Cappy",
        ("star", "starman", "star man"): "Star Man",
        ("magolor", "mag"): "Magolor",
        ("susie",): "Susie",
        ("dee", "waddle dee"): "Waddle Dee",
        ("rick",): "Rick",
        ("rock", "rocky"): "Rocky",
        ("scarfy",): "Scarfy",
        ("lola", "lololo", "lalala", "lololo and lalala", "lololo lalala", "lololo & lalala"): "Lololo & Lalala",
        ("marx",): "Marx",
        ("daroach", "droche"): "Daroach",
        ("ranza", "taranza"): "Taranza",
        ("noir", "noir dedede", "noir ddd"): "Noir Dedede",
    }

    aliases = {}
    for keys, value in alias_groups.items():
        for k in keys:
            aliases[k] = value

    normalized = rider.strip().lower()
    if normalized in aliases:
        return aliases[normalized]

    if rider in valid_riders:
        return rider

    raise ValueError("Invalid rider.")

def get_src_level_id(course: str, category: str) -> str:
    level_ids_fr = {
        "Floria Fields": "qyzpy5d1",
        "Waveflow waters": "ln8w0dnl",
        "Airtopia Ruins": "10vzm0pl",
        "Crystalline Fissure": "qj704woq",
        "Steamgust Forge": "q650xyol",
        "Cavernous Corners": "lmok4801",
        "Cyberion Highway": "1w4pde6q",
        "Mount Amberfalls": "qoxp3m4q",
        "Galactic Nova": "1398mwy1",
        "Fantasy Meadows": "qvvpr6yq",
        "Celestial Valley": "le2r4k6l",
        "Sky Sands": "q5vn5ovl",
        "Frozen Hillside": "lx5p8xg1",
        "Magma Flows": "14oyvxkq",
        "Beanstalk Park": "192m944q",
        "Machine Passage": "12vdw52q",
        "Checker Knights": "1pyp07n1",
        "Nebula Belt": "qkej4r4q"
    }

    level_ids_ta = {
        "Floria Fields": "le2r4npl",
        "Waveflow waters": "q5vn54rl",
        "Airtopia Ruins": "lx5p8gj1",
        "Crystalline Fissure": "14oyv9wq",
        "Steamgust Forge": "192m95jq",
        "Cavernous Corners": "12vdwovq",
        "Cyberion Highway": "1pyp04e1",
        "Mount Amberfalls": "qkej499q",
        "Galactic Nova": "q75j49n1",
        "Fantasy Meadows": "1gn84exl",
        "Celestial Valley": "qznp5v4q",
        "Sky Sands": "lr3p0j0l",
        "Frozen Hillside": "q75j49r1",
        "Magma Flows": "1gn84eol",
        "Beanstalk Park": "qznp5vkq",
        "Machine Passage": "lr3p0jwl",
        "Checker Knights": "1dkzyvgl",
        "Nebula Belt": "q8k6026q"
    }

    return level_ids_fr[course] if category == AIR_RIDE_FR_ID else level_ids_ta[course]

def validate_env(submit_type: str) -> str:
    if submit_type == "0":
        if SRC_API_KEY == None or GAMERTAG == None or TWITTER == None or SRC_API_KEY == "" or GAMERTAG == "" or TWITTER == "":
            raise ValueError("Make sure SRC_API_KEY, GAMERTAG and TWITTER in config.env are set")
        print("Submitting to both Speedrider and Speedrun.com")
        return submit_type
    elif submit_type == "1":
        if GAMERTAG == None or TWITTER == None or GAMERTAG == "" or TWITTER == "":
            raise ValueError("Make sure GAMERTAG and TWITTER in config.env are set")
        print("Submitting only to Speedrider")
        return submit_type
    elif submit_type == "2":
        if SRC_API_KEY == None or SRC_API_KEY == "":
            raise ValueError("Make sure SRC_API_KEY in config.env is set")
        print("Submitting only to Speedrun.com")
        return submit_type
    else:
        raise ValueError("Enter one of the listed numbers")
        
 
def get_src_rider_id(rider: str) -> str:
    rider_ids = {
        "Kirby (Pink)": "1pyp0nn1",
        "Kirby (Yellow or Green)": "qkej484q",
        "Kirby (Red or Purple)": "1gn84gol",
        "Kirby (Blue or White)": "q75j4gr1",
        "King Dedede": "qznp54kq",
        "Meta Knight": "lr3p07wl",
        "Bandana Waddle Dee": "q8k60z6q",
        "Waddle Doo": "qyzpy4d1",
        "Chef Kawasaki": "ln8w03nl",
        "Knuckle Joe": "10vzm7pl",
        "Gooey": "q650x7ol",
        "Cappy": "lmok4n01",
        "Star Man": "1398mry1",
        "Magolor": "lx5p88g1",
        "Susie": "192m994q",
        "Waddle Dee": "1dkzydgl",
        "Rick": "qj704doq",
        "Rocky": "1w4pd86q",
        "Scarfy": "qoxp3n4q",
        "Lololo & Lalala": "qvvprdyqm",
        "Marx": "le2r446l",
        "Daroach": "q5vn55vl",
        "Taranza": "14oyvvkq",
        "Noir Dedede": "12vdww2q",
    }

    return rider_ids[rider]

def get_src_machine_id(machine: str) -> str:
    machine_ids = {
        "Warp Star": "1pyp00n1",
        "Winged Star": "q75j44r1",
        "Shadow Star": "1gn844ol",
        "Wagon Star": "qznp55kq",
        "Slick Star": "lr3p00wl",
        "Bulk Star": "1gn8448l",
        "Rocket Star": "qznp558q",
        "Swerve Star": "lr3p00ml",
        "Turbo Star": "1dkzyy5l",
        "Wheelie Bike": "qyzpyy21",
        "Rex Wheelie": "ln8w00jl",
        "Paper Star": "lmok44m1",
        "Chariot": "1w4pd5vq",
        "Battle Chariot": "qoxp3rxq",
        "Tank Star": "1398m5x1",
        "Formula Star": "q75j44d1",
        "Jet Star": "q8k6003q",
        "Hop Star": "qj70443q",
        "Wheelie Scooter": "10vzmm2l",
        "Transform Star": "le2r4mkl",
        "Bull Tank": "qvvpre6q",
        "Vampire Star": "q650xxjl",
        "Dragoon": "q5vn5g2l",
        "Hydra": "lx5p8e41",
        "Leo": "14oyv7vq",
    }

    return machine_ids[machine]

def time_src_converter(time: str) -> float:
    s = time.strip()
    if ":" in s:
        mins_part, rest = s.split(":", 1)
        if "." not in rest:
            raise ValueError("Expected '.' in SS.CS part")
        secs_part, cs_part = rest.split(".", 1)
        if not (mins_part.isdigit() and secs_part.isdigit() and cs_part.isdigit()):
            raise ValueError("Non-numeric time components")
        if len(mins_part) > 2 or len(mins_part) < 1:
            raise ValueError("Minutes must be either 1 or 2 digits")
        if len(secs_part) != 2:
            raise ValueError("Seconds must be provided with 2 digits")
        if len(cs_part) != 2:
            raise ValueError("Centiseconds part must have 2 digits (MM:SS.CS or M:SS.CS)")
        minutes = int(mins_part)
        seconds = int(secs_part)
        centiseconds = int(cs_part)

        total_time_in_seconds = ((minutes * 60) + seconds) + (centiseconds / 100)
        print(f"Total time in seconds: {total_time_in_seconds}")

        return total_time_in_seconds
    else:
        secs_part, cs_part = s.split(".", 1)
        if len(secs_part) > 2 or len(secs_part) < 1:
            raise ValueError("Seconds must be either 1 or 2 digits")
        if len(cs_part) != 2:
            raise ValueError("Centiseconds must be 2 digits")
        seconds = int(secs_part)
        centiseconds = int(cs_part)

        total_time_in_seconds = seconds + (centiseconds / 100)
        print(f"Total time in seconds: {total_time_in_seconds}")

        return total_time_in_seconds

def get_run_type(machine) -> str: # for SRC, determines "Restricted" or "Legendaries"
    if machine == "Dragoon" or machine == "Hydra" or machine == "Leo":
        return "1pyp0d81"
    else:
        return "192m988q"

def submit_run(
    mode: str,
    course: str,
    machine: str,
    rider: str,
    run_time: str,
    video_url: str,
    upload_date: date,
    submit_type: str
):
    session = requests.session()

    timestamp = now_ms()

    speedrider_data = {
        "entry.1986804768": mode,
        "entry.1790591113": course,
        "entry.816568203": machine,
        "entry.481185262": rider,
        "entry.1940602356": run_time,
        "entry.555836324": video_url,
        "entry.1550570894_year": str(upload_date.year),
        "entry.1550570894_month": str(upload_date.month),
        "entry.1550570894_day": str(upload_date.day),

        # Some hidden Google Forms fields
        "partialResponse": make_partial_response(),
        "pageHistory": "0,1",
        "submissionTimestamp": timestamp,
    }

    src_data = {
        "run": {
            "category": AIR_RIDE_FR_ID if mode == "Free Run" else AIR_RIDE_TA_ID,
            "level": "dy123jpd", # This is static, don't change it
            "date": upload_date.isoformat(),
            "platform": "3167lw9q", # Switch 2, only platform so it's static
            "times": {
                "ingame": time_src_converter(run_time)
            },
            "emulated": False,
            "video": video_url,
            "variables": {
                "ylq4rkmn": {
                    "type": "pre-defined",
                    "name": "Track",
                    "value": get_src_level_id(course, mode)
                },
                "yn26r10l": {
                    "type": "pre-defined",
                    "name": "Rider",
                    "value": get_src_rider_id(rider)
                },
                "6njp6qpn": {
                    "type": "pre-defined",
                    "name": "Machine",
                    "value": get_src_machine_id(machine)
                },
                "wle3vxr8": { 
                    "type": "pre-defined",
                    "name": "Version",
                    "value": "1390wnk1" # This will change if the game receives an update.
                },
                "kn0e5z38": {
                    "type": "pre-defined",
                    "name": "Type",
                    "value": get_run_type(machine)
                }
            }
            
        }
    }

    if submit_type in {"0", "1"}:
        speedrider_response = session.post(url=FORM_RESPONSE_URL, data=urlencode(speedrider_data, quote_via=quote), headers={"Content-Type": "application/x-www-form-urlencoded"})
        if speedrider_response.status_code == 200 or speedrider_response.status_code == 302:
            print("Submitted successfully to Speedrider")
        else:
            print(f"Submission to Speedrider might have failed: {speedrider_response.status_code}")

    if submit_type in {"0", "2"}:
        src_response = session.post(url=SRC_URL, json=src_data, headers={"Content-Type": "application/json", "X-API-Key": SRC_API_KEY})
        if src_response.status_code == 201:
            print("Submitted successfully to Speedrun.com")
        else:
            print(f"Submission to Speedrun.com might have failed: {src_response.status_code}")


submit_type = validate_env(input("Where to submit (enter one of the following numbers): 0 = Both sites, 1 = Speedrider, 2 = Speedrun.com \n").strip())
mode = validate_mode(input("Mode [Free Run/Time Attack]: ").strip())
course = validate_course(input("Course: ").strip())
machine = validate_machine(input("Machine: ").strip())
rider = validate_rider(input("Rider: ").strip())
run_time = input("Time: ").strip()
video_url = input("Video URL: ").strip()

print("Fetching YouTube upload date...")
upload_date = get_youtube_upload_date(video_url)

print(f"Using upload date: {upload_date.isoformat()}")
print(f"Year: {upload_date.year}, Month: {upload_date.month}, Day: {upload_date.day}")

submit_run(
    mode,
    course,
    machine,
    rider,
    run_time,
    video_url,
    upload_date,
    submit_type
)
