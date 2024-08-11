# main.py
import streamlit as st
from crewai import Agent, Task, Crew
from utils.common_utils import (
    get_openai_api_key, display_markdown_content, create_download_button,
    get_user_input, show_success_message, show_warning_message
)
from utils.ai_models import OpenAILanguageModel


def create_agent(role: str, goal: str, backstory: str) -> Agent:
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        allow_delegation=False,
        verbose=True,
        llm=OpenAILanguageModel()
    )


def main() -> None:
    st.set_page_config(page_title="AI Content Generator",
                       page_icon="✍️", layout="wide")

    st.title("✍️ AI Content Generator")
    st.markdown("Generate blog posts on any topic using AI.")

    if get_openai_api_key():
        topic = get_user_input('Enter the topic for the blog post:')

        if st.button('Generate Content'):
            if not topic:
                show_warning_message(
                    "Please enter a topic before generating content.")
            else:
                with st.spinner('Generating content...'):
                    planner = create_agent(
                        role='Content Planner',
                        goal=f'Plan engaging and factually accurate content on {topic}',
                        backstory=f"You're working on planning a blog article about the topic: {topic}. "
                                  f"Your work is the basis for the Content Writer to write an article on this topic."
                    )

                    writer = create_agent(
                        role='Content Writer',
                        goal=f'Write insightful and factually accurate opinion piece about the topic: {topic}',
                        backstory=f"You're working on writing a new opinion piece about the topic: {topic}. "
                                  f"You base your writing on the work of the Content Planner."
                    )

                    editor = create_agent(
                        role='Editor',
                        goal='Edit a given blog post to align with the writing style of the organization.',
                        backstory="You are an editor who receives a blog post from the Content Writer."
                    )

                    plan = Task(
                        description=(
                            f'1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n'
                            f'2. Identify the target audience, considering their interests and pain points.\n'
                            f'3. Develop a detailed content outline including an introduction, key points, and a call to action.\n'
                            f'4. Include SEO keywords and relevant data or sources.'
                        ),
                        expected_output="A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.",
                        agent=planner
                    )

                    write = Task(
                        description=(
                            f'1. Use the content plan to craft a compelling blog post on {topic}.\n'
                            f'2. Incorporate SEO keywords naturally.\n'
                            f'3. Sections/Subtitles are properly named in an engaging manner.\n'
                            f'4. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n'
                            f'5. Proofread for grammatical errors and alignment with the brand\'s voice.'
                        ),
                        expected_output="A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs.",
                        agent=writer
                    )

                    edit = Task(
                        description="Proofread the given blog post for grammatical errors and alignment with the brand's voice.",
                        expected_output="A final, polished blog post in markdown format, ready for publication, with improved grammar and style.",
                        agent=editor
                    )

                    crew = Crew(
                        agents=[planner, writer, editor],
                        tasks=[plan, write, edit],
                        verbose=2
                    )

                    result = crew.kickoff()

                show_success_message("Content generated successfully!")

                final_output = str(result)

                display_markdown_content(final_output, "Generated Blog Post")

                create_download_button(
                    content=final_output,
                    filename=f"{topic.replace(' ', '_')}_blog_post.md"
                )
    else:
        st.warning('Please enter your OpenAI API key to proceed.')


if __name__ == '__main__':
    main()