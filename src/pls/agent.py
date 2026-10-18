from dataclasses import dataclass
import json
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")
client =  genai.Client(api_key=api_key)



@dataclass
class ProposedCommand:
    command: str | None
    explanation: str
    
def propose(prompt: str) -> ProposedCommand:
    # call model
    client = genai.Client()
    
    # build system instruction for model
    system_instruction = (
        "You translate English to terminal commands. Respond ONLY with a JSON object "
        "containing 'command' (string or null) and 'explanation' (string). If you "
        "cannot provide a command, set the 'command' field to null and fill in the explanation."
    )
    
    interaction = client.interactions.create(
        model = "gemini-3.5-flash-lite",
        input = prompt,
        generation_config={
            "system_instruction": system_instruction,
            "response_mime_type": "application/json"
        }
    )
    
    if interaction.output_text is None:
        raise ValueError("Gemini returned a completely empty response (None).")
    
    # load answer from model
    response_parsed = json.loads(interaction.output_text)

    # extract values from response
    return ProposedCommand(
        command=response_parsed.get("command"), 
        explanation=response_parsed.get("explanation", "")
    )
    


user_prompt = input("What do you want to do? ➔ ")
try:
    # 4. Pass the custom keyboard input directly to your function
    result = propose(user_prompt)
        
    # 5. Display the structured dataclass results
    print(f"📦 ProposedCommand Object Created:")
    print(f"   • Command:     {result.command}")
    print(f"   • Explanation: {result.explanation}")
    print("-" * 50 + "\n")            
except Exception as e:
    # If json.loads fails or the model returns bad data, it crashes here loudly
    print(f"💥 LOUD CRASH CAUGHT! Your function raised an error:")
    print(f"   Error Type: {type(e).__name__}")
    print(f"   Details:    {e}")
    print("-" * 50 + "\n")