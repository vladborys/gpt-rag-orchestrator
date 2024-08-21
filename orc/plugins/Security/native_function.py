from shared.util import get_secret
# from semantic_kernel.skill_definition import sk_function
from semantic_kernel.functions import kernel_function
import logging
import os
import aiohttp
import sys
from typing import Dict
if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated
SECURITY_HUB_ENDPOINT = os.environ["SECURITY_HUB_ENDPOINT"]
APIM_ENABLED=os.environ.get("APIM_ENABLED", "false")
APIM_ENABLED=True if APIM_ENABLED.lower() == "true" else False
class Security:
    @kernel_function(
        description="Check security of question.",
        name="QuestionSecurityCheck",
    )
    async def QuestionSecurityCheck(
        self,
        question: Annotated[str, "The user question"],
        security_hub_key: Annotated[str, "The key to access the security hub"]
    ) -> Annotated[bool, "Passed security checks"]:
        if APIM_ENABLED:
            security_hub_endpoint=os.environ["APIM_SECURITY_HUB_ENDPOINT"]
        else:
            security_hub_endpoint=SECURITY_HUB_ENDPOINT
        try:
            async with aiohttp.ClientSession() as session:
            # Make a POST request using the session.post() method
             async with session.post(
                security_hub_endpoint+"/QuestionChecks",
                json={"question": question},
                headers={"x-functions-key": security_hub_key}
            ) as request:
                if request.status != 200:
                    logging.error(f"Error requesting security hub: {request.status} {request.reason}")
                    raise(Exception(f"Error requesting security hub: {request.status} {request.reason}"))
                else:
                    result = await request.json()
                    return result
        except Exception as e:
            logging.error(f"Error requesting security hub: {str(e)}")
            raise(Exception(f"Error requesting security hub: {str(e)}"))
        
        
    @kernel_function(
        description="Check security of generated answer.",
        name="AnswerSecurityCheck",
    )
    async def AnswerSecurityCheck(
        self,
        question: Annotated[str, "The user question"],
        answer: Annotated[str, "The answer generated by the model"],
        sources: Annotated[str, "The sources to search for the answer"],
        security_hub_key: Annotated[str, "The key to access the security hub"]
    ) -> Annotated[bool, "Passed security checks"]:
        if APIM_ENABLED:
            security_hub_endpoint=os.environ["APIM_SECURITY_HUB_ENDPOINT"]
        else:
            security_hub_endpoint=SECURITY_HUB_ENDPOINT
        try:
            async with aiohttp.ClientSession() as session:
            # Make a POST request using the session.post() method
             async with session.post(
                security_hub_endpoint+"/AnswerChecks",
                json={"question": question, "answer": answer, "sources": sources},
                headers={"x-functions-key": security_hub_key}
            ) as request:
                if request.status != 200:
                    logging.error(f"Error requesting security hub: {request.status} {request.reason} {await request.text()}")
                    raise(Exception(f"Error requesting security hub: {request.status} {request.reason} {await request.text()}"))
                else:
                    result = await request.json()
                    return result
        except Exception as e:
            logging.error(f"Error requesting security hub: {str(e)}")
            raise(Exception(f"Error requesting security hub: {str(e)}"))
        
        
        