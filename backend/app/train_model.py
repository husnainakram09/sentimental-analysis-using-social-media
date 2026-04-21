from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from .config import get_settings
from .utils.preprocessing import clean_tweet


def load_training_data() -> pd.DataFrame:
    dataset_path = Path("data/train.csv")
    if dataset_path.exists():
        df = pd.read_csv(dataset_path)
        required = {"text", "label"}
        if not required.issubset(df.columns):
            raise ValueError("train.csv must contain 'text' and 'label' columns")
        return df[["text", "label"]]

    return pd.DataFrame(
        {
            "text": [
                "I love this product",
                "This is terrible",
                "It is okay, nothing special",
                "Amazing experience and very good service",
                "Worst thing ever",
                "The event was average",
                "I am so happy with the result",
                "I hate this app",
                "The update is fine",
                "Not bad at all",
                "Very disappointing service",
                "This made my day",
            ],
            "label": [2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 2],
        }
    )


def train_and_save_model() -> None:
    settings = get_settings()
    data = load_training_data()

    model = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    preprocessor=clean_tweet,
                    ngram_range=(1, 2),
                    max_features=50000,
                    min_df=1,
                    stop_words="english",
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                ),
            ),
        ]
    )

    model.fit(data["text"], data["label"])
    output_path = Path(settings.sentiment_model_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    print(f"Model saved to {output_path}")


if __name__ == "__main__":
    train_and_save_model()
