from unittest.mock import ANY, patch

from tests.fixtures import data

from pdchaoskit import controls


@patch('pdchaoskit.controls.client_session', spec=True)
@patch('pdchaoskit.controls.push_execution', spec=True)
def test_before_experiment_control(push_execution, session):
    # arrange
    experiment = data.provide_experiment()
    settings = data.provide_settings()
    push_execution.return_value = {"id": "12345"}

    # act
    controls.before_experiment_control(
        context=experiment, configuration={},
        secrets={}, settings=settings)

    assert settings.get('run_context').get('execution_id') == "12345"
    push_execution.assert_called_once_with(settings, ANY)


@patch('pdchaoskit.controls.client_session', spec=True)
@patch('pdchaoskit.controls.publish_event', spec=True)
def test_after_experiment_control(publish_event, session):
    # arrange
    experiment = data.provide_experiment()
    settings = data.provide_settings()
    journal = data.provide_journal()

    # act
    controls.after_experiment_control(
        context=experiment, state=journal,
        configuration={}, secrets={}, settings=settings)

    publish_event.assert_called_once_with(
        "after-experiment", None, journal, settings, ANY)


@patch('pdchaoskit.controls.client_session', spec=True)
@patch('pdchaoskit.controls.publish_event', spec=True)
def test_before_hypothesis_control(publish_event, session):
    # arrange
    settings = data.provide_settings()
    hypothesis = {"hypothesis": "hippo"}

    # act
    controls.before_hypothesis_control(
        context=hypothesis, state=None,
        configuration={}, secrets={}, settings=settings)

    publish_event.assert_called_once_with(
        "before-hypothesis", hypothesis, None, settings, ANY)


@patch('pdchaoskit.controls.client_session', spec=True)
@patch('pdchaoskit.controls.publish_event', spec=True)
def test_after_hypothesis_control(publish_event, session):
    # arrange
    settings = data.provide_settings()
    hypothesis = {"hypothesis": "hippo"}
    hypothesis_outcome = {"result": "maybe"}

    # act
    controls.after_hypothesis_control(
        context=hypothesis, state=hypothesis_outcome,
        configuration={}, secrets={}, settings=settings)

    publish_event.assert_called_once_with(
        "after-hypothesis", hypothesis, hypothesis_outcome, settings, ANY)


@patch('pdchaoskit.controls.client_session', spec=True)
@patch('pdchaoskit.controls.publish_event', spec=True)
def test_before_method_control(publish_event, session):
    # arrange
    experiment = data.provide_experiment()
    settings = data.provide_settings()

    # act
    controls.before_method_control(
        context=experiment, state=None,
        configuration={}, secrets={}, settings=settings)

    publish_event.assert_called_once_with(
        "before-method", experiment, None, settings, ANY)


@patch('pdchaoskit.controls.client_session', spec=True)
@patch('pdchaoskit.controls.publish_event', spec=True)
def test_after_method_control(publish_event, session):
    # arrange
    experiment = data.provide_experiment()
    settings = data.provide_settings()
    method_outcome = [{"result": "maybe"}]

    # act
    controls.after_method_control(
        context=experiment, state=method_outcome,
        configuration={}, secrets={}, settings=settings)

    publish_event.assert_called_once_with(
        "after-method", experiment, method_outcome, settings, ANY)


@patch('pdchaoskit.controls.client_session', spec=True)
@patch('pdchaoskit.controls.publish_event', spec=True)
def test_before_rollback_control(publish_event, session):
    # arrange
    experiment = data.provide_experiment()
    settings = data.provide_settings()

    # act
    controls.before_rollback_control(
        context=experiment, state=None,
        configuration={}, secrets={}, settings=settings)

    publish_event.assert_called_once_with(
        "before-rollback", experiment, None, settings, ANY)


@patch('pdchaoskit.controls.client_session', spec=True)
@patch('pdchaoskit.controls.publish_event', spec=True)
def test_after_rollback_control(publish_event, session):
    # arrange
    experiment = data.provide_experiment()
    settings = data.provide_settings()
    method_outcome = [{"result": "maybe"}]

    # act
    controls.after_rollback_control(
        context=experiment, state=method_outcome,
        configuration={}, secrets={}, settings=settings)

    publish_event.assert_called_once_with(
        "after-rollback", experiment, method_outcome, settings, ANY)


@patch('pdchaoskit.controls.client_session', spec=True)
@patch('pdchaoskit.controls.publish_event', spec=True)
def test_before_activity_control(publish_event, session):
    # arrange
    settings = data.provide_settings()
    activity = {"activity": "my_activity"}

    # act
    controls.before_activity_control(
        context=activity, state=None,
        configuration={}, secrets={}, settings=settings)

    publish_event.assert_called_once_with(
        "before-activity", activity, None, settings, ANY)


@patch('pdchaoskit.controls.client_session', spec=True)
@patch('pdchaoskit.controls.publish_event', spec=True)
def test_after_activity_control(publish_event, session):
    # arrange
    settings = data.provide_settings()
    activity = {"activity": "my_activity"}
    activity_outcome = {"result": "maybe"}

    # act
    controls.after_activity_control(
        context=activity, state=activity_outcome,
        configuration={}, secrets={}, settings=settings)

    publish_event.assert_called_once_with(
        "after-activity", activity, activity_outcome, settings, ANY)


@patch('pdchaoskit.controls.no_upload', spec=True)
def test_no_upload(no_upload_mock):
    # arrange
    no_upload_mock.return_value = True
    settings = {}

    # act
    controls.before_experiment_control(context=None, settings=settings)
    controls.after_experiment_control(context=None, state=None, settings=settings)
    controls.before_hypothesis_control(context=None, settings=settings)
    controls.after_hypothesis_control(context=None, state=None, settings=settings)
    controls.before_method_control(context=None, settings=settings)
    controls.after_method_control(context=None, state=None, settings=settings)
    controls.before_rollback_control(context=None, settings=settings)
    controls.after_rollback_control(context=None, state=None, settings=settings)
    controls.before_activity_control(context=None, settings=settings)
    controls.after_activity_control(context=None, state=None, settings=settings)

    assert no_upload_mock.call_count == 10
