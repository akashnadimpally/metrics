from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient
from datetime import datetime, timedelta
import pandas as pd

# Azure Subscription ID and Resource Group
subscription_id = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
resource_group = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
vm_name = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Set up Azure credentials
credential = DefaultAzureCredential()

# Set up Azure Monitor Metrics client
monitor_client = MonitorManagementClient(credential, subscription_id)

# Define the time range (last 30 days)
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=2)

# Query metrics data
metrics_data = monitor_client.metrics.list(
    resource_uri=f'/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/{vm_name}',
    timespan=f'{start_time.isoformat()}/{end_time.isoformat()}',
    interval='PT1M',  # 1 minute(s) interval
    metricnames='Percentage CPU',
    aggregation='Maximum'
)

# Extract and process metrics data
data = []
for metric in metrics_data.value:
    for timeseries in metric.timeseries:
        for data_point in timeseries.data:
            timestamp = data_point.time_stamp
            if metric.name.localized_value == 'Percentage CPU' and data_point.average is not None:
                value = data_point.average * 100  # Convert to percentage
            elif data_point.average is not None:
                value = data_point.average
            else:
                value = None  # Handle the case where average is None
            data.append({'Timestamp': timestamp, metric.name.localized_value: value})

# Create a Pandas DataFrame
df = pd.DataFrame(data)

# Convert Timestamp to datetime format and make it timezone-unaware
df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.tz_localize(None)

# Save the data to an Excel sheet
excel_file_path = 'cpu_metrics.xlsx'
df.to_excel(excel_file_path, index=False)

print(f'Data saved to {excel_file_path}')

