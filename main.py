from typing import List, Optional
import openai
import os
import random
import re
import ray
openai.api_key = os.getenv("OPENAI_API_KEY")


# some of seed tasks come from Self-Instruct
# https://github.com/yizhongw/self-instruct/blob/main/data/seed_tasks.jsonl
SEED_TASKS = [  
    "Instruction: Give me a cooking recipe for the following food. Watermelon",
    "Instruction: Make a list of the most popular podcasts.",
    "Instruction: Write a short story about a person who discovers a hidden talent.",
    "Instruction: Write a product review for your favorite tech gadget.",
    "Instruction: Generate a haiku using the following word: cat",
    "Instruction: Is there anything I can eat for a breakfast that doesn't include eggs, yet includes protein, and has roughly 700-1000 calories?",
    "Instruction: Write a cold email to a potential client for a tech startup focused on LLMs.",
    "Instruction: How to change a tire on a toyota corolla?",
    "Instruction: Given a sorted array, write a function to find the median element. [1, 2, 3, 4, 5]",
    "Instruction: Write a function that takes in a string and returns the number of vowels in the string.",
    "Instruction: Write a python program to output all permutations of the following word list. ['apple', 'banana', 'orange']",
    "Instruction: Is it a good idea to use online shopping?",
    "Instruction: A farmer has 5 chickens and wants to make at least $100 by selling them. he will sell each chicken for $10. how many chickens should he sell?",
    "Instruction: Write an essay about how you can make your college life better."
]
@ray.remote
def create_instruction_worker(tasks: List[str], id: int):
    # print worker id
    print(f"Worker {id} started")
    for j in range(20):
        # print worker id and iteration
        print(f"Worker {id} iteration {j}")
        # randomly select 5 tasks from the list of tasks
        tasks_to_complete = random.sample(tasks, 5)

        # create a prompt for the GPT-3 API
        prompt = "This is a list of example instructions:\n" + "\n".join(tasks_to_complete) + "\n" + "Write 20 more instructions\n"
        # print(prompt)
        # call chat-gpt API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes instructions."},
                    {"role": "user", "content": prompt}
                ]
        )

        # split the response into individual instructions
        new_tasks = response["choices"][0]["message"]["content"].split("\n")

        # remove regex [0-9]+\. from the beginning of each instruction
        new_tasks = [re.sub(r"^[0-9]{1,2,3}.", "", task) for task in new_tasks]

        # remove single and double digit numbers from the beginning of each instruction
        new_tasks = [re.sub(r"^Instruction [0-9]{1,2}.", "", task) for task in new_tasks]

        new_tasks = [re.sub(r"^Instruction.", "", task) for task in new_tasks]

        new_tasks = [re.sub(r"^[0-9]{1,2}. ", "", task) for task in new_tasks]

        # remove leading whitespace
        new_tasks = [task.lstrip() for task in new_tasks]

        # remove empty strings
        new_tasks = [task for task in new_tasks if task]
        
        # remove "Here are 20 more instructions:"
        new_tasks = [task for task in new_tasks if "20 more instructions:" not in task]

        with open(f"./data/worker-{id}.txt", "a") as f:
            for task in new_tasks:
                # if it doesn't contain "Instruction: " at the beginning, add it
                if not task.startswith("Instruction: "):
                    f.write(task + "\n")


        # add 2 new random tasks from new tasks to the list of tasks
        tasks.extend(random.sample(new_tasks, 2))



def create_instructions(num_workers: int = 8, seed_file_path: Optional[str] = None):
    if not seed_file_path:
        tasks = SEED_TASKS
    else: 
        # read in the list of tasks from a file
        with open("tasks.txt", "r") as f:
            tasks = f.read().splitlines()
            # add "Instruction: " to beginning of each task
            tasks = ["Instruction: " + task for task in tasks]

    # if data folder doesn't exist, create it
    if not os.path.exists("./data"):
        os.makedirs("./data")

    future_ref_list = []
    for i in range(num_workers):
        # deepcopy tasks
        tasks_copy = tasks.copy()

        # create create_instruction_worker
        future_ref = create_instruction_worker.remote (tasks_copy, i)
        future_ref_list.append(future_ref)

    ray.get(future_ref_list)

if __name__ == "__main__":
    import fire
    fire.Fire(create_instructions)