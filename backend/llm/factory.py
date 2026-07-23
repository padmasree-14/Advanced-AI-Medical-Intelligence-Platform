import logging
from backend.config.settings import settings
from backend.llm.base import BaseLLMProvider
from backend.llm.gemini_provider import GeminiLLMProvider
from backend.llm.mock_provider import MockLLMProvider

logger = logging.getLogger(__name__)

def get_llm_provider() -> BaseLLMProvider:
    provider_type = settings.LLM_PROVIDER.lower()
    if provider_type == "gemini" and settings.GEMINI_API_KEY:
        logger.info("Initializing Gemini LLM Provider")
        return GeminiLLMProvider()
    else:
        logger.info("Initializing Mock LLM Provider (Offline mode)")
        return MockLLMProvider()
