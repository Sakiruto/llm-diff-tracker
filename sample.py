import json

def json_to_markdown(input_file="sample.json", output_file="output.md"):
    """Reads a JSON file and converts it into a structured Markdown file."""

    # Load JSON data from file
    with open(input_file, "r", encoding="utf-8") as file:
        json_obj = json.load(file)

    md_content = "# Project Breakdown\n\n"

    for epic in json_obj.get("epics", []):
        md_content += f"## Epic: {epic['epic']}\n\n"

        for story in epic.get("user_stories", []):
            md_content += f"### User Story: {story['overview']}\n"
            md_content += f"**Request:** {story['request']}\n\n"
            md_content += f"**Acceptance Criteria:** {story['acceptance_criteria']}\n\n"
            md_content += f"**Priority:** {story['priority']}\n\n"
            md_content += f"**Labels:** {story['labels']}\n\n"
            
            md_content += "#### Tasks:\n"
            for task in story.get("tasks", []):
                md_content += f"- **Task:** {task['task']}\n"
                md_content += f"  - **Description:** {task['description']}\n"
                md_content += f"  - **Priority:** {task['priority']}\n"
                md_content += f"  - **Labels:** {task['labels']}\n\n"

        md_content += "---\n\n"

    # Write the markdown content to a file
    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)
    
    print(f"Markdown file generated: {output_file}")

# Convert JSON to Markdown
json_to_markdown()
