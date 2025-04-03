import os

def generate_report(summaries, goal, output_path="litlens_summary_report.txt", format="txt"):
    print("📝 Generating report...")

    # --- Fix extension automatically ---
    if format == "md" and not output_path.endswith(".md"):
        output_path = output_path.replace(".txt", ".md")
    elif format == "txt" and not output_path.endswith(".txt"):
        output_path = output_path.replace(".md", ".txt")

    with open(output_path, "w", encoding="utf-8") as f:

        # --- Header ---
        if format == "md":
            f.write(f"# LitLens Summary Report\n\n")
            f.write(f"## Research Goal\n\n{goal}\n\n")
            f.write(f"## Table of Contents\n\n")
        else:
            f.write("LitLens Summary Report\n")
            f.write("=======================\n\n")
            f.write(f"Research Goal: {goal}\n\n")
            f.write("Table of Contents\n========================\n\n")

        # --- TOC ---
        for i, paper in enumerate(summaries, 1):
            title = paper.get('title', f"Paper {i}")
            metadata = paper.get("metadata", {})

            meta_line = []  # reset meta_line correctly per paper
            if metadata.get("year"):
                meta_line.append(f"Year: {metadata['year']}")
            if metadata.get("journal"):
                meta_line.append(f"Journal: {metadata['journal']}")
            if metadata.get("authors"):
                meta_line.append(f"Authors: {metadata['authors']}")
            meta_line_str = " | ".join(meta_line)

            if format == "md":
                f.write(f"{i}. [{title}](#paper-{i})\n")
                if meta_line_str:
                    f.write(f"   - {meta_line_str}\n")
            else:
                f.write(f"{i}. {title}\n")
                if meta_line_str:
                    f.write(f"   - {meta_line_str}\n")

            chunks = paper.get("chunks", [])
            seen = set()
            for chunk in chunks:
                section_title = chunk.get('title', 'Untitled Section').strip()
                if section_title and section_title not in seen:
                    seen.add(section_title)
                    f.write(f"   - {section_title}\n")

        f.write("\n--- End of Table of Contents ---\n\n")

        # --- Full Summaries ---
        for i, paper in enumerate(summaries, 1):
            title = paper.get('title', f"Paper {i}")
            metadata = paper.get("metadata", {})

            meta_line = []  # reset meta_line again properly
            if metadata.get("year"):
                meta_line.append(f"Year: {metadata['year']}")
            if metadata.get("journal"):
                meta_line.append(f"Journal: {metadata['journal']}")
            if metadata.get("authors"):
                meta_line.append(f"Authors: {metadata['authors']}")
            meta_line_str = " | ".join(meta_line)

            if format == "md":
                f.write(f"## Paper {i}: {title}\n")
                if meta_line_str:
                    f.write(f"*{meta_line_str}*\n\n")
            else:
                f.write(f"Paper {i}: {title}\n")
                if meta_line_str:
                    f.write(f"{meta_line_str}\n")
                f.write("Summary:\n")

            f.write(paper.get("summary", "[No summary available]") + "\n\n")

    print(f"💾 Report saved as: {output_path}\n")
