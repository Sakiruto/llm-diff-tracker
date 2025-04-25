
# 🚀 Project Setup

Follow these steps to set up and run the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/Sakiruto/llm-diff-tracker.git
```

### 2. Navigate to the Project Directory

```bash
cd llm-diff-tracker
```

### 3. Install Dependencies

Make sure you have all the required dependencies. It's recommended to create a virtual environment first.

```bash
# Optional: Create and activate a virtual environment
python3 -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Set Up the Environment Variables
You can find the `.env.example` in the root directory for the API keys structure.

### 5. Run the Main Module

```bash
python -m prd_to_issues.main
```

> Make sure the `.env` file is properly configured before running the module.

### 6. Improvements Made

- User intent is clearly structured using structured outputs and keyword-based detection with Pydantic.
- Maintaining user feedback consistency by structuring leveled prompts.
- Instead of converting to a .md file through LLM, the JSON is obtained and structured into a .md file as needed.
- ID-based segregation of tasks, user stories, and epics.
- Token-efficient prompting with minimal hallucination.
- Several additional improvements (you'll discover them as you review the code) in `prd_sample` and `main` when comparing the changes.

### 7. Problems Currently Faced

Some major issues are:
- Sometimes, it returns the entire original structure with minor updates (full response).
- Sometimes, it returns only the updated part (partial response), e.g., just a task or a user story.

If we try to use a code diff algorithm like Meyers' algorithm (along with Bentley-McIlroy and Patience), the major problem arises when merging the partial responses.

Using code diff algorithms is not very fruitful in the case of partial responses, and searching for the updated response after user feedback to track updates based on the initial/first response generated is somewhat complicated. I found useful libraries like `deepDiff` that can help search JSON responses, but the extent of search is still questionable.

I would encourage the person working on this problem statement to thoroughly go through:
- OpenAI's core concepts documentation (important topics: structured response, text generation and prompting, function calling).
- Code diff algorithms. I have some good resources to get started with:
  - [Basic understanding of algorithms](https://ably.com/blog/practical-guide-to-diff-algorithms#bentley-mc-ilroy)
  - [Meyers Algorithm Research Paper](http://www.xmailserver.org/diff2.pdf)

For a detailed understanding of the problem statement, you can visit the StackOverflow question I posted (still waiting for an answer, unfortunately!):
[Link](https://stackoverflow.com/questions/79587971/how-to-detect-and-merge-updates-in-nested-pydantic-models-partial-vs-full-upda)
