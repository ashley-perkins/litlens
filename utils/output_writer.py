import os
import shutil
from modules import report_generator

# ✅ Set the output directory inside the static folder
BASE_OUTPUT_DIR = "./output"

def sanitize_filename(name):
    return "_".join(name.strip().lower().split())

def save_summary_to_file(summaries, goal, output_dir=BASE_OUTPUT_DIR, format="md"):
    os.makedirs(output_dir, exist_ok=True)  # ✅ Create folder if it doesn't exist

    safe_goal = sanitize_filename(goal)
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

    # 📄 Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Summary written to: {output_path}")
    static_reports_dir = os.path.join("static", "reports")
    os.makedirs(static_reports_dir, exist_ok=True)
    shutil.copy(output_path, os.path.join(static_reports_dir, filename))
    return output_path
