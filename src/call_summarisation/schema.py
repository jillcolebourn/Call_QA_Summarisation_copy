from typing import List, Literal, Optional
from pydantic import BaseModel, Field


PrimaryCategory = Literal[
    "payments","cards_atm","credit_limits","economic_crime_prevention",
    "mortgage_servicing","mortgage_applications","complaints","other"
]

IntentType = Literal[
  # Payments
  "payment_status_check","payment_failed","payment_refund_request","payment_dispute","misdirected_payment_recovery",
  # Cards/ATM
  "card_activation","card_replacement","card_declined","atm_cash_withdrawal_issue",
  # Credit limits
  "overdraft_limit_increase_request","personal_loan_enquiry",
  # Fraud/security
  "account_security_review","report_suspected_scam", "account_access_concern","card_security_status","account_restriction_inquiry","verify_bank_communication",
  # Mortgage
  "mortgage_payment_issue","mortgage_statement_request","mortgage_application_status","mortgage_transfer_of_equity","mortgage_product_transfer","mortgage_arrears_capitalisation_request",
  # Complaints
  "new_complaint","escalate_complaint",
  # Other
  "general_information","other", "product_comparison"
]

Teams = Literal[
    "mortgage_operations_team","payments_support_team","transaction_support_team","card_services_team",
    "borrowing_and_lending_support_team","economic_crime_operations_team","customer_complaints_team"
]

Urgency = Literal["low","medium","high"]
Sentiment = Literal["expressed_dissatisfaction","neutral","satisfied"]

ProfileFlag = Literal[
    "account_security_monitoring","potential_scam_vulnerability","phishing_concern_reported","unusual_activity_concern_reported",
    "account_restricted_recently","payment_dispute_activity","multiple_phishing_concerns",
    "high_contact_frequency","multiple_dispute_activity","mortgage_payment_support_required",
    "mortgage_application_processing_delay","card_replacement_recent","atm_retained_card_event",
    "credit_limit_change_activity","customer_support_needs_identified","financial_support_indicator",
    "potential_complaint_escalation","customer_dissatisfaction_indicator"
]
class CallDataExtraction(BaseModel):
    """Schema for call summary and categorization."""
    # most fields are not optional. only primary category is mandatory 
    primary_category: PrimaryCategory = Field(..., description="The category in which the call falls. One of the allowed categories.")
    call_outcome: IntentType = Field(..., description="The main outcome of at the end of the call.")
    initial_contact_reason: IntentType = Field(..., description="The initial reason for contact at the start of the call.")
    customer_journey: List[IntentType] = Field(default_factory=list, description="A list of the intents raised throughout the call in the order they were raised. intent reasons can be repeated.")
  
    customer_requested: List[str] = Field(default_factory=list, description="1–5 bullets of the specific requests made by the customer.")
    actions_taken: List[str] = Field(default_factory=list, description="Actions explicitly taken during the call and stated in the transcript.")
    follow_up_needed: bool = Field(False, description="True only if a future step is needed, otherwise false.")
    next_team: Teams = Field(..., description="If follow_up_needed=false, keep empty. Otherwise,The next team to be assigned to the call.")
    next_steps: List[str] = Field(default_factory=list, description="If follow_up_needed=false, keep empty. Otherwise, list the next steps. Use team names from identified in next_teams")

    profile_flags: List[ProfileFlag] = Field(default_factory=list, description="flag attached to the customer profile if necessary or relevant. If no flags are relevant, leave empty")
    urgency: Urgency = Field("low", description="low/medium/high based on impact and time sensitivity.")
    sentiment: Sentiment = Field("neutral", description="Customer sentiment.")


class CallSummary(CallDataExtraction):
    summary: str = Field("", description = "2-5 sentences summary of the main points of the call.")