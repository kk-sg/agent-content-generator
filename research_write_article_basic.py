import os
from getpass import getpass
from typing import List, Dict, Any
from crewai import Agent, Task, Crew


def get_user_input(prompt: str) -> str:
    """
    Prompt the user for input.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: The user's input.
    """
    return input(prompt)


def get_openai_api_key() -> str:
    """
    Prompt the user to enter their OpenAI API key securely.

    Returns:
        str: The OpenAI API key entered by the user.
    """
    return getpass('Please enter your OpenAI API key: ')


def create_agent(role: str, goal: str, backstory: str) -> Agent:
    """
    Create an Agent with specified parameters.

    Args:
        role (str): The role of the agent.
        goal (str): The goal of the agent.
        backstory (str): The backstory of the agent.

    Returns:
        Agent: A configured Agent object.
    """
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        allow_delegation=False,
        verbose=True
    )


def create_task(description: str, expected_output: str, agent: Agent) -> Task:
    """
    Create a Task with specified parameters.

    Args:
        description (str): The description of the task.
        expected_output (str): The expected output of the task.
        agent (Agent): The agent responsible for the task.

    Returns:
        Task: A configured Task object.
    """
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )


def main() -> None:
    """
    Main function to set up and execute the content creation process.
    """
    openai_api_key = get_openai_api_key()
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

    topic = get_user_input("Please enter the topic for the blog post: ")

    planner = create_agent(
        role="Content Planner",
        goal=f"Plan engaging and factually accurate content on {topic}",
        backstory=f"You're working on planning a blog article about the topic: {topic}. "
                  f"You collect information that helps the audience learn something "
                  f"and make informed decisions. Your work is the basis for "
                  f"the Content Writer to write an article on this topic."
    )

    writer = create_agent(
        role="Content Writer",
        goal=f"Write insightful and factually accurate opinion piece about the topic: {topic}",
        backstory=f"You're working on writing a new opinion piece about the topic: {topic}. "
                  f"You base your writing on the work of the Content Planner, who provides an outline "
                  f"and relevant context about the topic. You follow the main objectives and "
                  f"direction of the outline, as provided by the Content Planner. "
                  f"You also provide objective and impartial insights and back them up with information "
                  f"provided by the Content Planner. You acknowledge in your opinion piece "
                  f"when your statements are opinions as opposed to objective statements."
    )

    editor = create_agent(
        role="Editor",
        goal="Edit a given blog post to align with the writing style of the organization.",
        backstory="You are an editor who receives a blog post from the Content Writer. "
                  "Your goal is to review the blog post to ensure that it follows journalistic best practices, "
                  "provides balanced viewpoints when providing opinions or assertions, "
                  "and also avoids major controversial topics or opinions when possible."
    )

    plan = create_task(
        description=(
            f"1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
            f"2. Identify the target audience, considering their interests and pain points.\n"
            f"3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
            f"4. Include SEO keywords and relevant data or sources."
        ),
        expected_output="A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.",
        agent=planner
    )

    write = create_task(
        description=(
            f"1. Use the content plan to craft a compelling blog post on {topic}.\n"
            f"2. Incorporate SEO keywords naturally.\n"
            f"3. Sections/Subtitles are properly named in an engaging manner.\n"
            f"4. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
            f"5. Proofread for grammatical errors and alignment with the brand's voice."
        ),
        expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
        agent=writer
    )

    edit = create_task(
        description="Proofread the given blog post for grammatical errors and alignment with the brand's voice.",
        expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
        agent=editor
    )

    crew = Crew(
        agents=[planner, writer, editor],
        tasks=[plan, write, edit],
        verbose=2
    )

    result = crew.kickoff()
    print(result)


if __name__ == "__main__":
    main()
