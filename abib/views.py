from django.shortcuts import render, redirect
# import openai
# from .apikey_max import API_KEY

import google.generativeai as genai
from django.http import JsonResponse
import os
import markdown

# openai.api_key = API_KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create your views here.

def index(request):
    
    if request.method == "GET":
        return render(request, "abib/index.html", {})
    
    response = ""
    user_prompt = request.POST.get('prompt', '')
    try:
        # system_prompt = "only engage with biblical-related queries, controversial question should be answered by the various opinion"
        system_prompt = "only engage in scientific related question or queries"
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_prompt)

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_prompt)
        response_text = response.text
        response_text = markdown.markdown(response_text)

        # response = model.generate_content(prompt)
        # j = JsonResponse({'result': response.text})
    except Exception as e:
        response_text = f"Error: {str(e)}"
        
    return render(request, "abib/index.html", {'message': response_text})
    # response = openai.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "Write a poem about the ocean."}
    #     ],
    #     temperature=0.7,
    #     max_tokens=150,
    # )
    # response = openai.completions.create(
    #     model="text-davinci-003",
    #     prompt="Write a poem about the ocean.",
    #     temperature=0.7,
    #     max_tokens=150,
    # )

    # formatted_response = response['choices'][0]['message']['content']
    # return render(request, "abib/index.html", {'message': formatted_response})
    
    