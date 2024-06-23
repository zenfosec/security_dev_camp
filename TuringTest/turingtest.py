import os
import json
from openai import OpenAI
import argparse
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')) # remember to set your OpenAI API key as an environment variable

def query_chatgpt(code_block):
    prompt = f"""Analyze the following code and determine the likelihood that any part of it was generated by an AI language model. Return only a number between 0 and 100 representing the confidence percentage. Higher numbers indicate higher confidence that AI was involved in generating the code.

Code to analyze:
{code_block}

Confidence percentage:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you prefer, but tokens are limited
        messages=[
            {"role": "system", "content": "You are an AI code analyzer. Respond only with a number between 0 and 100."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,
        n=1,
        temperature=0.5,
    )

    confidence = response.choices[0].message.content.strip()
    try:
        return int(confidence)
    except ValueError:
        return None

def analyze_directory(directory):
    results = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                confidence = query_chatgpt(code)
                results[file_path] = confidence
                print(f"File: {file_path}, Confidence: {confidence}%")
    return results

def main():
    parser = argparse.ArgumentParser(description="Analyze Python files in a directory for AI-generated code.")
    parser.add_argument("directory", help="The directory to scan for .py files.")
    args = parser.parse_args()

    results = analyze_directory(args.directory)

    with open('output.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

    print("Results have been written to output.json")

if __name__ == "__main__":
    main()
