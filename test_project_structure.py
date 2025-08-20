import unittest
from pathlib import Path

ROOT = Path(__file__).parent

class ProjectStructureTests(unittest.TestCase):
    def test_task_definitions_exist(self):
        task_py = (ROOT / 'Task.py').read_text(encoding='utf-8')
        # Ensure key task variables are defined
        self.assertIn('plan = Task(', task_py)
        self.assertIn('write = Task(', task_py)
        self.assertIn('edit = Task(', task_py)

    def test_agents_definitions_exist(self):
        agents_py = (ROOT / 'Agents.py').read_text(encoding='utf-8')
        # Ensure key agent variables are defined
        self.assertIn('planner = Agent(', agents_py)
        self.assertIn('writer = Agent(', agents_py)
        self.assertIn('editor = Agent(', agents_py)

    def test_crew_file_references(self):
        crew_py = (ROOT / 'Article_Writer_Crew.py').read_text(encoding='utf-8')
        # Ensure Crew is instantiated and kickoff is called in main guard
        self.assertIn('crew = Crew(', crew_py)
        self.assertIn("if __name__ == \"__main__\":", crew_py)
        self.assertIn('crew.kickoff', crew_py)

if __name__ == '__main__':
    unittest.main()