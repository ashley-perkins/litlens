import os
import shutil
from modules import report_generator

# ✅ Hugging Face writable directory
BASE_OUTPUT_DIR = "/data/reports"

def sanitize_filename(name):
    return "_".join(name.strip().lower().split())

def save_summary_to_file(summaries, goal, output_dir=BASE_OUTPUT_DIR, format="md"):
    os.makedirs(output_dir, exist_ok=True)

    safe_goal = sanitize_filename(goal or "summary")
    filename = f"{safe_goal}_summary_report.{format}"
    output_path = os.path.join(output_dir, filename)

    # ✍️ Generate report content
    content = (
        report_generator.generate_markdown_report(summaries, goal)
        if format == "md"
        else report_generator.generate_report(summaries, goal, return_as_string=True)
    )

    if isinstance(content, list):
        content = "\n".join(content)

    # 📄 Write to /data
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Summary written to: {output_path}")
    return output_path
