# import requests
# import json
# import sseclient

import openai
import spacy

import os
import openai
openai.api_key = "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"
# openai.Model.list()

#assert "openai" in openai_secret_manager.get_services()
# secrets = openai_secret_manager.get_secret("openai")

# api_key = secrets["API_Key_SP"]

# openai.api_key = api_key
api = openai.api_key

spacy.prefer_gpu()
nlp = spacy.load("en_core_web_sm")


# essay_prompt should also include the "grade level" at which it should be evaluated
# also, essay_prompt should specify that the response should be in prose
def gpt_response(essay_prompt, user_response):
      p_n = 50
      sim_threshold = 0.8        
      gpt_response = ""     
      response = openai.Completion.create(
            engine = "text-davinci-002",
            prompt = essay_prompt,
            max_tokens = 2048,
            n = p_n,
            temperature = 0.8,
            stop = None
      )
      # calculate average of top quartile of scores
      gpt_answer_scores = []
      for answer in response:
            gpt_answer_scores.append(get_similarity_score(answer.strip(), user_response))
      sum = 0
      count = 0
      gpt_answer_scores.sort()
      
      
      for i in range(6):
            sum += gpt_answer_scores[i]
            count += 1
      user_score = sum / count
      gpt_response = gpt_response + "Your score for this response is " + str(user_score) + ". "
      # evaluate correctness
      if (user_score >= sim_threshold):
            gpt_response += "Nice job!\n\n"
      else:
            gpt_response += "That's not quite right - try again.\n\n"
      # add conversation history
      messages=[
            {"role": "user", "content": "Evaluate the correctness of my response to the following prompt: " + essay_prompt},
            {"role": "assistant", "content": "Certainly! What was your response to the prompt?"},
            {"role": "user", "content": user_response},
            {"role": "assistant", "content": gpt_response} 
      ]
      # add additional feedback and resources
      response = openai.Completion.create(
            engine = "text-davinci-002",
            prompt = "What can I improve or fix about my answer on World War II? Where can I learn more?",
            max_tokens = 1024,
            n = 1,
            temperature = 0.5,
            stop = None
      )
      gpt_response += response.choices[0].text.strip()
      return user_score, gpt_response
            
                  

def get_similarity_score(gpt_generated_text, user_input):
    text1 = nlp(user_input)
    text2 = nlp(gpt_generated_text)
    return text1.similarity(text2)




prompt = "What were the causes of German unrest prior to World War Two? Use prose form and write at a 10th grade level."
user_input = input( "What were the causes of German unrest prior to World War Two?")
text_a = "In the years leading up to World War II, Germany experienced significant political and social unrest, with a variety of factors contributing to the country's instability. One major cause was the harsh terms imposed on Germany by the Treaty of Versailles following World War I. This agreement placed the blame for the war on Germany and required the country to pay reparations, cede territory, and limit its military capabilities. Many Germans saw these terms as unjust and resented the other countries involved in the treaty. "+ "Additionally, economic struggles contributed to the unrest. Following the Great Depression, Germany experienced high unemployment rates, inflation, and a general decline in the standard of living. These challenges created a sense of frustration and desperation among the German people, which was exploited by Nazi leaders."

text_b = "Furthermore, political divisions and polarization contributed to the unrest. Germany's government was unstable, with multiple parties vying for power and influence. This instability led to frequent changes in leadership and a lack of coherent policies. The Nazi Party, led by Adolf Hitler, capitalized on these divisions and used propaganda to rally supporters around their message of nationalism and racial purity."
text3 = "Finally, the rise of fascism and authoritarianism in other parts of Europe also influenced events in Germany. The Italian fascist leader Benito Mussolini and the Spanish dictator Francisco Franco provided models for Hitler and other German leaders to emulate, and Germany's growing alliance with fascist Italy further solidified their commitment to these ideals."
text4 = "In conclusion, the causes of German unrest prior to World War II were complex and multifaceted. Harsh treaty terms, economic struggles, political divisions, and the influence of fascist ideologies all played a role in the country's instability and eventual descent into war."

#user_response = text_a + text_b
#user_response = user_response + text3
# user_response = user_response + text4

user_response = user_input

print(gpt_response(prompt, user_response))

# #
# # IGNORE EVERYTHING BELOW HERE
# #


# # model parameters
# model = "text-davinci-002" # alternatively: "davinci-codex" "gpt-3.5-turbo" or "gpt-4"
# p_max_tokens = 2048
# p_n = 100 # number of responses gpt will generate (per question?)
# p_temperature = 0.8 # want the outputs to be more random
# p_stop = ["\\stop"] # list of string to stop generating at

# gpt_answers = []



# ## topic would be user input
# # this generates GPT's answers to the AI's questions
# def generate_response(user_question, conversation_history = None):
#     prompt = "Insert-user-input-here"

#     # if conversation_history is None:
#     #     conversation_history = []
    
#     # prompt_with_history = "\n".join([f"{turn['user']}: {turn['text']}" for turn in conversation_history] + [user_question])

#     response = openai.Completion.create(
#         engine=model,
#         prompt=prompt,#_with_history,
#         max_tokens=p_max_tokens,
#         n=p_n,
#         stop=p_stop,
#         temperature=p_temperature, # want the outputs to be more random
#     )

#     for answer in response.choices:
#         gpt_answers.append(answer.text.strip())
    
#     #generated_text = response.choices[0].text.strip()
#     #return generated_text

# # models have no memory of past conversations; may need something like:
# # openai.ChatCompletion.create(
# #   model="gpt-3.5-turbo",
# #   messages=[
# #         {"role": "system", "content": "You are a helpful assistant."},
# #         {"role": "user", "content": "Who won the world series in 2020?"},
# #         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
# #         {"role": "user", "content": "Where was it played?"}
# #     ]
# # )
# #
# # (messages is an array of dictionaries that stores past information)


# # determine similarity score 
# def similarity(gpt_generated_text, user_input, similarity_threshold):
#     text1 = nlp(user_input)
#     text2 = nlp(gpt_generated_text)
#     similarity_score = text1.similarity(text2)
    
#     ## could be increased later, just for attempt
#     # similarity_threshold = 0.6 # pass in similarity_threshold as a parameter instead of hard coding it
    
#     if similarity_score < similarity_threshold:
#             similarity_result = True
#     else:
#             similarity_result = False
#     return similarity_result
        
# # #topic would be user input & similarity
# # def generate_questions(similarity_result):
# #     # response = openai.Completion.create (
# #     #     engine = "text-davinci-002",
# #     #     prompt = generated_text
# #     #     max_tokens = 100,
# #     #     n = 1,
# #     #     stop = None,
# #     #     temperature = 0.5,
# #     # )
    
# #     generated_question = response.choices[0].text.strip()
# #     generated_answer = response.choices[0].answers[0].text.strip
    
# #     return generated_question, generated_answer

# ## generated_question will be printed out and
# ## generated_answer would be inputted in the similarity score function\
#  #   to be compared against user input