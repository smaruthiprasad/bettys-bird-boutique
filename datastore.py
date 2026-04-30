import os
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine


def search(
    project_id: str,
    location: str,
    engine_id: str,
    search_query: str,
) -> list[str]:
    """Core search function using Vertex AI Search."""
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    client = discoveryengine.SearchServiceClient(client_options=client_options)

    serving_config = (
        f"projects/{project_id}/locations/{location}"
        f"/collections/default_collection/engines/{engine_id}"
        f"/servingConfigs/default_config"
    )

    content_search_spec = {
        "search_result_mode": (
            discoveryengine.SearchRequest.ContentSearchSpec
            .SearchResultMode.CHUNKS
        )
    }

    request = {
        "serving_config": serving_config,
        "query": search_query,
        "page_size": 10,
        "content_search_spec": content_search_spec,
        "query_expansion_spec": {
            "condition": (
                discoveryengine.SearchRequest.QueryExpansionSpec
                .Condition.AUTO
            ),
        },
        "spell_correction_spec": {
            "mode": (
                discoveryengine.SearchRequest.SpellCorrectionSpec
                .Mode.AUTO
            ),
        },
    }

    page_result = client.search(request)

    results = []
    for result in page_result:
        if result.chunk and result.chunk.content:
            results.append(result.chunk.content)

    return results


def datastore_search_tool(search_query: str) -> str:
    """
    Searches Betty's Bird Boutique documents for store information
    including hours, location, history, and staff details.

    Args:
        search_query (str): What information about Betty's Bird Boutique
                           the customer is looking for
    """
    try:
        results = search(
            project_id=os.environ.get("DATASTORE_PROJECT_ID"),
            engine_id=os.environ.get("DATASTORE_ENGINE_ID"),
            location=os.environ.get("DATASTORE_LOCATION", "global"),
            search_query=search_query,
        )
        if not results:
            return "No results found in store documents."
        return "\n\n".join(results)
    except Exception as e:
        return f"A problem occurred searching store documents: {e}"
