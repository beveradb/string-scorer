import subprocess
import requests
import time


def start_application():
    """
    Starts the application by invoking the Poe 'start' task.
    It then waits up to 30 seconds for the application to become responsive.
    """
    subprocess.Popen(["poe", "start"])
    for _ in range(30):  # Try for 30 seconds
        try:
            response = requests.get("http://localhost:54321/")
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            pass
        time.sleep(1)


def stop_application():
    """
    Stops the application by invoking the Poe 'stop' task.
    This is used to clean up after tests are run.
    """
    subprocess.Popen(["poe", "stop"])


def test_score_text_endpoint():
    """
    Tests the 'score_text' endpoint of the application.
    It starts the application, sends requests with text to be scored,
    and asserts the correctness of the response.
    """
    start_application()

    try:
        with open("tests/integration/fixtures/sentences.txt", "r") as file:
            sentences = file.readlines()

        for sentence in sentences:
            response = requests.post("http://localhost:54321/score_text", json={"text": sentence.strip()})

            assert response.status_code == 200
            assert isinstance(response.json(), dict), "Response should be a JSON object"
            assert "toxicity" in response.json(), "Response JSON should include 'toxicity' key"
            assert "vectara" in response.json(), "Response JSON should include 'vectara' key"
            assert isinstance(response.json()["toxicity"], float), "'toxicity' value should be a float"
            assert isinstance(response.json()["vectara"], float), "'vectara' value should be a float"
            assert 0 <= response.json()["toxicity"] <= 1, "'toxicity' value should be between 0 and 1"
            assert 0 <= response.json()["vectara"] <= 1, "'vectara' value should be between 0 and 1"

    finally:
        stop_application()
