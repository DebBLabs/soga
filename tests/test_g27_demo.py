import contextlib
import io
import unittest
from unittest import mock

from g27_tip_jar.demo import main


class G27DemoTests(unittest.TestCase):
    def run_demo(self, scenario):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main([scenario])
        self.assertEqual(result, 0, output.getvalue())
        self.assertIn("DEMONSTRATION PASSED", output.getvalue())
        return output.getvalue()

    def test_positive_demo_preserves_unknown_physical_outcome(self):
        output = self.run_demo("positive")
        self.assertIn("no invented physical success: unknown", output)
        self.assertIn("other target unchanged", output)

    def test_same_grant_collision_demo(self):
        output = self.run_demo("same-grant-race")
        self.assertIn("one replay rejection", output)

    def test_session_slot_collision_demo_leaves_loser_unused(self):
        output = self.run_demo("session-slot-race")
        self.assertIn("loser remains unused", output)

    def test_rejection_demo_stops_at_named_boundaries(self):
        output = self.run_demo("rejections")
        self.assertIn("wrong target exact stage", output)
        self.assertIn("changed replay exact stage", output)

    def test_safety_demo_preserves_latch_and_terminal_session(self):
        output = self.run_demo("safety")
        self.assertIn("halt defeats late ALLOW", output)
        self.assertIn("old session remains terminal", output)

    def test_interactive_flow_shows_pending_before_separate_allow(self):
        output = io.StringIO()
        commands = iter(["offer a", "scan", "request greet_participant", "status", "events", "allow", "events", "quit"])
        with contextlib.redirect_stdout(output), mock.patch("builtins.input", side_effect=lambda _prompt: next(commands)):
            result = main(["interactive"])
        self.assertEqual(result, 0)
        rendered = output.getvalue()
        self.assertIn("request received; state=pending", rendered)
        self.assertIn("operating state: pending", rendered)
        self.assertIn("01 request_received", rendered)
        self.assertIn("02 decision_received", rendered)
        self.assertIn("03 dispatch_recorded", rendered)
        self.assertIn("04 outcome_recorded", rendered)

    def test_interactive_flow_shows_safety_before_late_allow(self):
        output = io.StringIO()
        commands = iter(["offer a", "scan", "request greet_participant", "stop", "allow", "events", "quit"])
        with contextlib.redirect_stdout(output), mock.patch("builtins.input", side_effect=lambda _prompt: next(commands)):
            result = main(["interactive"])
        self.assertEqual(result, 0)
        rendered = output.getvalue()
        self.assertIn("safety stop latched", rendered)
        self.assertIn("governance arrived but was rejected", rendered)
        self.assertIn("01 request_received", rendered)
        self.assertIn("02 safety_halt", rendered)
        self.assertIn("03 decision_received", rendered)
        self.assertIn("04 decision_rejected", rendered)

    def test_interactive_rejects_second_request_while_first_is_pending(self):
        output = io.StringIO()
        commands = iter(["offer a", "scan", "request first", "request second", "quit"])
        with contextlib.redirect_stdout(output), mock.patch("builtins.input", side_effect=lambda _prompt: next(commands)):
            result = main(["interactive"])
        self.assertEqual(result, 0)
        self.assertIn("resolve or stop the current Pending request first", output.getvalue())


if __name__ == "__main__":
    unittest.main()
