import os
import tempfile
import shutil
from modules import report_generator

def sanitize_filename(name):
    return "_".join(name.strip().lower().split())

def save_summary_to_file(summaries, goal, format="md"):
    # ✅ Build safe filename and temp path
    safe_goal = sanitize_filename(goal)
    filename = f"{safe_goal}_summary_report.{format}"
    output_path = os.path.join(tempfile.gettempdir(), filename)

    # 🧠 Generate report content
    content = (
        report_generator.generate_markdown_report(summaries, goal)
        if format == "md"
        else report_generator.generate_report(summaries, goal, return_as_string=True)
    )

    if isinstance(content, list):
        content = "\n".join(content)

    # 📝 Write to temp file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Summary written to temp path: {output_path}")

    # 📤 Move to public static directory
    public_dir = os.path.join("static", "reports")
    os.makedirs(public_dir, exist_ok=True)
    public_path = os.path.join(public_dir, filename)
    shutil.copy(output_path, public_path)

    # 🔗 Return web-accessible path
    return "/" + public_path.replace("\\", "/")