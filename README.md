# Creating new Instruction Prompts
**Use [Stanford Alpaca's Instruction generating script](https://github.com/tatsu-lab/stanford_alpaca/blob/main/generate_instruction.py) instead, this is just a demo**

This repo is a demo of how to create new instruction prompts using ChatGPT API and using ray as workers to distribute the work across up to 1000 workers.

I wanted to see in 5 minutes, how many features I can write from scratch for an instruction generating script.

The variants is the generated instructions is pretty low. Probably using more seed instructions and a similiarity filter like in Alpaca would help.

## How to Run
Optional: [Set up your ray cluster](https://docs.ray.io/en/latest/cluster/getting-started.html)

```bash
## set up OPENAI_API_KEY
export OPENAI_API_KEY=YOUR_KEY

# Install dependencies
pip install -r requirements.txt

# Run the script
python main.py
```
```


# References
- https://github.com/yizhongw/self-instruct
- https://github.com/tatsu-lab/stanford_alpaca