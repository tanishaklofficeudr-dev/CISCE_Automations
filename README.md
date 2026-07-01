Project Setup & Execution Steps

1. Open project folder in VS Code

2. Create virtual environment:
   python -m venv venv

3. Activate virtual environment:
   venv\Scripts\activate

4. Install dependencies:
   pip install -r requirements.txt

5. Install Playwright browsers:
   playwright install

--------------------------------------------------
Run Automation Test
--------------------------------------------------

Basic Execution:
python -m pytest tests/test_preliminary_form_main.py -v --headed

Execution with Slow Motion:
python -m pytest tests/test_preliminary_form_main.py -v --headed --slowmo=1000

--------------------------------------------------
Generate HTML Report
--------------------------------------------------

python -m pytest tests/test_preliminary_form_main.py --html=reports/report.html --self-contained-html

Report Location:
reports/report.html

--------------------------------------------------
Capture Screenshots on Failure
--------------------------------------------------

pytest --screenshot=only-on-failure

Screenshot Location:
screenshots/

--------------------------------------------------
Capture Video Recording
--------------------------------------------------

pytest --video=on

Video Location:
videos/

--------------------------------------------------
Capture Playwright Traces
--------------------------------------------------

pytest --tracing=on

Trace Location:
traces/

To Open Trace Viewer:
playwright show-trace traces/<trace-file>.zip

--------------------------------------------------
Run Complete Framework
--------------------------------------------------

python -m pytest -v --headed

--------------------------------------------------
Folder Structure
--------------------------------------------------

pages/        -> Page Object Model files
tests/        -> Test cases
utils/        -> Utility files
test_data/    -> Test data & documents
reports/      -> HTML reports
screenshots/  -> Failure screenshots
videos/       -> Execution videos
traces/       -> Playwright traces