#!/usr/bin/env python3

import os
import re
import argparse

def process_vtt_text(vtt_text, chunk_size=None):
    """
    - Removes WebVTT timestamps and metadata lines (e.g., align:start position:0%).
    - Strips out any <...> tags (like <c>).
    - Normalizes spacing.
    - Optionally breaks the transcript into smaller word-based chunks if chunk_size is provided.
    """

    # Regex to match WebVTT time ranges (e.g., "00:00:45.120 --> 00:00:47.270")
    timecode_pattern = re.compile(
        r'^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}.*$'
    )
    
    # Regex to remove tags like <c>, <00:00:45.280>, etc.
    tag_pattern = re.compile(r'<[^>]*>')

    cleaned_lines = []
    lines = vtt_text.splitlines()

    for line in lines:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
        
        # Skip lines that contain timecode
        if timecode_pattern.match(line):
            continue
        
        # Skip lines that contain alignment or position metadata
        # (You can refine this if you have legitimate text with these words.)
        if "align:start" in line or "position:" in line:
            continue

        # Remove leftover tags (e.g., <c>)
        line = tag_pattern.sub('', line)

        # Normalize multiple spaces to a single space
        line = re.sub(r'\s+', ' ', line)

        if line:
            cleaned_lines.append(line)

    # Join into one big string
    combined_text = " ".join(cleaned_lines)

    if not chunk_size:
        # No chunking, return as a single element in a list
        return [combined_text]
    else:
        # Chunk the transcript by number of words
        words = combined_text.split()
        chunks = []
        current_chunk = []
        word_count = 0

        for w in words:
            current_chunk.append(w)
            word_count += 1
            if word_count >= chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                word_count = 0

        # Add remaining words if any
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks


def main():
    parser = argparse.ArgumentParser(description="Clean all .vtt files in a given folder.")
    parser.add_argument("--folder", required=True, help="Path to the folder containing .vtt files")
    parser.add_argument("--chunk_size", type=int, default=None,
                        help="Number of words per chunk (optional). If not specified, single output.")
    
    args = parser.parse_args()
    input_folder = args.folder
    chunk_size = args.chunk_size

    # Ensure the folder exists
    if not os.path.isdir(input_folder):
        print(f"Error: The folder '{input_folder}' does not exist.")
        return

    # Process each .vtt file in the folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".vtt"):
            file_path = os.path.join(input_folder, filename)
            
            with open(file_path, "r", encoding="utf-8") as f:
                raw_vtt = f.read()
            
            # Clean and (optionally) chunk the transcript
            chunks = process_vtt_text(raw_vtt, chunk_size=chunk_size)

            # Build an output filename
            base_name = os.path.splitext(filename)[0]  # remove .vtt
            output_file = os.path.join(input_folder, f"{base_name}_cleaned.txt")

            # Write the output
            with open(output_file, "w", encoding="utf-8") as out_f:
                # If chunk_size is None, we have a single chunk
                # If chunk_size is provided, we have multiple
                for i, chunk in enumerate(chunks, start=1):
                    out_f.write(chunk)
                    out_f.write("\n\n")  # Separate chunks with blank line

            print(f"Processed '{filename}' -> '{output_file}'")


if __name__ == "__main__":
    main()
