"""Testes mínimos para impedir uma configuração aparentemente verde e vazia."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from create_jira_tasks import TASKS


ROOT = Path(__file__).resolve().parents[1]


class RepositorySetupTests(unittest.TestCase):
    """Valida contratos básicos da configuração inicial."""

    def test_required_documentation_exists(self) -> None:
        required = (
            "constitution.md",
            "docs/ai_development_workflow.md",
            "docs/software_setup.md",
            "docs/development_best_practices.md",
            "docs/github_jira_workflow.md",
        )
        missing = [path for path in required if not (ROOT / path).is_file()]
        self.assertEqual([], missing)

    def test_jira_task_definitions_are_complete_and_unique(self) -> None:
        self.assertEqual(8, len(TASKS))
        self.assertEqual(8, len({task.person for task in TASKS}))
        self.assertEqual(8, len({task.summary for task in TASKS}))

    def test_jira_member_example_covers_the_whole_team(self) -> None:
        member_example = json.loads(
            (ROOT / "jira_members.example.json").read_text(encoding="utf-8")
        )
        self.assertEqual({task.person for task in TASKS}, set(member_example))

    def test_numpy_is_bounded_below_version_two(self) -> None:
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("numpy>=1.24.0,<2.0", requirements)

    def test_env_example_contains_only_placeholders_for_tokens(self) -> None:
        env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("JIRA_API_TOKEN=your_jira_api_token_here", env_example)
        self.assertIn("DEEPSEEK_API_KEY=your_deepseek_api_key_here", env_example)


if __name__ == "__main__":
    unittest.main()
