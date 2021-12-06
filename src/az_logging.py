import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware

from opencensus.trace import config_integration
from opencensus.trace.samplers import AlwaysOnSampler, ProbabilitySampler
from opencensus.trace.tracer import Tracer


def wrap_the_app(role_name, app):
    config_integration.trace_integrations(['logging', 'requests'])
    logger = logging.getLogger(role_name)
    handler = AzureLogHandler()
    def set_envelope(envelope):
        envelope.tags['ai.cloud.role'] = role_name

    handler.add_telemetry_processor(set_envelope)
    logger.addHandler(handler)
    exporter = AzureExporter()
    exporter.add_telemetry_processor(set_envelope)
    sampler = AlwaysOnSampler()

    tracer = Tracer(sampler=sampler, exporter=exporter)

    middleware = FlaskMiddleware(
        app,
        exporter=exporter,
        sampler=sampler,
    )
    return logger, tracer

    
