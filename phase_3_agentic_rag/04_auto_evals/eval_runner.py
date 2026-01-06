import json
import colorama
from colorama import Fore, Style
from openai import OpenAI
from agent import get_agent_response 

colorama.init(autoreset=True)
client = OpenAI()

def evaluate_answer(question, actual_answer, expected_fact):
    """
    Uses an LLM to decide if the Actual Answer matches the Expected Fact.
    Returns: Boolean (True/False)
    """
    judge_prompt = f"""
    You are a strict Grader. 
    
    QUESTION: {question}
    EXPECTED FACT: {expected_fact}
    ACTUAL ANSWER: {actual_answer}
    
    Did the ACTUAL ANSWER contain the EXPECTED FACT? 
    Answer only 'YES' or 'NO'.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": judge_prompt}]
    )
    
    grade = response.choices[0].message.content.strip().upper()
    return "YES" in grade

def run_tests():
    with open("test_cases.json", "r") as f:
        tests = json.load(f)
        
    print(f"--- Starting Eval Run ({len(tests)} tests) ---\n")
    passed = 0
    
    for test in tests:
        print(f"Testing: '{test['question']}'")
        
        # 1. Run Agent
        actual_response = get_agent_response(test['question'])
        
        # 2. Check Logic (LLM Judge)
        fact_check = evaluate_answer(test['question'], actual_response, test['expected_fact'])
        
        # 3. Check Citations (Simple String Match)
        citation_check = test['expected_citation'] in actual_response
        
        # 4. Final Verdict
        if fact_check and citation_check:
            print(Fore.GREEN + "PASS")
            passed += 1
        else:
            print(Fore.RED + "FAIL")
            print(f"   Expected: {test['expected_fact']}")
            print(f"   Got: {actual_response}")
            if not citation_check:
                print(f"   Missing Citation: {test['expected_citation']}")
                
        print("-" * 30)
        
    print(f"\nTotal Score: {passed}/{len(tests)}")

if __name__ == "__main__":
    run_tests()