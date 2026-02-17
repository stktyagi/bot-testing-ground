import os
import xml.etree.ElementTree as ET
import google.generativeai as genai

def get_error():
    try:
        tree = ET.parse("report.xml")
        root = tree.getroot()
        for issue in root.iter():
            if issue.tag in ['failure', 'error']:
                return issue.text
    except:
        return "Log parsing failed."
    return "No error found."

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Skipping: No API Key found.")
        return

    genai.configure(api_key=api_key)
    
    error_log = get_error()
    with open("repo_context.xml", "r") as f:
        context = f.read()

    prompt = f"""
    Fix this failing test.
    ERROR: {error_log}
    CODE: {context}
    """

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    print(f"## AI Fix\n\n{response.text}")

if __name__ == "__main__":
    main()
