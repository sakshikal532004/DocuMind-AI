# import os
# import time
# import ollama
# from dotenv import load_dotenv
# from google import genai

# from embeddings import retrieve

# load_dotenv()

# client = genai.Client(
#     api_key=os.getenv("GOOGLE_API_KEY")
# )


# def ask_pdf(question, history=""):

#     context = retrieve(question)

#     prompt = f"""
# You are an intelligent AI PDF Assistant.

# Use previous conversation if needed.

# Previous Conversation:
# {history}

# Context from PDF:
# {context}

# Current Question:
# {question}

# Instructions:
# 1. Answer ONLY from the PDF context.
# 2. If the answer is not present in the context, say:
# "I couldn't find this information in the uploaded PDFs."
# 3. Explain clearly and simply.
# 4. Use previous conversation if the current question depends on it.

# Answer:
# """

#     for attempt in range(3):

#         try:

#             response = client.models.generate_content(
#                 model="gemini-2.0-flash",
#                 contents=prompt
#             )

#             return "⚡ Powered by Gemini\n\n" + response.text

#         except Exception as e:

#             error_message = str(e)

#             # Quota Exceeded
#             if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

#                 print("Gemini quota exceeded. Switching to Ollama...")

#                 response = ollama.chat(
#                     model="llama3.2:3b",
#                     messages=[
#                         {
#                             "role": "user",
#                             "content": prompt
#                         }
#                     ]
#                 )

#                 return (
#                     "⚡ Powered by Local AI (Ollama)\n\n"
#                     + response["message"]["content"]
#                 )

#             # Server Busy
#             elif "503" in error_message or "UNAVAILABLE" in error_message:

#                 if attempt < 2:

#                     time.sleep(5)

#                 else:

#                     print("Gemini server busy. Switching to Ollama...")

#                     response = ollama.chat(
#                         model="llama3.2:3b",
#                         messages=[
#                             {
#                                 "role": "user",
#                                 "content": prompt
#                             }
#                         ]
#                     )

#                     return (
#                         "⚡ Powered by Local AI (Ollama)\n\n"
#                         + response["message"]["content"]
#                     )

#             # Any Other Error
#             else:

#                 try:

#                     print("Gemini error. Switching to Ollama...")

#                     response = ollama.chat(
#                         model="llama3.2:3b",
#                         messages=[
#                             {
#                                 "role": "user",
#                                 "content": prompt
#                             }
#                         ]
#                     )

#                     return (
#                         "⚡ Powered by Local AI (Ollama)\n\n"
#                         + response["message"]["content"]
#                     )

#                 except Exception as ollama_error:

#                     return (
#                         "❌ Gemini and Ollama both failed.\n\n"
#                         f"Gemini Error:\n{error_message}\n\n"
#                         f"Ollama Error:\n{str(ollama_error)}"
#                     )


import os
import time
import ollama
from dotenv import load_dotenv
from google import genai

from embeddings import retrieve

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def ask_pdf(question, history=""):

    context = retrieve(question)

    prompt = f"""
You are an intelligent AI PDF Assistant.

Use previous conversation if needed.

Previous Conversation:
{history}

Context from PDF:
{context}

Current Question:
{question}

Instructions:
1. Answer ONLY from the PDF context.
2. If the answer is not present in the context, say:
"I couldn't find this information in the uploaded PDFs."
3. Explain clearly and simply.
4. Use previous conversation if the current question depends on it.

Answer:
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            return "⚡ Powered by Gemini\n\n" + response.text

        except Exception as e:

            error_message = str(e)

            # Retry if Gemini server busy
            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < 2:
                    time.sleep(5)
                    continue

            # Local laptop pe Ollama fallback
            if os.path.exists("C:\\Users"):

                try:

                    response = ollama.chat(
                        model="llama3.2:3b",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    return (
                        "⚡ Powered by Local AI (Ollama)\n\n"
                        + response["message"]["content"]
                    )

                except Exception:
                    pass

            # Streamlit Cloud ya final error
            return f"""
❌ AI service unavailable.

Gemini Error:
{error_message}

Possible reasons:
• Invalid GOOGLE_API_KEY
• API quota exceeded
• Temporary server issue

Please try again later.
"""