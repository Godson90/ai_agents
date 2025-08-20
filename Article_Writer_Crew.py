import os
import pathlib
import warnings
from Task import *
from crewai import Crew, Process
from Helper import slugify
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown
warnings.filterwarnings("ignore")   # warning control

crew = Crew(
    agents=[planner, writer_agent, editor_agent],   # all Agents
    tasks=[plan_task, write_task, edit_task], # all Tasks
    process=Process.sequential,
    verbose=False,
)

if __name__ == "__main__":
    topic = input("What topic do you wish to write? ")
    write_choice = input("Write result to file? (y/n): ")

    result = crew.kickoff(inputs={"topic": topic})
    # Ensure we have a string to write/print
    result_str = result if isinstance(result, str) else str(result)

   # print(result_str)
    Console().print(Markdown(result_str))

    if write_choice.strip().lower() in {"y", "yes", "1", "true", "t"}:
        try:
            # Target directory (Windows)
            target_dir = Path(r"C:\Workspace\AI_Agents\Result")
            target_dir.mkdir(parents=True, exist_ok=True)

            # Build a safe filename: YYYYMMDD_HHMMSS_<topic>.MD
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"{ts}_{slugify(topic)}.MD"
            out_path = target_dir / fname

            # Optional: add a simple header to the markdown
            header = f"# {topic}\n\n*Generated:* {datetime.now().isoformat()}\n\n"
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(header)
                f.write(result_str)

            print(f"\nSaved to: {out_path}")
        except OSError as e:
            print(f"\n[WARN] Could not write file: {e}")
