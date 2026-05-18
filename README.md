# Kirby Air Riders Tools
Here you can find tools which simplify processes within the Kirby Air Riders community.

## KARS Submission
This script (kars_submission.py) simplifies the submission process to both [Speedrider](https://speedrider.coresv.net/?lang=en) and [Speedrun.com](https://speedrun.com/kars). Motivations for this script were both time consumption of submitting (always opening each site, clicking through forms, etc.) and making it easier for the maintainers of each site so they don't have to manually copy records over.

### Installing
Make sure to clone the repository and have [Python](https://python.org) installed. On Windows or Mac you'd download the executable from the website, on Linux you probably have it installed already or can simply download it from your package manager.

You will need Pip (which is a package manager for Python) but it should be installed by the Python installer. It is recommended to install Git if you haven't and clone the repository with it. If you really don't want to do that you can also manually download the folder by clicking "Code" -> "Download ZIP".

#### Installing dependencies
Open a terminal/command prompt/powershell and navigate to the folder you cloned this repository into. You need to be in the same folder as the file "requirements.txt". Windows users can Shift+right-click in their file explorer while in the desired folder and click something along the lines of "Open PowerShell here"/"Open Command Prompt here" (I can't test it as I don't use Windows but you will find it).

On Linux/Mac OS, open your terminal and navigate into the directory by cd'ing into it.

```
git clone https://github.com/Kins0/Kirby-Air-Riders-Tools.git
cd Kirby-Air-Riders-Tools
```

Once you're in the correct directory install the necessary dependencies by running

```
pip install -r requirements.txt
```

You can either do it globally (the way shown above) or within a venv. If you don't know what that is don't worry about it, you won't need it.
### Usage
Once you cloned the repository you will have to copy config.example.env and create the file config.env. Inside there you will see SRC_API_KEY, GAMERTAG and TWITTER. If you plan on submitting to both sites all of those need to be filled.

If you plan on submitting to only Speedrider you will not have to specify SRC_API_KEY. If you plan on submitting only to Speedrider.com you will only need to specify SRC_API_KEY.

Setting all environmental variables is recommended to seamlessly be able to submit to both sites at the same time. Once they're set you won't have to touch that file ever again and you will automatically submit to the correct accounts.

If you're wondering where to get SRC_API_KEY from or what it is: It is a key which let's you submit to [Speedrun.com](https://speedrun.com) by using their REST API without needing to log into the site every time.

To obtain that key you will have to log into the site and go to your account settings. In the category "DEVELOPERS" you will find "API Key". Here you can obtain your API key. Make sure to save it and store it somewhere (you can also just store it in the config.env if you don't plan on deleting it again).

To run the tool (make sure to have all install steps completed beforehand) run

```
python kars_submission.py
```

Make sure you're in the same directory as that file in your terminal or python won't find the script and can't run it. You will be guided through the submission with text prompts and have to answer them. If something is invalid you will get an error and have to restart the script. This ensures you don't accidentally submit something invalid to make the site maintainers' life easier. Each input you provide will be validated and if you didn't provide a valid input you will have to start over without needing to finish the prompts after the invalid one. The prompts aren't case sensitive so don't worry about that.

First you will be asked whether you want to submit to both sites or just one of them. Enter the number that's assigned to the desired option.

Then you will be asked whether you want to submit a Free Run or Time Attack run. A quality of life feature in this script is the ability to use aliases (e.g. you can type "fr" instead of "Free Run" or "ta" instead of "Time Attack").

Then you'll have to type in the course your run was set on. You can either type out the full name of the course or use abbreviations. I've tried to add as many abbreviations as I could think of for each course. The fastest and easiest way is probably to just use initials (e.g. "nb" for "Nebula Belt", "ma" for "Mount Amberfalls", etc.).

Then you are prompted to enter the machine you used in your run. Either type the full name or use an abbreviation. Unless it is ambiguous it is enough to just provide one of the words (e.g. "slick" instead of "Slick Star", "warp" instead of "Warp Star", etc.). "Wheelie" is not a valid abbreviation as "Wheelie Scooter", "Wheelie Bike" and "Rex Wheelie" all contain that word. You can just use the other word (e.g. "rex").

Next you will be prompted to enter the used rider. Both the full name and common abbreviations work (e.g. "ddd", "lola" etc.).

Then you will need to enter your run time. The time needs to be entered in one of the following formats (trailing zeros can be omitted, e.g. 02:05.44 = 2:05.44, 00:34.18 = 34.18):
 - MM:SS.cc (Minutes, Seconds, Centiseconds)
 - SS.cc (Seconds, Centiseconds. This only works if your run is shorter than a minute. If your run is longer than a minute you need to use the other format)

Then you'll be prompted to provide a URL to your run. The tool will automatically fetch the video's upload date so you will not have to manually provide that.

If everything went right your run should be submitted. The tool will tell you whether a submission was successful or if it failed. Nevertheless, scripts can have bugs so it's worth to check whether your run was submitted to the site or not. Do this by checking [Speedrider submissions](https://speedrider.coresv.net/status) and pending runs your profile settings at [Speedrun.com](https://speedrun.com).

Submitting a run with this tool is done in less than a minute and once you got it to work the process is always the same.
