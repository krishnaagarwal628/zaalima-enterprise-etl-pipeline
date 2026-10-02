from unittest.mock import MagicMock, patch
from utils.alerting import send_slack_alert


def test_send_slack_alert_console_logging(caplog):
    """Verify that send_slack_alert formats the alert and logs it when webhook is missing."""
    mock_task_instance = MagicMock()
    mock_task_instance.task_id = "test_failing_task"

    mock_dag = MagicMock()
    mock_dag.dag_id = "test_dag"

    mock_context = {
        "task_instance": mock_task_instance,
        "dag": mock_dag,
        "execution_date": "2026-10-02",
        "exception": Exception("API Connection Timeout Error"),
    }

    with caplog.at_level("ERROR"):
        send_slack_alert(mock_context)

    assert "Airflow Task Failure Alert" in caplog.text
    assert "test_failing_task" in caplog.text
    assert "API Connection Timeout Error" in caplog.text


@patch("requests.post")
def test_send_slack_alert_webhook_dispatch(mock_post, monkeypatch):
    """Verify that send_slack_alert dispatches a POST request when webhook URL is set."""
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/mock/test")
    mock_post.return_value.status_code = 200

    mock_task_instance = MagicMock()
    mock_task_instance.task_id = "test_failing_task"

    mock_context = {
        "task_instance": mock_task_instance,
        "dag": MagicMock(dag_id="test_dag"),
        "execution_date": "2026-10-02",
        "exception": Exception("Simulated Failure"),
    }

    send_slack_alert(mock_context)

    assert mock_post.called
    assert mock_post.call_args[0][0] == "https://hooks.slack.com/services/mock/test"