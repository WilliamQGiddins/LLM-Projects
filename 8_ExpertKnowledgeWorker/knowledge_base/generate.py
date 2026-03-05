import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pathlib import Path
from rag_implementation.ingest import main as ingest
load_dotenv(override=True)

MODEL= "gpt-4o-mini"

# Initialize openai client
openai = OpenAI()
ollama_url = "http://localhost:11434/v1"
ollama = OpenAI(base_url=ollama_url, api_key='ollama')

class CompanyDetails(BaseModel):
    about: str = Field(description="Markdown about the company and its mission")
    careers: str = Field(description="Markdown about the different roles at the company")
    culture: str = Field(description="Markdown about the culture and values of the company")
    overview: str = Field(description="Markdown providing a general overview about the company")

class ContractDetails(BaseModel):
    name: str = Field(description="Name of the contract")
    description: str = Field(description="Description of the contract")
    partner: str = Field(description="Name of the partner the contract is with")

class EmployeeDetails(BaseModel):
    name: str = Field(description="Name of the employee")
    jobTitle: str = Field(description="Name of the employee job title")
    achievement: str = Field(description="A employee achievement")
    skill: str = Field(description="A unique job related skill")

class ProductDetails(BaseModel):
    name: str = Field(description="Name of the product")
    description: str = Field(description="Description of the product")

class KnowledgeBase(BaseModel):
    company: CompanyDetails = Field(description="A dictionary of markdown pertaining to the company")
    contracts: list[ContractDetails] = Field(description="A list of 10 sample contracts with other companies each returned in Mardown")
    employees: list[EmployeeDetails] = Field(description="A list of 10 sample employees and their roles, achievements and skills each returned in Mardown")
    products: list[ProductDetails] = Field(description="A list of 10 sample products and their features and benefits each returned in Mardown")

def generate_knowledge_base(description: str):
    system_prompt = f"""
    You are a expert assistant for generating the knowledge base for a company. Given a
    description of the company you produce a thorough sample knowledge base to be used by a RAG system 
    for the company that can be used to answer questions about the company, its employees products and services.
    The knowledge base should be broken down into four sections: company, contracts, employees and products.

    The company section should contain four sections returned in markdown:
    about: A brief description of the company and its products and services.
    careers: A list of the company's roles with a brief description.
    culture: A description of the company's culture and values.
    overview: A overview about the company.

    The contracts section should contain 10 sample contracts with other companies each property returned in Mardown format, each contract has three properties:
    name: Name of the contract
    description: Description of the contract
    partner: Name of the partner the contract is with
    
    The employees section should contain 10 sample employees and their roles, achievements and skills each property returned in Mardown format, each employee has four properties:
    name: Name of the employee
    jobTitle: Name of the employee job title
    achievement: A employee achievement
    skill: A unique job related skill 

    The products section should contain 10 sample products and their features and benefits each property returned in Mardown format, each product has two properties:
    name: Name of the product
    description: Description of the product
    """

    user_prompt = f"""
    Generate a sample knowledge base for the company described here: {description}.
    Format separate each section and subsection so that they can be broken up into their own markdown file.
    """

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt }]
    response = openai.chat.completions.parse(
      model=MODEL,
      messages=messages,
      response_format=KnowledgeBase
    )
    result = response.choices[0].message.content

    knowledgeBase_docs = KnowledgeBase.model_validate_json(result)

    return knowledgeBase_docs

def generate_test(docs):
    system_prompt = f"""
    You are a expert assistant responsible for creating a jsonL file for RAG testing
    Basd on submitted knowledge base

    Generate 10 test cases in the following format for a JSONL file:
    "question": "", "keywords": [], "category": "" 

    Here is an example:
    "question": "What is the contract number for DriveSmart Insurance's Carllm agreement?", "keywords": ["CR-2025-E-0078", "DriveSmart"], "reference_answer": "The contract number for DriveSmart Insurance's Carllm agreement is CR-2025-E-0078.", "category": "direct_fact"
    """

    user_prompt = f"""
    Generate 10 test in JSONL format for the company knowledge base here:
    {docs}

    Respond in JSONL only remove any text that is not a JSONL object
    """

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt }]
    response = openai.chat.completions.create(
      model=MODEL,
      messages=messages,
    )

    result = response.choices[0].message.content

    try:
        file_path = Path("../evaluation/tests.jsonl")
        with open(file_path, 'w') as f:
            f.write(result)
        print(f"Successfully wrote to {file_path}")
    except FileNotFoundError:
        print(f"Error: The directory for '{file_path}' does not exist.")
    
def create_knowledge_base_files(description: str):

    docs = generate_knowledge_base(description)
    generate_test(docs)

    company = docs.company
    contracts = docs.contracts
    employees = docs.employees
    products = docs.products

    # Create Company Directory
    try:
        folder_path = os.path.join( "company" )
        os.makedirs(folder_path, exist_ok=True)
    except FileExistsError:
        print('Directory {} already exists'.format(folder_path))

    # About
    try:
        file_path = "company/about.md"
        with open(file_path, 'w') as f:
            f.write(company.about)
        print(f"Successfully wrote to {file_path}")
    except FileNotFoundError:
        print(f"Error: The directory for '{file_path}' does not exist.")

    # Careers
    try:
        file_path = "company/careers.md"
        with open(file_path, 'w') as f:
            f.write(company.careers)
        print(f"Successfully wrote to {file_path}")
    except FileNotFoundError:
        print(f"Error: The directory for '{file_path}' does not exist.")

    # Culture
    try:
        file_path = "company/culture.md"
        with open(file_path, 'w') as f:
            f.write(company.culture)
        print(f"Successfully wrote to {file_path}")
    except FileNotFoundError:
        print(f"Error: The directory for '{file_path}' does not exist.")

    # Overview
    try:
        file_path = "company/overview.md"
        with open(file_path, 'w') as f:
            f.write(company.overview)
        print(f"Successfully wrote to {file_path}")
    except FileNotFoundError:
        print(f"Error: The directory for '{file_path}' does not exist.")

    # Create Contracts Directory
    try:
        folder_path = os.path.join("contracts" )
        os.makedirs(folder_path, exist_ok=True)
    except FileExistsError:
        print('Directory {} already exists'.format(folder_path))

    for contract in contracts:
        try:
            file_path = f"contracts/{contract.name}.md"
            with open(file_path, 'w') as f:
                f.write(f"Name: {contract.name} \nDescription: {contract.description} \nPartner: {contract.partner}")
                print(f"Successfully wrote to {file_path}")
        except FileNotFoundError:
            print(f"Error: The directory for '{file_path}' does not exist.")

        # Create Employees Directory
    try:
        folder_path = os.path.join("employees" )
        os.makedirs(folder_path, exist_ok=True)
    except FileExistsError:
        print('Directory {} already exists'.format(folder_path))

    for employee in employees:
        try:
            file_path = f"employees/{employee.name}.md"
            with open(file_path, 'w') as f:
                f.write(f"Name: {employee.name} \nJobTitle: {employee.jobTitle} \nSkill: {employee.skill} \nAchievement: {employee.achievement}")
                print(f"Successfully wrote to {file_path}")
        except FileNotFoundError:
            print(f"Error: The directory for '{file_path}' does not exist.")

    # Create Products Directory
    try:
        folder_path = os.path.join("products" )
        os.makedirs(folder_path, exist_ok=True)
    except FileExistsError:
        print('Directory {} already exists'.format(folder_path))

    for product in products:
        try:
            file_path = f"products/{product.name}.md"
            with open(file_path, 'w') as f:
                f.write(f"Name: {product.name} \nDescription: {product.description}")
                print(f"Successfully wrote to {file_path}")
        except FileNotFoundError:
            print(f"Error: The directory for '{file_path}' does not exist.")

    # Ingest Knowledge base and create vector store
    ingest()
            