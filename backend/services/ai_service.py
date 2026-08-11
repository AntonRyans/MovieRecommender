import json
import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5-mini"
)


SYSTEM_PROMPT = """
You are Movie Compass AI.

You are a movie assistant.

You have two main capabilities:

1. RECOMMEND MOVIES

Understand what the user wants and convert their request
into structured movie-search criteria.

2. GUESS MOVIES

The user may describe a movie without giving its title.
Identify the most likely movie.

You must never invent movie metadata.

TMDB will be used by the application to verify movie information.

Return JSON only.

For recommendations use:

{
    "intent": "recommend",
    "query": "...",
    "genres": [],
    "min_year": null,
    "max_year": null,
    "max_runtime": null,
    "min_rating": null
}

For guessing use:

{
    "intent": "guess",
    "movie_title": "...",
    "alternative_titles": [],
    "confidence": 0.0
}

If you cannot confidently identify the movie,
use the most likely candidate and lower the confidence.

Keep the response concise.
"""


def analyse_message(
    message,
    conversation=None
):

    history = conversation or []

    conversation_text = ""

    for item in history:

        conversation_text += (
            f"{item['role']}: "
            f"{item['message']}\n"
        )

    prompt = f"""
Previous conversation:

{conversation_text}

Current user message:

{message}

Analyse the current request.
"""

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=prompt
    )

    text = response.output_text.strip()

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        return {
            "intent": "recommend",
            "query": message,
            "genres": [],
            "min_year": None,
            "max_year": None,
            "max_runtime": None,
            "min_rating": None
        }

from services.tmdb_service import (
    discover_movies,
    search_movies,
    get_movie
)


def recommend_from_request(analysis):

    query = analysis.get("query")

    genres = analysis.get(
        "genres",
        []
    )

    min_year = analysis.get(
        "min_year"
    )

    max_year = analysis.get(
        "max_year"
    )

    max_runtime = analysis.get(
        "max_runtime"
    )

    min_rating = analysis.get(
        "min_rating"
    )

    # ------------------------------------------------
    # If there is a specific movie/title reference
    # ------------------------------------------------

    if query:

        search_result = search_movies(query)

        movies = search_result.get(
            "results",
            []
        )

        if movies:

            return movies[:6]

    # ------------------------------------------------
    # Otherwise use TMDB discovery
    # ------------------------------------------------

    results = discover_movies(
        genre_ids=genres,
        min_year=min_year,
        max_year=max_year,
        max_runtime=max_runtime,
        min_rating=min_rating
    )

    return results.get(
        "results",
        []
    )[:6]


def guess_from_request(analysis):

    title = analysis.get(
        "movie_title"
    )

    alternatives = analysis.get(
        "alternative_titles",
        []
    )

    candidates = []

    if title:

        results = search_movies(title)

        candidates.extend(
            results.get("results", [])[:3]
        )

    for alternative in alternatives:

        results = search_movies(
            alternative
        )

        candidates.extend(
            results.get("results", [])[:2]
        )

    # Remove duplicate movies

    unique = {}

    for movie in candidates:

        movie_id = movie.get("id")

        if movie_id:
            unique[movie_id] = movie

    return list(unique.values())[:5]