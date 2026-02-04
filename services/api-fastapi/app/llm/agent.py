from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_cohere import ChatCohere

from app.llm.tools import get_candidate_profile, search_similar_profiles, calculate_score
from app.llm.prompt_loader import PromptLoader
from app.llm.compression import ContextCompressor
from app.core.config import settings
import json, re


class Agent:
    def __init__(self):
        self.llm = ChatCohere(
            cohere_api_key=settings.COHERE_API_KEY,
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE
        )

        self.tools = [
            get_candidate_profile,
            search_similar_profiles, 
            calculate_score
        ]

        prompt = ChatPromptTemplate.from_messages([
            ("system", PromptLoader.get_prompt("candidate_summary", "v1")),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        self.agent = create_tool_calling_agent(
            llm=self.llm, 
            tools=self.tools, 
            prompt=prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5
        )

    async def generate_insight(self, query: str):
        try:
            compressed_input = ContextCompressor.compress(query)
            response = await self.agent_executor.ainvoke({
                "input": compressed_input
            })
            
            raw_output = response["output"]
            
            match = re.search(r'\{.*\}', raw_output, re.DOTALL)

            if match:
                json_str = match.group(0)
                try:
                    # 2. Convertir el string a un diccionario real de Python
                    data = json.loads(json_str)
                    return data
                except json.JSONDecodeError:
                    print("Error al parsear JSON del LLM")

            return {
                "summary": raw_output,
                "score": 0,
                "strengths": [],
                "weaknesses": [],
                "suggested_role": "N/A"
                }
        except Exception as e:
            return f"Error: {str(e)}."
