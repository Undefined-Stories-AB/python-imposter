

from typing import List
from os import linesep

def create_prompt(title: str, language: str='English', additional_text: str="", required_phrases: List[str] | None=None):
  return f"""I Want You To Act As A Very Proficient SEO writer That Speaks And Writes Fluently in {language}. Write A Long Form Article For This Title "{title}" Employing These directives:
1. Make sure you answer the question/subject in a NLP-friendly manner early in the article, and include the keyword in the first paragraph.
2. Write The Information In Your Own Words Rather Than Copying And Pasting From Other Sources.
3. Also Double-Check For Plagiarism Because I Need Pure Unique Content,
4. Write The Content In A Conversational Style As Written By A Human (Use An Informal Tone, Utilize Personal Pronouns, Keep It Simple, Engage The Reader, Use The Active Voice, Keep It Brief, Use Rhetorical Questions, and Incorporate Analogies And Metaphors).
5. When Creating Content, It's Essential To Consider Three Factors: Perplexity, Burstiness, And Complexity. (Perplexity Measures The Intricacy Of The Text, While Burstiness Evaluates The Variability Between Sentences.)
6. When Creating Content, It Is Important That Both Perplexity And Burstiness Are Present In High Amounts Without Losing Any Context Or Specificity.
7. Please use Markdown headings for each section
8. Keywords should also be bolded throughout the article
9. When Preparing The Article, Prepare To Write The Necessary Words In Bold.
10. Write Content So That It Can Outrank Other Websites.
11. Write An Article In A Formal "We" Form
12. The Article Should Contain Rich And Comprehensive, Very Detailed Paragraphs, With Lots Of Details, Even if it requires over a 1000 words.
13. Make the article long as to cover all the details.
Do Not Echo My Prompt. Do Not Self-Reference. Do Now Use Generic Filler Phrases. Do Use Useful Subheadings With Keyword-Rich Titles. Get To The Point Precisely And Accurately. Do Not Explain What And Why, Just Give Me Your Best Possible Article.
{f"Make sure to use these phrases at least once:{linesep + linesep.join(required_phrases)}" if required_phrases else ""}
{f"Please write in the {language} language." if language != "English" else ""}
{additional_text if additional_text else ""}
"""