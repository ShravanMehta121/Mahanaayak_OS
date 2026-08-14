import os

class PromptBuilder:
    @staticmethod
    def build_prompt(template_name, **kwargs):
        template_path = os.path.join(os.path.dirname(__file__), 'prompt_templates', f"{template_name}.txt")
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template {template_name}.txt not found")
            
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
            
        # Basic replacement of {{ key }}
        for key, value in kwargs.items():
            template = template.replace(f"{{{{ {key} }}}}", str(value))
            template = template.replace(f"{{{{{key}}}}}", str(value))
            
        return template
