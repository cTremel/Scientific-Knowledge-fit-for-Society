import openai

# Set up your OpenAI API key
api_key = "YOUR_OPENAI_API_KEY"
openai.api_key = api_key

def generate_text(prompt):
# Call the OpenAI API to generate text based on the prompt
    response = openai.Completion.create(
        engine="text-davinci-002", # You can choose a different engine if needed
        prompt=prompt,
        max_tokens=100 # You can adjust this to control the length of the generated text
    )

    # Extract the generated text from the API response
    generated_text = response.choices[0].text.strip()
    return generated_text

# Example prompt
prompt = "Please extract Entities from: 'Human activities, principally through emissions of greenhouse gases, have unequivocally caused global warming, with global surface temperature reaching 1.1°C above 1850–1900 in 2011–2020.'"
generated_text = generate_text(prompt)
print(generated_text)