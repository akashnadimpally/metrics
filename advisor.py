from azure.identity import DefaultAzureCredential
from azure.mgmt.advisor import AdvisorManagementClient

# Azure Subscription ID and Resource Group
subscription_id = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
resource_group_name = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
vm_name = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

credential = DefaultAzureCredential()
client = AdvisorManagementClient(credential, subscription_id=subscription_id)

resource_uri = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}"

response = client.recommendations.generate()

print(response)

recommendations = client.recommendations.list(
    scope=resource_uri
)

# Process the recommendations
for recommendation in recommendations:
    print(f"Recommendation ID: {recommendation.id}")
    print(f"Recommendation Name: {recommendation.name}")
    print(f"Recommended Action: {recommendation.properties.recommended_action}")
    print(f"Estimated Monthly Savings: {recommendation.properties.estimated_monthly_savings.amount} {recommendation.properties.estimated_monthly_savings.currency}")
    print("------")


# recommendations = client.recommendations.get_resource_recommendations(
#     resource_uri=resource_uri,
#     filter="cost"  # Filter for cost-related recommendations
# )

# for recommendation in recommendations:
#     print("Recommendation ID:", recommendation.id)
#     print("Category:", recommendation.category)
#     print("Impact:", recommendation.impact)
#     print("Description:", recommendation.short_description.localized_value)
#     print("----------------------------------------------------------------")
