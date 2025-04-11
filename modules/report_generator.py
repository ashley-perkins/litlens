import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_report(summaries, goal, output_path="litlens_summary_report.txt", format="txt", return_as_string=False):
    logger.info("📝 Generating report...")

    # --- Fix extension automatically ---
    if format == "md" and not output_path.endswith(".md"):
        output_path = output_path.replace(".txt", ".md")
    elif format == "txt" and not output_path.endswith(".txt"):
        output_path = output_path.replace(".md", ".txt")

    lines = []

    try:
        # --- Header ---
        if format == "md":
            lines.append(f"# LitLens Summary Report\n")
            lines.append(f"## Research Goal\n\n{goal}\n")
            lines.append(f"## Table of Contents\n")
        else:
            lines.append("LitLens Summary Report\n")
            lines.append("=======================\n")
            lines.append(f"Research Goal: {goal}\n")
            lines.append("Table of Contents\n========================\n")

        # --- TOC ---
        for i, paper in enumerate(summaries, 1):
            title = paper.get('title', f"Paper {i}")
            metadata = paper.get("metadata", {})

            meta_line = []
            if metadata.get("year"):
                meta_line.append(f"Year: {metadata['year']}")
            if metadata.get("journal"):
                meta_line.append(f"Journal: {metadata['journal']}")
            if metadata.get("authors"):
                meta_line.append(f"Authors: {metadata['authors']}")
            meta_line_str = " | ".join(meta_line)

            if format == "md":
                lines.append(f"{i}. [{title}](#paper-{i})")
                if meta_line_str:
                    lines.append(f"   - {meta_line_str}")
            else:
                lines.append(f"{i}. {title}")
                if meta_line_str:
                    lines.append(f"   - {meta_line_str}")

            chunks = paper.get("chunks", [])
            seen = set()
            for chunk in chunks:
                section_title = chunk.get('title', 'Untitled Section').strip()
                if section_title and section_title not in seen:
                    seen.add(section_title)
                    lines.append(f"   - {section_title}")

        lines.append("\n--- End of Table of Contents ---\n")
        logger.info("📚 TOC created successfully")

        # --- Full Summaries ---
        for i, paper in enumerate(summaries, 1):
            title = paper.get('title', f"Paper {i}")
            metadata = paper.get("metadata", {})

            meta_line = []
            if metadata.get("year"):
                meta_line.append(f"Year: {metadata['year']}")
            if metadata.get("journal"):
                meta_line.append(f"Journal: {metadata['journal']}")
            if metadata.get("authors"):
                meta_line.append(f"Authors: {metadata['authors']}")
            meta_line_str = " | ".join(meta_line)

            if format == "md":
                lines.append(f"\n## Paper {i}: {title}")
                if meta_line_str:
                    lines.append(f"*{meta_line_str}*\n")
            else:
                lines.append(f"\nPaper {i}: {title}")
                if meta_line_str:
                    lines.append(f"{meta_line_str}")
                lines.append("Summary:")

            lines.append(paper.get("summary", "[No summary available]").strip())

        if return_as_string:
            return "\n".join(lines)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        logger.info(f"💾 Report saved as: {output_path}\n")

    except Exception as e:
        logger.error(f"❌ Failed to generate report: {e}")



def generate_markdown_report(summaries, goal):
    report = []

    # --- Header ---
    report.append(f"# LitLens Summary Report\n")
    report.append(f"## Research Goal\n\n{goal}\n")
    report.append(f"## Table of Contents\n")

    for i, paper in enumerate(summaries, 1):
        title = paper.get("title", f"Paper {i}")
        metadata = paper.get("metadata", {})
        meta_line = []

        if metadata.get("year"):
            meta_line.append(f"Year: {metadata['year']}")
        if metadata.get("journal"):
            meta_line.append(f"Journal: {metadata['journal']}")
        if metadata.get("authors"):
            meta_line.append(f"Authors: {metadata['authors']}")
        meta_line = " | ".join(meta_line)

        report.append(f"{i}. [{title}](#paper-{i})")
        if meta_line:
            report.append(f"   - {meta_line}")
        seen = set()
        for chunk in paper.get("chunks", []):
            section_title = chunk.get("title", "Untitled Section").strip()
            if section_title not in seen:
                seen.add(section_title)
                report.append(f"   - {section_title}")

    report.append("\n--- End of Table of Contents ---\n")

    for i, paper in enumerate(summaries, 1):
        title = paper.get("title", f"Paper {i}")
        metadata = paper.get("metadata", {})
        meta_line = []

        if metadata.get("year"):
            meta_line.append(f"Year: {metadata['year']}")
        if metadata.get("journal"):
            meta_line.append(f"Journal: {metadata['journal']}")
        if metadata.get("authors"):
            meta_line.append(f"Authors: {metadata['authors']}")
        meta_line = " | ".join(meta_line)

        report.append(f"\n## Paper {i}: {title}")
        if meta_line:
            report.append(f"*{meta_line}*\n")
        report.append(paper.get("summary", "[No summary available]").strip())

    return "\n".join(report)
