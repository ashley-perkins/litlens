import os
from modules import report_generator

# Use /data on HF Spaces; otherwise fallback to ../output
HF_OUTPUT_DIR = "/data"
LOCAL_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
BASE_OUTPUT_DIR = HF_OUTPUT_DIR if os.access(HF_OUTPUT_DIR, os.W_OK) else LOCAL_OUTPUT_DIR

def sanitize_filename(name):
    """
    Replace or remove problematic characters from a string to make it safe for filenames.
    """
    return "_".join(name.strip().lower().split())

def save_summary_to_file(summaries, goal, output_dir=BASE_OUTPUT_DIR, format="md"):
    """
    Saves the generated summary report to a file in the specified format (markdown or text).
    """
    os.makedirs(output_dir, exist_ok=True)
    safe_goal = sanitize_filename(goal)
    filename = f"{safe_goal}_summary_report.{format}"
    output_path = os.path.join(output_dir, filename)

    # Generate report content
    if format == "md":
        content = report_generator.generate_markdown_report(summaries, goal)
    else:
        content = report_generator.generate_report(summaries, goal, return_as_string=True)

    # Ensure content is a string
    if isinstance(content, list):
        content = "\n".join(content)

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Summary written to: {output_path}")
    return output_path
