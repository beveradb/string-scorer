from sentence_transformers import CrossEncoder
from detoxify import Detoxify


class StringScorerInferencer:
    def __init__(self, logger, models, input_text):
        """
        Initializes the StringScorerInferencer with a list of models and input text.

        :param models: A list of model names to inference, e.g. ["vectara", "toxicity"]
        :param input_text: The input text to score, as a tuple
        """
        self.logger = logger
        self.models = models
        self.input_text = input_text

        self.logger.debug(f"Initializing StringScorerInferencer with models: {models} and input_text: {input_text}")

        self.model_functions_map = {
            "vectara": self.score_text_with_vectara,
            "toxicity": self.score_text_with_toxicity,
        }

    def run(self):
        """
        Processes the input text by calling a different method for each loaded model,
        returning a dict of scores returned by each model.

        :return: A dictionary of scores where keys are model names and values are their scores.
        """
        self.logger.debug("Running inference for selected models on input text.")
        scores = {}

        for model_name in self.models:
            self.logger.debug(f"Scoring text with model: {model_name}")
            scores[model_name] = self.model_functions_map[model_name](self.input_text)

        self.logger.debug(f"Scoring complete. Scores: {scores}")
        return scores

    def score_text_with_vectara(self, input_text):
        """
        Scores the input text with the 'hallucination_evaluation_model' model from the vectara library.

        :param input_text_pair: A tuple of input text to score.
        :return: A dictionary of scores where keys are model names and values are their scores.
        """
        self.logger.debug("Scoring text with Vectara model.")

        model = CrossEncoder("vectara/hallucination_evaluation_model")
        score = model.predict([input_text])

        self.logger.debug(f"Vectara model score: {score}")
        # Convert numpy float32 to Python float
        return float(score)

    def score_text_with_toxicity(self, input_text):
        """
        Scores the input text with the 'original' model from the unitaryai/detoxify library.

        :param input_text_pair: A tuple of input text to score.
        :return: A dictionary of scores where keys are model names and values are their scores.
        """
        self.logger.debug("Scoring text with Detoxify model.")

        results = Detoxify("original").predict(input_text)
        score = results["toxicity"]
        
        self.logger.debug(f"Detoxify model score: {score}")

        # Convert numpy float32 to Python float
        return float(score)
