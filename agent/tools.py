import json
import os
from datetime import datetime, timedelta
from langchain_core.tools import tool

@tool
def book_consultation(
    caller_name: str,
    phone: str,
    practice_area: str,
    preferred_time: str,
    email: str = ""
) -> str:
    """
    Books a free 15-minute consultation with the appropriate attorney.
    Use this when the caller is ready to schedule and has provided
    their name, phone number, and preferred time.
    """
    confirmation_id = f"MLAW-{datetime.now().strftime('%Y%m%d%H%M%S')}" 
    
    attorney_map = {
        "family law": "Sarah Chen, J.D.",
        "personal injury": "Marcus Rodriguez, J.D.",
        "criminal defense": "David Kim, J.D.",
        "estate planning": "Patricia Williams, J.D."
    }
    attorney = attorney_map.get(practice_area.lower(), "Senior Attorney")

    result = {
        "status": "confirmed", 
        "confirmation_id": confirmation_id,
        "client_name": caller_name,
        "attorney": attorney,
        "practice_area": practice_area,
        "scheduled_time": preferred_time,
        "duration": "15 minutes",
        "message": f"Booked! {attorney} will call {phone} at {preferred_time}."
    }

    print(f"\n[TOOL] book_consultation → {caller_name} | {practice_area}")
    return json.dumps(result)

@tool
def capture_lead(
    name:str,
    phone:str,
    case_type:str,
    notes:str,
    email:str="",
    urgency:str="normal" 
) -> str:
    """
    Saves caller information to the CRM as a new lead.
    Use this for every caller even if they do not book immediately.
    Always capture the lead before ending the conversation.
    """
    lead_id=f"HS-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    result = {
        "status": "saved",
        "lead_id": lead_id,
        "name": name,
        "phone": phone,
        "case_type": case_type,
        "urgency": urgency,
        "notes": notes,
        "assigned_to": "Intake Team",
        "message": f"Lead {lead_id} saved. Intake team notified."
    }

    print(f"\n [TOOL] capture_lead->{name}|{case_type}|{urgency}")
    return json.dumps(result)

@tool
def escalate_urgent_case(
    caller_name:str,
    phone: str,
    situation: str 

)->str:
    """
    Immediately escalates urgent cases to the on-call attorney.
    Use when caller mentions arrest, detention, custody emergency,
    restraining order violation, or says they need help RIGHT NOW.
    This should be called before any other tool in urgent situations.
    """

    alert_id=f"URGENT-{datetime.now().strtime('%Y%m%d%H%M%S')}"

    result={
        "status":"escalated",
        "alert_id":alert_id,
        "on_call_attorney": "David Kim, J.D.",
        "expected_callback": "Within 15 minutes",
        "message": (
            f"URGENT alert sent. Attorney David Kim has been notified "
            f"and will call {phone} within 15 minutes. "
            f"If with police: say I am invoking my right to remain silent "
            f"and my right to an attorney."
        )
    }
    print(f"\n[TOOL]escalate_urgent_case->{caller_name}|{situation}")
    return json.dumps(result)

@tool
def check_availability(
    practice_area:str,
    preferred_day:str = "any"

) -> str:
    """
    Checks available consultation slots for the specified practice area.
    Use this when the caller asks when they can meet or before booking.
    """
    today =datetime.now()
    slots=[]
    for i in range(1,4):
        day= today +timedelta(days=i)
        if day.weekday() <5:
            slots.append(f"{day.strftime('%A %B %d')} at 10:00 AM CST")
            slots.append(f"{day.strftime('%A %B %d')} at 2:30 PM CST")
    attorney_map={
        "family law": "Sarah Chen",
        "personal injury": "Marcus Rodriguez",
        "criminal defense": "David Kim",
        "estate planning": "Patricia Williams"

    }
    attorney=attorney_map.get(practice_area.lower(),"our attorney")

    result={
        "attorney": attorney,
        "available_slots": slots[:4],
        "duration": "15 minutes free consultation",
        "message": f"{attorney} has openings available."
    }
@tool
def capture_lead(
    name: str,
    phone: str,
    case_type: str,
    notes: str,
    email: str = "",
    urgency: str = "normal"
) -> str:
    """
    Saves caller information to the CRM as a new lead.
    Use this for every caller even if they do not book immediately.
    Always capture the lead before ending the conversation.
    """
    lead_id = f"HS-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    result = {
        "status": "saved",
        "lead_id": lead_id,
        "name": name,
        "phone": phone,
        "case_type": case_type,
        "urgency": urgency,
        "notes": notes,
        "assigned_to": "Intake Team",
        "message": f"Lead {lead_id} saved. Intake team notified."
    }

    print(f"\n[TOOL] capture_lead → {name} | {case_type} | {urgency}")
    return json.dumps(result)

@tool
def escalate_urgent_case(
    caller_name: str,
    phone: str,
    situation: str
) -> str:
    """
    Immediately escalates urgent cases to the on-call attorney.
    Use when caller mentions arrest, detention, custody emergency,
    restraining order violation, or says they need help RIGHT NOW.
    This should be called before any other tool in urgent situations.
    """
    alert_id = f"URGENT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    result = {
        "status": "escalated",
        "alert_id": alert_id,
        "on_call_attorney": "David Kim, J.D.",
        "expected_callback": "Within 15 minutes",
        "message": (
            f"URGENT alert sent. Attorney David Kim has been notified "
            f"and will call {phone} within 15 minutes. "
            f"If with police: say I am invoking my right to remain silent "
            f"and my right to an attorney."
        )
    }

    print(f"\n[TOOL] escalate_urgent_case → {caller_name} | {situation}")
    return json.dumps(result)

@tool
def check_availability(
    practice_area: str,
    preferred_day: str = "any"
) -> str:
    """
    Checks available consultation slots for the specified practice area.
    Use this when the caller asks when they can meet or before booking.
    """
    today = datetime.now()
    slots = []
    for i in range(1, 4):
        day = today + timedelta(days=i)
        if day.weekday() < 5:
            slots.append(f"{day.strftime('%A %B %d')} at 10:00 AM CST")
            slots.append(f"{day.strftime('%A %B %d')} at 2:30 PM CST")

    attorney_map = {
        "family law": "Sarah Chen",
        "personal injury": "Marcus Rodriguez",
        "criminal defense": "David Kim",
        "estate planning": "Patricia Williams"
    }
    attorney = attorney_map.get(practice_area.lower(), "our attorney")

    result = {
        "attorney": attorney,
        "available_slots": slots[:4],
        "duration": "15 minutes free consultation",
        "message": f"{attorney} has openings available."
    }

    print(f"\n📆 [TOOL] check_availability → {practice_area}")
    return json.dumps(result)


@tool
def search_firm_knowledge(query: str) -> str:
    """
    Search Morrison & Associates knowledge base for information about
    services, pricing, attorneys, office hours, and firm policies.
    Use this for any question about the firm.
    
    Args:
        query: The question or topic to search for
    """
    import os
    import boto3
    from dotenv import load_dotenv
    load_dotenv()

    client = boto3.client(
        "bedrock-agent-runtime",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    try:
        response = client.retrieve(
            knowledgeBaseId=os.getenv("BEDROCK_KNOWLEDGE_BASE_ID"),
            retrievalQuery={"text": query},
            retrievalConfiguration={
                "vectorSearchConfiguration": {"numberOfResults": 3}
            }
        )

        results = response.get("retrievalResults", [])
        if not results:
            return "I don't have specific information about that. Let me connect you with one of our attorneys."

        context = "\n\n".join([r["content"]["text"] for r in results])
        return f"Based on our firm information:\n\n{context}"

    except Exception as e:
        return f"I'm unable to retrieve that information right now. Please call us directly at (312) 555-0100."

    query_lower = query.lower()
    found = []
    for key, value in knowledge.items():
        if key in query_lower:
            found.append(value)

    if found:
        result = {"found": True, "information": " ".join(found)}
    else:
        result = {
            "found": False,
            "information": "Best answered by an attorney in your free consultation."
        }

    print(f"\n🔍 [TOOL] search_firm_knowledge → {query}")
    return json.dumps(result)


ALL_TOOLS = [
    book_consultation,
    capture_lead,
    escalate_urgent_case,
    check_availability,
    search_firm_knowledge
]




    
