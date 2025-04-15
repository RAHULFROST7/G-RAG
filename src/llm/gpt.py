from openai import OpenAI

class AnswerQuery:
    
    def __init__(self,gpt_model, gpt_api_key, chunks):
     

        # Initialize GPT Client
        self.gpt_model = gpt_model
        self.gpt_client = OpenAI(api_key=gpt_api_key)

        self.chunks = chunks

    def prepare_prompt(self, query, retrieved_chunks):

        # Format retrieved chunks
        formatted_chunks = []
        for chunk in retrieved_chunks[:5]:  # Limit to top 5 chunks
            chunk_id = chunk['id']
            title = chunk.get('title', 'Unknown Title')
            link = chunk.get('link', 'No Link Available')
            content = chunk.get('snippet', 'No content found')

            formatted_chunks.append(
                f"* Title: {title}\n"
                f"* Link: {link}\n"
                f"* Content: {content}\n"
                f"* Chunk ID: {chunk_id}\n"
            )

        combined_chunks = "\n\n".join(formatted_chunks)

        # System prompt
        system_prompt = {
            "role": "system",
            "content": (
                "You are an AI system responsible for generating answers based on user queries and provided document chunks. "
                "Your response must include:\n"
                "**Title**: Extract the most relevant title from the provided chunks.\n"
                "**Answer**: Concise and relevant to the query.\n"
                "**Reference**: Use links from the chunks as references.\n\n"
                "IMPORTANT: Do NOT fabricate chunk IDs. Use exact IDs given in the chunks."
            )
        }

        # User prompt
        user_prompt = {
            "role": "user",
            "content": (
                f"Based on the provided chunks, answer the following query: '{query}'.\n\n"
                f"Format your response as:\n"
                f"Title: <Most relevant chunk title>\n"
                f"Answer: <Generated response>\n"
                f"Reference: <Link to the source>\n\n"
                f"Here are the document chunks:\n\n{combined_chunks}"
            )
        }

        return [system_prompt, user_prompt]


    def query_gpt(self, prompt):
        """
        Query GPT with the prepared prompt.

        Args:
            prompt (list): The structured prompt.

        Returns:
            str: GPT's response.
        """
        response = self.gpt_client.chat.completions.create(
            model=self.gpt_model,
            messages=prompt,
            max_tokens=1024,
            temperature=0.7
        )

        return response.choices[0].message.content

    def answerBasedOnLLM(self, query):

        prompt = self.prepare_prompt(query, self.chunks)
        return self.query_gpt(prompt)
