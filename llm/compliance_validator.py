"""Gemini-powered compliance validation module."""

from __future__ import annotations

from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from config import get_settings


class ComplianceReport(BaseModel):
    """Structured compliance result returned by the model."""

    violations: List[str] = Field(default_factory=list)
    risk_score: int = Field(ge=0, le=100)
    summary: str
    recommendations: List[str] = Field(default_factory=list)


class ComplianceValidator:
    """Runs compliance checks using Gemini with strict JSON schema output."""

    def __init__(self) -> None:
        settings = get_settings()
        # TODO: Set GOOGLE_API_KEY in your .env file.
        self.llm = ChatGoogleGenerativeAI(
            model=settings.gemini_chat_model,
            google_api_key=settings.google_api_key,
            temperature=0.1,
        )
        self.structured_llm = self.llm.with_structured_output(ComplianceReport)
        self.prompt = ChatPromptTemplate.from_template(
            """
You are a strict compliance auditor. Review the evidence against the policy rules.

Policy Rules:
{rules_context}

Evidence Text (Transcript + OCR):
{evidence}

Return a structured JSON report:
- violations: specific issues found
- risk_score: integer from 0 to 100
- summary: short overall assessment
- recommendations: actionable remediation items
If there are no violations, keep violations empty and risk_score low.
""".strip()
        )

    def validate(self, evidence: str, rules_context: str) -> ComplianceReport:
        """Run compliance validation and return structured report."""

        chain = self.prompt | self.structured_llm
        return chain.invoke({"evidence": evidence, "rules_context": rules_context})
