from typing import Any, Dict

import httpx
import pandas as pd


def get_results(url: str, username: str, password: str) -> Dict[str, pd.DataFrame]:
    request_result = httpx.post(url, auth=(username, password))
    if request_result.status_code == 200:
        result_json = request_result.json().get("data", {})
        results_dict: Dict[Any, Any] = {}
        if isinstance(result_json, list):
            results_dict = {"data": pd.DataFrame.from_records(result_json)}
        elif isinstance(result_json, dict):
            for result_type, result_data in result_json.items():
                if isinstance(result_data, dict):
                    results_dict.update({result_type: pd.DataFrame.from_records([result_data])})
                else:
                    results_dict.update({result_type: pd.DataFrame.from_records(result_data)})
        return results_dict
    else:
        raise httpx.RequestError(f"{request_result.status_code=}, {request_result.json()=}")
