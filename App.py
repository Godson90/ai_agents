from rich.console import Console
from rich.markdown import Markdown

text = open(r"C:\Workspace\AI_Agents\Result\20250818_135852_AI_Security.MD", encoding="utf-8").read()
Console().print(Markdown(text))