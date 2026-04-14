import boto3
from datetime import datetime

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

def put_metric(name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='LakehousePipeline',
        MetricData=[{
            'MetricName': name,
            'Value': value,
            'Unit': unit,
            'Timestamp': datetime.utcnow()
        }]
    )

def monitor_pipeline(rows_before, rows_after):
    put_metric('RowsProcessed', rows_before)
    put_metric('RowsAfterCleaning', rows_after)
    put_metric('RowsDropped', rows_before - rows_after)
    put_metric('DataQualityScore', 
               round((rows_after / rows_before) * 100, 2), 
               'Percent')
    print(f"Metrics sent to CloudWatch:")
    print(f"  Rows processed: {rows_before}")
    print(f"  Rows after cleaning: {rows_after}")
    print(f"  Rows dropped: {rows_before - rows_after}")
    print(f"  Data quality score: {round((rows_after/rows_before)*100,2)}%")

def create_alarm():
    cloudwatch.put_metric_alarm(
        AlarmName='LowDataQuality',
        MetricName='DataQualityScore',
        Namespace='LakehousePipeline',
        Statistic='Average',
        Period=300,
        EvaluationPeriods=1,
        Threshold=80.0,
        ComparisonOperator='LessThanThreshold',
        AlarmDescription='Alert when data quality drops below 80%'
    )
    print("CloudWatch alarm created!")

if __name__ == "__main__":
    monitor_pipeline(1369765, 1220127)
    create_alarm()