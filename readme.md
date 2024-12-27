# Course-Note-Helper

A **command-line tool** for taking **concise course notes** from YouTube video subtitles. Whether you’re a student, researcher, or lifelong learner, this tool automates much of the grunt work in **capturing lecture notes** from online lectures or educational videos. Simply download the `.vtt` subtitles, clean them with our script, and optionally process them further in GPT (or any other language model).

## Key Features

- **YouTube Subtitles Support**  
  Automatically download `.vtt` subtitles from YouTube using `yt-dlp`.

- **Automated Cleanup**  
  Remove timestamps, alignment tags, and extraneous formatting (`<c>`, `<00:00:07.440>`, etc.), leaving you with clean, readable text.

- **Customizable Chunking**  
  Split large transcripts into smaller chunks (by word count), making them easier to feed into GPT or other AI models with token limits.

- **Minimal Dependencies**  
  A single Python script (`clean.py`) plus `yt-dlp` (and optionally other libraries if you plan to do more advanced text processing).

## Getting Started

### 1. Clone This Repository

```bash
git clone https://github.com/mark.ma/course-note-helper.git
cd course-note-helper
```

### 2. Download YouTube Subtitles
Before cleaning them, you need .vtt files. Use yt-dlp from your command line:

```bash
yt-dlp --write-auto-subs --sub-lang en --skip-download "https://www.youtube.com/watch?v=VIDEO_ID"
```
### 3. Clean and Chunk Subtitles
Use clean_vtt.py to clean all .vtt files in a specified folder. You can also break them into chunks for easier processing in GPT or other LLMs.
```bash
python clean.py --folder /path/to/vtt_files 
```
### 4. Next Steps: Summarize with GPT

"You are a teaching assistant. The following text is a transcript from a YouTube lecture on [TOPIC]. 
Your task is to produce comprehensive yet concise notes suitable for a course handout. 
Focus on key concepts, examples, definitions, and any step-by-step processes mentioned. 
Below is the transcript: 

[Transcript chunk]

Now, please generate a bullet-point summary that highlights the main points, important details, and potential exam questions."



