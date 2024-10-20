from typing import Dict, Callable
import importlib
import pandas as pd

from models.poll_model import PollModel
from models import weighting_methods
from models.plotting import plot_results
from config import WEIGHTING_METHODS, DATA_PATHS, OUTPUT_PATH


def load_weighting_methods() -> Dict[str, Callable]:
    return {name: getattr(weighting_methods, method_name)
            for name, method_name in WEIGHTING_METHODS.items()}

def run_model_with_method(model: PollModel, method: Callable) -> pd.DataFrame:
    return model.run_time_series([method])

def main():
    try:
        model = PollModel(DATA_PATHS['polls'], DATA_PATHS['pollster_ratings'])
        weighting_methods_dict = load_weighting_methods()

        results = {name: run_model_with_method(model, method)
                   for name, method in weighting_methods_dict.items()}

        plot_results(results, OUTPUT_PATH)

        # print summary stats
        for name, df in results.items():
            print(f"\nSummary for {name} weighting:")
            print(df[['Harris', 'Trump', 'Harris_Trump_Difference']].describe())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
