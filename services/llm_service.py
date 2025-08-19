from google import genai
from google.genai import types
import os
from config import Settings
from typing import List

settings = Settings()

class LLMService:
    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )
        self.model = "gemini-2.5-pro"  # Model name as a string

    def generate_response(self, query: str, search_results: List[dict]) -> str:
        # Format search results as context
        context_text = "\n\n".join([
            f"Source {i+1} ({result['url']}):\n{result['content']}"
            for i, result in enumerate(search_results)
        ])

        full_prompt = f"""
        Context from web search:
        {context_text}

        Query: {query}

        Please provide a comprehensive, detailed, well-cited, and accurate response using the above context.
        Think and reason deeply. Ensure it answers the query the user is asking.
        Do not use your own knowledge unless absolutely necessary.
        """

        # Create Gemini input structure
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=full_prompt)],
            )
        ]

        # Generate content
        # response = self.client.models.generate_content(
        #     model=self.model,
        #     contents=contents,
        #     stream = True
        # )

        # for chunk in response:
        #     yield chunk.text
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=-1),
            # Optional: Add tools if needed
        )
        try:
            # response = self.client.models.generate_content(
            # model=self.model,
            # contents=contents,
            # stream = True
            # )
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                if hasattr(chunk, "text"):
                    yield chunk.text
        except Exception as e:
            print("Error in generate_response:", e)
            yield "An error occurred while generating a response."

       
