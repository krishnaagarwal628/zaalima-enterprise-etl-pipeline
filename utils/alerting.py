import logging
import os
import requests

logger = logging.getLogger(__name__)


def send_slack_alert(context):
    """Callback function triggered when an Airflow task fails.

    Extracts execution context details and logs/sends real-time alert.
    """
    task_instance = context.get("task_instance")
    task_id = task_instance.task_id if task_instance else "Unknown Task"
    dag_id = context.get("dag").dag_id if context.get("dag") else "Unknown DAG"
    execution_date = context.get("execution_date", "N/A")
    exception = context.get("exception", "No exception details available")

    alert_message = (
        f"🚨 *Airflow Task Failure Alert* 🚨\n"
        f"*DAG:* {dag_id}\n"
        f"*Task:* {task_id}\n"
        f"*Execution Date:* {execution_date}\n"
        f"*Error Details:* {exception}"
    )

    # 1. Log failure alert locally
    logger.error(f"[Alert System] {alert_message}")

    # 2. Trigger Slack Webhook if configured in environment
    slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if slack_webhook_url:
        try:
            payload = {"text": alert_message}
            response = requests.post(slack_webhook_url, json=payload, timeout=5)
            if response.status_code == 200:
                logger.info("[Alert System] Slack alert dispatched successfully.")
            else:
                logger.warning(
                    f"[Alert System] Slack webhook returned status code {response.status_code}"
                )
        except Exception as e:
            logger.error(f"[Alert System] Failed to send Slack alert: {e}")
    else:
        logger.info(
            "[Alert System] SLACK_WEBHOOK_URL not set. Alert logged to console."
        )