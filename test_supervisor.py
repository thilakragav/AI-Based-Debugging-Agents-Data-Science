from agent.agents.supervisor_agent import (
    supervisor_agent
)


state = {

    "error_message":
        'column "customer_name" does not exist',

    "classification": {

        "technology":
            "postgresql",

        "category":
            "schema",

        "error_type":
            "UndefinedColumn"
    }
}


result = supervisor_agent(state)


print("=" * 60)
print("SUPERVISOR TEST")
print("=" * 60)

print(
    "\nSelected Agent:",
    result["selected_agent"]
)

print(
    "\nReason:",
    result["routing_reason"]
)