from __future__ import annotations
import json
from pathlib import Path
import typer
from rich import print
from src.reflexion_lab.agents import ReActAgent, ReflexionAgent
from src.reflexion_lab.reporting import build_report, save_report
from src.reflexion_lab.utils import load_dataset, save_jsonl
app = typer.Typer(add_completion=False)

import concurrent.futures
from rich.progress import track

@app.command()
def main(dataset: str = "data/hotpotqa.json", out_dir: str = "outputs/sample_run", reflexion_attempts: int = 3, workers: int = 3) -> None:
    examples = load_dataset(dataset)
    react = ReActAgent()
    reflexion = ReflexionAgent(max_attempts=reflexion_attempts)
    
    print(f"[bold cyan]Running ReAct Agent with {workers} workers...[/bold cyan]")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        react_records = list(track(executor.map(react.run, examples), total=len(examples), description="ReAct"))
        
    print(f"[bold cyan]Running Reflexion Agent with {workers} workers...[/bold cyan]")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        reflexion_records = list(track(executor.map(reflexion.run, examples), total=len(examples), description="Reflexion"))
        
    all_records = react_records + reflexion_records
    out_path = Path(out_dir)
    save_jsonl(out_path / "react_runs.jsonl", react_records)
    save_jsonl(out_path / "reflexion_runs.jsonl", reflexion_records)
    report = build_report(all_records, dataset_name=Path(dataset).name, mode="llm")
    json_path, md_path = save_report(report, out_path)
    print(f"[green]Saved[/green] {json_path}")
    print(f"[green]Saved[/green] {md_path}")
    print(json.dumps(report.summary, indent=2))

if __name__ == "__main__":
    app()
