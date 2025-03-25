import pandas as pd

def process_transcript(file_path):
    df = pd.read_csv(file_path)
    print(f"Columns in the CSV file: {df.columns}")
    print(f"First few rows of the DataFrame:\n{df.head()}")
    df['subject'] = file_path.split('/')[-1].split('_')[0]  # Extract subject
    return df.to_dict('records')

def chunk_transcript(transcript, chunk_size=1000):
    chunks = []
    for row in transcript:
        if 'Course' in row and 'Topic' in row and 'Content' in row and 'subject' in row:
            text = f"{row['subject']} - {row['Course']} - {row['Topic']}: {row['Content']}"
        else:
            text = " - ".join(str(value) for value in row.values())
        chunks.extend([text[i:i+chunk_size] for i in range(0, len(text), chunk_size)])
    return chunks

if __name__ == "__main__":
    file_path = 'data/PDSA_Transcripts.csv'
    transcripts = process_transcript(file_path)
    chunked_transcripts = chunk_transcript(transcripts)

    print(f"Number of rows in transcript: {len(transcripts)}")
    print(f"Number of chunks: {len(chunked_transcripts)}")
    if chunked_transcripts:
        print(f"First chunk: {chunked_transcripts[0][:100]}...")
    else:
        print("No chunks were created.")