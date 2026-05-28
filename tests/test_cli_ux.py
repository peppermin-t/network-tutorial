import contextlib
import io
import unittest

from netlab.cli import main


class CliUxTest(unittest.TestCase):
    def test_doctor_does_not_require_optional_tools(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["doctor"])

        self.assertEqual(code, 0)
        self.assertIn("python=", output.getvalue())
        self.assertIn("tshark=", output.getvalue())
        self.assertIn("docker=", output.getvalue())
        self.assertIn("recommended_start=python -m netlab path tutorial", output.getvalue())
        self.assertIn("recommended_first_lab=python labs/week01-ip-routing-subnetting/experiment.py", output.getvalue())
        self.assertNotIn("server tcp-echo", output.getvalue())

    def test_path_tutorial_outputs_full_course(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["path", "tutorial"])

        self.assertEqual(code, 0)
        self.assertIn("Week00", output.getvalue())
        self.assertIn("Week12", output.getvalue())

    def test_path_ai_outputs_fast_track(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["path", "ai"])

        self.assertEqual(code, 0)
        self.assertIn("Week12", output.getvalue())

    def test_path_design_outputs_design_path(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["path", "design"])

        self.assertEqual(code, 0)
        self.assertIn("Week01", output.getvalue())
        self.assertIn("Week12", output.getvalue())

    def test_path_vpn_outputs_path(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["path", "vpn"])

        self.assertEqual(code, 0)
        self.assertIn("Week11", output.getvalue())

    def test_concept_tcp_outputs_summary(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["concept", "tcp"])

        self.assertEqual(code, 0)
        self.assertIn("byte stream", output.getvalue())

    def test_concept_vpn_outputs_summary(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["concept", "vpn"])

        self.assertEqual(code, 0)
        self.assertIn("route table", output.getvalue())

    def test_common_concepts_have_cli_summaries(self) -> None:
        for concept in ("ip", "cidr", "route", "nat", "firewall", "tls", "http"):
            with self.subTest(concept=concept):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    code = main(["concept", concept])

                self.assertEqual(code, 0)
                self.assertIn(concept, output.getvalue())

    def test_unknown_concept_returns_nonzero_without_crashing(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["concept", "unknown"])

        self.assertEqual(code, 1)
        self.assertIn("available=", output.getvalue())


if __name__ == "__main__":
    unittest.main()
