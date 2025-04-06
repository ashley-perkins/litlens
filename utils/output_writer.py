import os

def save_summary_to_file(summary_data, output_dir="output", filename="summary.txt"):
    """
    Saves a summarized paper to a text file with metadata.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Goal: {summary_data.get('goal', 'N/A')}\n")
        f.write(f"Filename: {summary_data.get('filename', 'N/A')}\n")
        f.write(f"Title: {summary_data.get('title', 'N/A')}\n")
        
        metadata = summary_data.get("metadata", {})
        f.write(f"Year: {metadata.get('year', 'N/A')}\n")
        f.write(f"Authors: {metadata.get('authors', 'N/A')}\n")
        f.write(f"Journal: {metadata.get('journal', 'N/A')}\n")
        
        f.write("\n--- Summary ---\n")
        f.write(summary_data.get("summary", "No summary available.").strip())
        print(f"📄 Writing summary to {output_path}")
    
    print(f"✅ Summary written to: {output_path}")