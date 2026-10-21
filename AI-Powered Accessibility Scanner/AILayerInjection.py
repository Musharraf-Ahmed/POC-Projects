from importlib import import_module

Portkey = import_module("portkey_ai").Portkey

def explain_issue(rule, description):

    prompt = f"""
        Explain this accessibility violation.
    
        Rule: {rule}
    
        Description:
        {description}
    
        Give:
        1. Issue
        2. Impact
        3. WCAG Reference
        4. Suggested Fix
        """
    
    portkey = Portkey(
       base_url = "https://portkeygateway.perficient.com/v1",
       api_key = "myr2tBJ3n1F9WsXBeDDLa50bgZxQ")
       
    response = portkey.chat.completions.create(
       model = "@azure-openai/anthropic.claude-3-7-sonnet@20250219",
       messages = [
         {"role": "system", "content": "You are a helpful assistant."},
         {"role": "user", "content": prompt}
       ],
       MAX_TOKENS = 512)

    explanation = response.choices[0].message.content

    print(explanation)
    return explanation