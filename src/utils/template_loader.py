"""
Template loading and rendering utility for prompt templates.

Usage:
    from src.utils.template_loader import TemplateLoader

    # Load router prompt
    prompt = TemplateLoader.load_router_prompt(
        context="Current workflow state...",
        ltv_max=0.95,
        lti_max=4.5,
        ndi_min_percent=40
    )

    # Load agent task template
    task = TemplateLoader.load_task_template(
        agent='data_gatherer',
        task_type='basic_data_retrieval',
        client_id=31567,
        customer_data_status='✅ Already Retrieved'
    )
"""
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class TemplateLoader:
    """Load and render prompt templates with variable substitution"""

    @staticmethod
    def load_template(template_path: str, **kwargs) -> str:
        """
        Load a template file and substitute variables.

        Args:
            template_path: Path to template file (relative to project root)
            **kwargs: Variables to substitute in template

        Returns:
            Rendered template string

        Example:
            template = TemplateLoader.load_template(
                'prompts/task_templates/data_gatherer/basic_data_retrieval.txt',
                client_id=31567,
                customer_data_status='✅ Retrieved'
            )
        """
        path = Path(template_path)

        if not path.exists():
            logger.error(f"Template not found: {template_path}")
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(path, 'r', encoding='utf-8') as f:
            template = f.read()

        try:
            # Only use str.format() if there are actually variables to substitute.
            # This prevents errors with single curly braces in JSON-like blocks in non-parameterized templates.
            if kwargs:
                rendered = template.format(**kwargs)
            else:
                rendered = template
            logger.debug(f"Template loaded: {template_path}")
            return rendered
        except KeyError as e:
            logger.error(f"Missing template variable in {template_path}: {e}")
            raise ValueError(f"Template {template_path} requires variable: {e}")

    @staticmethod
    def load_router_prompt(context: str, **config_values) -> str:
        """
        Load router decision-making prompt with context and config values.

        Args:
            context: Pre-built context string from build_rich_context()
            **config_values: Config values like ltv_max, lti_max, ndi_min_percent, strikes_max

        Returns:
            Rendered router prompt

        Example:
            from src.config.config_loader import POLICIES

            prompt = TemplateLoader.load_router_prompt(
                context=build_rich_context(state),
                ltv_max=POLICIES['pre_qualification']['ltv_max'],
                lti_max=POLICIES['affordability']['lti_max'],
                ndi_min_percent=POLICIES['affordability']['ndi_min_percent'] * 100,
                strikes_max=POLICIES['pre_qualification']['strikes_max']
            )
        """
        return TemplateLoader.load_template(
            'prompts/router_prompts/autonomous_router.txt',
            context=context,
            **config_values
        )

    @staticmethod
    def load_task_template(agent: str, task_type: str, **variables) -> str:
        """
        Load agent task template.

        Args:
            agent: Agent name (data_gatherer, decision_maker, action_orchestrator)
            task_type: Task type (basic_data_retrieval, income_docs_extraction, etc.)
            **variables: Template variables

        Returns:
            Rendered task template

        Example:
            task = TemplateLoader.load_task_template(
                agent='data_gatherer',
                task_type='basic_data_retrieval',
                client_id=31567,
                customer_data_status='✅ Already Retrieved',
                account_data_status='❌ NOT YET RETRIEVED',
                income_docs_status='⏳ Not Checked'
            )
        """
        template_path = f'prompts/task_templates/{agent}/{task_type}.txt'
        return TemplateLoader.load_template(template_path, **variables)


# Helper functions for status string formatting
def format_retrieval_status(retrieved: bool) -> str:
    """Format retrieval status as checkmark string"""
    return '✅ Already Retrieved' if retrieved else '❌ NOT YET RETRIEVED'


def format_assessment_status(completed: bool) -> str:
    """Format assessment status as checkmark string"""
    return '✅ COMPLETED - DO NOT REPEAT' if completed else '⏳ Needs to be done'


def format_docs_status(docs_available: bool | None) -> str:
    """Format document availability status"""
    if docs_available is None:
        return '⏳ Not Checked'
    elif docs_available:
        return '✅ Successfully Retrieved'
    else:
        return '❌ Not Retrieved Yet'


def format_verification_status(verified: bool | None) -> str:
    """Format verification status"""
    if verified is None:
        return '⏳ Not Performed'
    elif verified:
        return '✅ VERIFIED'
    else:
        return '❌ NOT VERIFIED'
