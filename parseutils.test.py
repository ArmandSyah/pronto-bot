import unittest
import parseutils


class TestParseUtils(unittest.TestCase):
    def test_parse_direct_mentions(self):
        mentioned_message = "<@UA29HP8H2> hello"
        user_id, message = parseutils.parse_direct_mention(mentioned_message)
        self.assertEqual(user_id, "UA29HP8H2")
        self.assertEqual(message, "hello")

    def test_parse_question_and_answer(self):
        message = "[Why did the chicken cross the road] (To get to the other side)"
        question, answer = parseutils.parse_question_answer(message)
        self.assertEqual(question, 'Why did the chicken cross the road')
        self.assertEqual(answer, 'To get to the other side')


if __name__ == "__main__":
    unittest.main()
