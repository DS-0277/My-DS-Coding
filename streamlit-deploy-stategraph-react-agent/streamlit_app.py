"""Cloud-friendly launcher for the State-Graph ReAct Agent assignment.

Streamlit Community Cloud currently splits the original assignment path at its
spaces while it installs dependencies.  This launcher lives in a short,
space-free directory and then starts the original application unchanged.
"""

from pathlib import Path
import runpy
import sys


PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
    / "Fall 2026"
    / "Assignment - State-Graph ReAct Agent with Short-Term Memory, Cycle Bounds & Human-in-the-Loop (HITL) - AD331 (Week 8)"
    / "stategraph-react-agent"
)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

runpy.run_path(str(PROJECT_ROOT / "streamlit_app.py"), run_name="__main__")
