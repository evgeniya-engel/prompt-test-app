def get_transferrable_skills(current_role, desired_role):
    return {"role": "user",
             "content": f"""1. Analyze the current role description and the desired role.
             Current Role: {current_role};
             Desired Role: {desired_role}
             2. Generate a list of up to 10 possible technical skills that are applicable to the current role that can be transferred to the desired role - transferrable skills.
             3. If there are not enought technical skills in the Current Role description, you can assume the technical skills as most popular skills that people working in this role normally posess.
             4. Only output the list in a parseable Python format, like in example: ["python programming", "machine learning algorithms", "data visualization"]. Do not include "```python\\n" in the output.
             """
            }

def get_roadmap_prompt(current_role, desired_role, transferrable_skills, timeline):
    return {
            
            "role": "user",
            
             "content": f'''
             Analyze the Current Role description, the Desired Role and a list of Skills that user posesses that can be applicable to the Desired Role.
             Current Role: {current_role};
             Desired Role: {desired_role};
             Skills: {transferrable_skills}

            Build a 5 step career transition roadmap that will help the user reach this goal within {timeline}.
            Provide the result in json format following this structure:

            {{"goals": 
            [ {{"goal_number": int, "goal_content": str,
                "focus": str, 
                "actions": str, 
                "outcome": str,
                "time_commitment_hours": int}}, 
                {{...}}, 
                ... ] }}
                "]
            '''
        }
