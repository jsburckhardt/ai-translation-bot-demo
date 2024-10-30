from openai import AzureOpenAI
import os
import time
from models.translate import TranslateRequest, TranslateResponse


# Language code to language name mapping
language_map = {
    'zh-Hans': 'Chinese (Simplified)',
    'en': 'English',
    'es': 'Spanish',
    'ja': 'Japanese'
}


def translate_text(client, deployment_id, source_language, target_language, source_text):
    """
    Translates the provided text from the source language to the target language using Azure OpenAI.

    Args:
        client: The AzureOpenAI client object.
        deployment_id: The deployment ID of the Azure OpenAI model.
        source_language: The language to translate from.
        target_language: The language to translate to.
        source_text: The text to be translated.

    Returns:
        response: The translation response from the Azure OpenAI model.
    """

    try:
        response = client.chat.completions.create(
            model=deployment_id,
            messages=[
                {
                    'role': 'system',
                    'content': '''You are a translator. YOU ONLY TRANSLATE. You are asked to translate the text you receive from {source_language} to {target_language}.
    The translation should avoid the following issues:
    - Distortion: An element of meaning in the source text is altered in the target text.
    - Unjustified omission: An element of meaning in the source text is not transferred into the target text.
    - Unjustified addition: An element of meaning that does not exist in the source text is added to the target text.
    - Inappropriate register: Incorrect variety of language or inappropriate vocabulary for the text type (e.g. inappropriate level of formality or informality).
    - Unidiomatic expression: An expression sounding unnatural or awkward to a native speaker irrespective of the context in which the expression is used, but the intended meaning can be understood.
    - Error of grammar, syntax, spelling or punctuation.'''.format(source_language=source_language, target_language=target_language)
                },
                {
                    'role': 'user',
                    'content': source_text
                }
            ],
            max_tokens=4096,
            temperature=0.5,
        )

        return response

    except Exception as e:
        print(f"Error during translation: {e}")
        return None


async def translate(request: TranslateRequest) -> TranslateResponse:
    client = AzureOpenAI(
        azure_endpoint=os.getenv('OPENAI_API_BASE'),
        api_key=os.getenv('OPENAI_API_KEY'),
        api_version='2024-02-01',
    )
    deployment_id = os.getenv('OPENAI_DEPLOYMENT_ID')

    source_language = language_map[request.source_language]
    target_language = language_map[request.target_language]

    response = translate_text(
        client, deployment_id, source_language, target_language, request.source_text)

    return TranslateResponse(
        target_text=response.choices[0].message.content,
    )