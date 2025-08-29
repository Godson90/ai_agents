import os
import warnings
from pathlib import Path
from datetime import datetime
from Helper import *
from crewai import Crew, Process
from rich.console import Console
from rich.markdown import Markdown
from Agents import Agents
from Task import ContentTasks

warnings.filterwarnings("ignore")
# ---- build agents once ----
agents = Agents()
planner = agents.planner()
writer  = agents.writer()
editor  = agents.editor()

# ---- build tasks once (from the same factory) ----
plan_task  = ContentTasks().plan_task
write_task = ContentTasks().write_task
edit_task  = ContentTasks().edit_task

# Normalize contexts to the actual instances we will pass to Crew
# (Some task factories recreate tasks internally; this ensures the right wiring.)
try:
    write_task.context = [plan_task]
except Exception:
    pass
try:
    edit_task.context = [write_task]
except Exception:
    pass

# ---- assemble Crew ----
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan_task, write_task, edit_task],
    process=Process.sequential,
    verbose=False,
)

if __name__ == "__main__":
    # sanity check for API key (avoids confusing network errors later)
    if not os.getenv("OPENAI_API_KEY"):
        print("[WARN] OPENAI_API_KEY is not set in the environment.")

    topic = input("What topic do you wish to write? ")
    write_choice = input("Write result to file? (y/n): ").strip().lower()

    try:
        result = crew.kickoff(inputs={"topic": topic})
    except Exception as e:
        # surface a concise error and exit
        print(f"[ERROR] Crew run failed: {e}")
        raise

    # Ensure printable string
    result_str = result if isinstance(result, str) else str(result)

    # Pretty terminal preview
    Console().print(Markdown(result_str))

    # Optional write-to-file
    if write_choice in {"y", "yes", "1", "true", "t"}:
        try:
            target_dir = Path(r"C:\Workspace\CrewAI\Result")
            target_dir.mkdir(parents=True, exist_ok=True)

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"{ts}_{slugify(topic)}.md"  # use .md (lowercase is conventional)
            out_path = target_dir / fname

            header = f"# {topic}\n\n*Generated:* {datetime.now().isoformat()}\n\n"
            out_path.write_text(header + result_str, encoding="utf-8")

            print(f"\nSaved to: {out_path}")
        except OSError as e:
            print(f"\n[WARN] Could not write file: {e}")

