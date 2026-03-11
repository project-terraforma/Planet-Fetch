# Getting Started
Here is how to get this project running on your local machine!
## 1. Clone the Repository

- Fork the repository from https://github.com/project-terraforma/Planet-Fetch.git
- git clone https://github.com/project-terraforma/Planet-Fetch.git


## System Requirements:
- This project works best on a linux based terminal in VS Code.
- Have unzip installed on your system.
- You will need to have python installed on your machine.
- Due to the size of the metrics folder, you will have to manually insert the metrics folder   into your directory -> (Steps shown later on).

## 2. Set up Python Environment

Create a virtual environment:
```bash
python3 -m venv .venv
```

Activate the venv:

```bash
source .venv/bin/activate
```

## dependencies needed

For python pipeline:

```bash
pip install -r requirements.txt
```

For App:

```bash
npm install
```

## Downloading and Setting Up Metrics Folder

- Download the zipped Metrics folder from the following link: 
https://drive.google.com/file/d/17Yip5rMcTmhHohHdc2jGx7ewMElbH9Gq/view?usp=sharing

- create a folder named metrics in your project directory.
- place the zipped folder in Metrics folder.
- Unzip the folder using the command: unzip Metrics.zip
- feel free to delete zipped folder after unzipping.

## 3. Run the Pipeline
The pipeline can be ran one of two ways.

### Option 1: 
Run each stage of the pipeline manually using the CLI.

Example:

```bash
python python_pipeline/clean.py
python python_pipeline/flatten.py
python python_pipeline/contextgen.py
python python_pipeline/reformatter.py
```

You may also run the full pipeline script:
```bash
python python_pipeline/pipeline.py
```

### Option 2: 
Run the pipeline using the app interface.

From the UI you can:

- Trigger the pipeline
- Process datasets
- Generate context files
- View outputs

This option runs the pipeline through the backend API routes.

## 4. Example Output

Generated context files will appear in:

contexts/<release-date>/

Each folder corresponds to an Overture release and contains the generated context files.

Example:

contexts/
   2025-05-21.0/
   2025-06-25.0/
   ...

## 5. Troubleshooting

unzip not found

Install it with:

```bash 
sudo apt install unzip
```

Python dependencies not installing

Make sure the virtual environment is activated:

```bash
source .venv/bin/activate
```

npm install fails

Ensure Node.js is installed:

```bash
node -v
npm -v
```

App not updating or behaving strangely

Delete the Next.js build cache and restart the app:

```bash
rm -rf .next
npm run dev
```

Context generation taking too long or UI becomes unresponsive

Try running the app on a different port:

```bash
npm run dev -- -p 3001
```

Then open:

```bash
http://localhost:3001
```

Running on a different port can sometimes resolve issues with stalled processes or port conflicts.