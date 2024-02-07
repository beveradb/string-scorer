import unittest
from unittest.mock import patch, MagicMock
from string_scorer.inference import StringScorerInferencer


class TestStringScorerInferencer(unittest.TestCase):

    @patch("string_scorer.inference.CrossEncoder")
    @patch("string_scorer.inference.Detoxify")
    def setUp(self, MockDetoxify, MockCrossEncoder):
        """Set up the test environment by mocking dependencies and initializing the StringScorerInferencer."""
        self.mock_logger = MagicMock()
        self.models = ["vectara", "toxicity"]
        self.input_text = "test text"
        self.inferencer = StringScorerInferencer(self.mock_logger, self.models, self.input_text)

    def test_initialization(self):
        """Test the initialization of StringScorerInferencer to ensure it correctly sets up models and input_text."""
        self.assertEqual(self.inferencer.models, self.models)
        self.assertEqual(self.inferencer.input_text, self.input_text)
        self.mock_logger.debug.assert_called()

    @patch("string_scorer.inference.CrossEncoder.predict", return_value=0.5)
    @patch("string_scorer.inference.Detoxify.predict", return_value={"toxicity": 0.7})
    def test_run(self, mock_detoxify_predict, mock_crossencoder_predict):
        """Test the run method to ensure it correctly predicts scores using the mocked models and aggregates them."""
        scores = self.inferencer.run()
        expected_scores = {"vectara": 0.5, "toxicity": 0.7}

        self.assertEqual(scores, expected_scores)
        self.mock_logger.debug.assert_called()
        mock_crossencoder_predict.assert_called_once_with([self.input_text])
        mock_detoxify_predict.assert_called_once_with(self.input_text)

    @patch("string_scorer.inference.CrossEncoder.predict", return_value=0.5)
    def test_score_text_with_vectara(self, mock_predict):
        """Test scoring with the Vectara model to ensure it correctly predicts and returns the score for given text."""
        score = self.inferencer.score_text_with_vectara(self.input_text)
        self.assertEqual(score, 0.5)
        mock_predict.assert_called_once_with([self.input_text])

    @patch("string_scorer.inference.Detoxify.predict", return_value={"toxicity": 0.7})
    def test_score_text_with_toxicity(self, mock_predict):
        """Test scoring with the Toxicity model to ensure it correctly predicts and returns the toxicity score."""
        score = self.inferencer.score_text_with_toxicity(self.input_text)
        self.assertEqual(score, 0.7)
        mock_predict.assert_called_once_with(self.input_text)


if __name__ == "__main__":
    unittest.main()
