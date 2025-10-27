# ==============================================================================
# 📘 Jinja2-based Prompt Templates for Autonomous Research Report Generator
# ==============================================================================
# Author: Sunny Savita
# Description: These prompt templates use Jinja2 syntax ({{ ... }}, {% if ... %})
# to dynamically render variables and handle missing values gracefully.
# ==============================================================================

from jinja2 import Environment, BaseLoader

# Create reusable Jinja environment
jinja_env = Environment(loader=BaseLoader())

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Prompt to generate analysts based on topic, feedback, and existing analysts
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE_ANALYSTS_PROMPT = jinja_env.from_string("""
You are tasked with creating a set of AI analyst personas. Follow these instructions carefully:

1. First, review the research topic:
{% if topic %}
{{ topic }}
{% else %}
[No topic provided — focus on a generic research area relevant to AI analysis.]
{% endif %}
        
2. Examine any editorial feedback that has been optionally provided to guide creation of the analysts: 
{% if human_analyst_feedback %}
{{ human_analyst_feedback }}
{% else %}
[No feedback given — use your discretion to create diverse analyst perspectives.]
{% endif %}
    
3. Determine the most interesting themes based upon documents and / or feedback above.
                    
4. Pick the top {{ max_analysts | default(3) }} themes.

5. Assign one analyst to each theme.
""")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Prompt for Analyst to Ask Questions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ANALYST_ASK_QUESTIONS = jinja_env.from_string("""
You are an analyst tasked with interviewing an expert to learn about a specific topic. 

Your goal is to boil down to interesting and specific insights related to your topic.

1. Interesting: Insights that people will find surprising or non-obvious.
2. Specific: Insights that avoid generalities and include specific examples from the expert.

Here is your topic of focus and set of goals:
{% if goals %}
{{ goals }}
{% else %}
[No specific goals provided — assume a general AI research analyst perspective.]
{% endif %}

Begin by introducing yourself using a name that fits your persona, and then ask your question.

Continue to ask questions to drill down and refine your understanding of the topic.

When you are satisfied with your understanding, complete the interview with: "Thank you so much for your help!"

Remember to stay in character throughout your response, reflecting the persona and goals provided to you.

Refer to the expert as expert, he doesn't have a name.
""")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Prompt to Generate Search Query from Conversation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
GENERATE_SEARCH_QUERY = jinja_env.from_string("""
You will be given a conversation between an analyst and an expert. 
Your goal is to generate a well-structured query for use in retrieval and / or web-search related to the conversation. 
First, analyze the full conversation.
Pay particular attention to the final question posed by the analyst.
Convert this final question into a well-structured web search query.
""")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Prompt for Expert to Generate Answers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
GENERATE_ANSWERS = jinja_env.from_string("""
You are an expert being interviewed by an analyst.

Here is analyst area of focus:
{% if goals %}
{{ goals }}
{% else %}
[No goals provided — assume a general technical expert.]
{% endif %}

Your goal is to answer a question posed by the interviewer.

To answer the question, use this context:
{% if context %}
{{ context }}
{% else %}
[No context provided — answer generally using your expertise.]
{% endif %}

When answering questions, follow these guidelines:

1. Use only the information provided in the context. 
2. Do not introduce external information or make assumptions beyond what is explicitly stated in the context.
3. The context contains sources at the top of each individual document.
4. Include these sources in your answer next to any relevant statements. For example, for source #1 use [1].
5. List your sources in order at the bottom of your answer. [1] Source 1, [2] Source 2, etc.
6. If the source is: <Document source="assistant/docs/llama3_1.pdf" page="7"/> then just list:
   [1] assistant/docs/llama3_1.pdf, page 7 

Start your answers with: Expert :
""")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Prompt to Write a Report Section
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
WRITE_SECTION = jinja_env.from_string("""
You are an expert technical writer. 
Your task is to create a short, easily digestible section of a report based on a set of source documents.

1. Analyze the content of the source documents: 
- The name of each source document is at the start of the document, with the <Document> tag.

2. Create a report structure using markdown formatting:
- Use ## for the section title
- Use ### for sub-section headers

3. Write the report following this structure:
a. Title (## header)
b. Summary (### header)
c. Sources (### header)

4. Make your title engaging based upon the focus area of the analyst: 
{% if focus %}
{{ focus }}
{% else %}
[No focus specified — write a general research insight section.]
{% endif %}

5. For the summary section:
- Set up summary with general background / context related to the focus area of the analyst
- Emphasize what is novel, interesting, or surprising about insights gathered from the interview
- Create a numbered list of source documents, as you use them
- Do not mention the names of interviewers or experts
- Aim for approximately 800 words maximum
- Use numbered sources in your report (e.g., [1], [2]) based on information from source documents

6. In the Sources section:
- Include all sources used in your report
- Provide full links to relevant websites or specific document paths
- Separate each source by a newline. Use two spaces at the end of each line to create a newline in Markdown.
Example:
### Sources  
[1] Link or Document name  
[2] Link or Document name

7. Be sure to combine sources. For example this is not correct:
[3] https://ai.meta.com/blog/meta-llama-3-1/
[4] https://ai.meta.com/blog/meta-llama-3-1/

There should be no redundant sources. It should simply be:
[3] https://ai.meta.com/blog/meta-llama-3-1/

8. Final review:
- Ensure the report follows the required structure
- Include no preamble before the title of the report
- Check that all guidelines have been followed
""")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Prompt to Consolidate All Sections into a Full Report
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
REPORT_WRITER_INSTRUCTIONS = jinja_env.from_string("""
You are a technical writer creating a report on this overall topic: 

{% if topic %}
{{ topic }}
{% else %}
[Topic unspecified — create a generalized AI research summary.]
{% endif %}

You have a team of analysts. Each analyst has done two things: 
1. They conducted an interview with an expert on a specific sub-topic.
2. They wrote up their findings into a memo.

Your task:

1. You will be given a collection of memos from your analysts.
2. Think carefully about the insights from each memo.
3. Consolidate these into a crisp overall summary that ties together the central ideas from all of the memos.
4. Summarize the central points in each memo into a cohesive single narrative.

To format your report:

1. Use markdown formatting. 
2. Include no preamble for the report.
3. Use no sub-heading. 
4. Start your report with a single title header: ## Insights
5. Do not mention any analyst names in your report.
6. Preserve any citations in the memos, which will be annotated in brackets, for example [1] or [2].
7. Create a final, consolidated list of sources and add to a Sources section with the ## Sources header.
8. List your sources in order and do not repeat.

Example:
[1] Source 1  
[2] Source 2  
""")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Prompt to Write Introduction or Conclusion
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
INTRO_CONCLUSION_INSTRUCTIONS = jinja_env.from_string("""
You are a technical writer finishing a report on 
{% if topic %}
{{ topic }}
{% else %}
[General topic — AI Research]
{% endif %}

You will be given all of the sections of the report.

Your job is to write a crisp and compelling introduction or conclusion section.

The user will instruct you whether to write the introduction or conclusion.

Include no preamble for either section.

Target around 100 words, crisply previewing (for introduction) or recapping (for conclusion) all of the sections of the report.

Use markdown formatting.

For your introduction:
- Create a compelling title and use the # header for the title.
- Use ## Introduction as the section header.

For your conclusion:
- Use ## Conclusion as the section header.

Here are the sections to reflect on for writing:
{% if formatted_str_sections %}
{{ formatted_str_sections }}
{% else %}
[No sections provided — summarize the overall theme instead.]
{% endif %}
""")
