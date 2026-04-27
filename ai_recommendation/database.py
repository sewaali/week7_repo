from dotenv import load_dotenv

import os

from langchain_openai import ChatOpenAI

from langchain_classic.chains import LLMChain, SequentialChain

from langchain_core.prompts import PromptTemplate

load_dotenv()

my_var = os.getenv('Aapi_Key')

 

llm = ChatOpenAI(model="gpt-4o-mini", api_key=my_var)

 

plan_prompt = PromptTemplate(

   input_variables=["task"],

   template="Create a detailed step-by-step plan for this task{task}"

)

plan_chain = LLMChain(llm=llm, prompt=plan_prompt, output_key="plan")

organize_prompt = PromptTemplate(

   input_variables=["plan"],

   template="Organize this plan into clear priorities and timeline:\n{plan}"

)

organize_chain = LLMChain(llm=llm, prompt=organize_prompt, output_key="organized_plan")

final_prompt = PromptTemplate(

   input_variables=["organized_plan"],

   template="Improve this plan and make it more practical and easy to follow:\n{organized_plan}"

)

final_chain = LLMChain(llm=llm, prompt=final_prompt, output_key="final_output")

chain = SequentialChain(

   chains=[plan_chain, organize_chain, final_chain],

   input_variables=["task"],

   output_variables=["plan", "organized_plan", "final_output"],

   verbose=True

)

user_task = input("Enter your task:\n")

result = chain.invoke({"task": user_task})

print("\n--- PLAN ---")

print(result["plan"])

print("\n--- ORGANIZED ---")

print(result["organized_plan"])

print("\n--- FINAL ---")

print(result["final_output"])