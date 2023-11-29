from azure.data.tables import TableClient

class ReportRetreival:

    def __init__(self, client: TableClient) -> None:
        self.client = client

    def get_report(self, id: str, year: str):
        query = f"id eq '{id}' and year eq '{year}'"
        results = self.client.query_entities(query)
        for result in results:
            return result['report']
        return None
