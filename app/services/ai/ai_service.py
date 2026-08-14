import os
import json
from datetime import datetime, timezone
from app.extensions import db
from app.models.ai_history import AIHistory
from app.core.cache import Cache
from app.services.ai.gemini_service import GeminiService
from app.services.ai.mock_ai_service import MockAIService
from app.services.ai.prompt_builder import PromptBuilder
import hashlib

class AIService:
    @staticmethod
    def _generate_cache_key(prompt_type: str, prompt: str) -> str:
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
        return f"ai_response:{prompt_type}:{prompt_hash}"

    @staticmethod
    def process_ai_request(prompt_type: str, template_name: str, template_kwargs: dict, current_user_id: str) -> dict:
        # Build prompt
        prompt = PromptBuilder.build_prompt(template_name, **template_kwargs)
        
        # Check cache
        cache_key = AIService._generate_cache_key(prompt_type, prompt)
        cached_result = Cache.get(cache_key)
        if cached_result:
            return cached_result

        # Generate response
        use_mock = os.getenv("USE_MOCK_AI", "True").lower() == "true"
        
        try:
            if use_mock:
                method = getattr(MockAIService, f"generate_{prompt_type}")
                result = method(prompt)
            else:
                result = GeminiService.generate_json(prompt)
        except Exception as e:
            return {"error": str(e)}

        # Save to AIHistory
        history = AIHistory(
            prompt_type=prompt_type,
            input_data=json.dumps(template_kwargs),
            output_data=json.dumps(result),
            generated_by=current_user_id
        )
        db.session.add(history)
        db.session.commit()

        # Cache for 24 hours (86400 seconds)
        Cache.set(cache_key, result, timeout=86400)
        
        return result
