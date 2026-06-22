from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file
print(os.getenv("GOOGLE_API_KEY"))  # Print the value of GOOGLE_API_KEY