# Usage

## 1. Create a virtual environment
```bash
cd ClassAutoLogger
python3 -m venv venv
```

## 2. Install libraries
```bash
pip install -r requirements.txt
```

## 3. Setup the timetable
```bash
nano timetable.txt
```
The timetable should be in the following format:
```
Day,Hour1,Hour2,Hour3,Hour4,Hour5,Hour6 
Monday,ICS 423,ICS 422, IOE421,...
Tuesday,,IOE421,...
.
.
Friday,......

Example (Classes can start from 11 to 13):
Day,11,12,13
Monday,,ICS 423,IOE 421
Tuesday,ICS 422,IOE 421,ICS 422
Wednesday,ICS 423,,ICS 423
Thursday,,ICS 423,ICS 423
Friday,,IOE 421,ICS 422


```

## 4. Run the program
```bash
python class_auto_login.py
```

