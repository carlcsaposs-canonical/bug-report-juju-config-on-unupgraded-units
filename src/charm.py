#!/usr/bin/env python3
# Copyright 2023 Ubuntu
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following tutorial that will help you
develop a new k8s charm using the Operator Framework:

https://juju.is/docs/sdk/create-a-minimal-kubernetes-charm
"""

import logging

import ops
import lightkube
import lightkube.resources.apps_v1

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)


class BarCharm(ops.CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.stop, self._on_stop)

    def _on_config_changed(self, _):
        logger.info(f'{self.config["pause_after_unit_refresh"]=}')

    def _on_stop(self, _):
        partition = int(self.unit.name.split("/")[-1])
        lightkube.Client().patch(
            res=lightkube.resources.apps_v1.StatefulSet,
            name=self.app.name,
            obj={
                "spec": {"updateStrategy": {"rollingUpdate": {"partition": partition}}}
            },
        )


if __name__ == "__main__":  # pragma: nocover
    ops.main(BarCharm)  # type: ignore
