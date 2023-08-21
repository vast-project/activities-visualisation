import json


class DashboardData:
    @staticmethod
    def fetch_animals(**kwargs) -> str:
        data = {"giraffes": 20, "orangutans": 14, "monkeys": 23}

        return json.dumps(dict(
            data=[
                dict(
                    x=list(data.keys()),
                    y=list(data.values()),
                    type="bar",
                )
            ]
        ))
