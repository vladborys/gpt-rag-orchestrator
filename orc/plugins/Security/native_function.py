from shared.util import get_secret
# from semantic_kernel.skill_definition import sk_function
from semantic_kernel.functions import kernel_function
import logging
import os
import requests
import sys
from typing import Dict
if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

SECURITY_HUB_ENDPOINT = os.environ["SECURITY_HUB_ENDPOINT"]
class Security:
    @kernel_function(
        description="Check security of question and answer generated.",
        name="SecurityCheck",
    )
    def SecurityCheck(
        self,
        question: Annotated[str, "The user question"],
        answer: Annotated[str, "The answer generated by the model"],
        sources: Annotated[str, "The sources to search for the answer"],
    ) -> Annotated[bool, "Passed security checks"]:
        security_hub_endpoint=SECURITY_HUB_ENDPOINT
        try:
            security_hub_key = get_secret("securityHubKey")
            request = requests.post(
                security_hub_endpoint,
                json={"question": question, "answer": answer, "sources": sources},
                headers={"x-functions-key": security_hub_key}
            )
            if request.status_code != 200:
                logging.error(f"Error requesting security hub: {request.text}")
                return {"status": "error", "details": request.text}
            result = request.json()
            return {"status": "success", "details": result["details"],"successful":result["successful"]}
        except Exception as e:
            logging.error(f"Error requesting security hub: {str(e)}")
            return {"status": "error", "details": str(e)}
        
        
        