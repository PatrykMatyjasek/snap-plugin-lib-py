#!/usr/bin/env python

# http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import random
import time

import snap_plugin.v1 as snap

LOG = logging.getLogger(__name__)


class RandomStream(snap.StreamCollector):
    """Rand

    Streams random int and float metrics
    """

    def stream(self):
        LOG.debug("Metrics streaming started")
        while True:
            time.sleep(1)
            metrics = []
            metric = snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="streaming"),
                    snap.NamespaceElement(value="random"),
                    snap.NamespaceElement(value="int")
                ],
                version=1,
                tags={"mtype": "gauge"},
                description="Random {}".format("int"),
                data=random.randint(1, 100)
            )
            metrics.append(metric)
            metric = snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="streaming"),
                    snap.NamespaceElement(value="random"),
                    snap.NamespaceElement(value="float")
                ],
                version=1,
                tags={"mtype": "gauge"},
                description="Random {}".format("float"),
                data=random.random()
            )
            metrics.append(metric)

            for mt in metrics:
                self.proxy.metrics_queue.put(mt)

    def update_catalog(self, config):
        LOG.debug("GetMetricTypes called")
        metrics = []
        for key in ("float64", "int64"):
            metric = snap.Metric(
                namespace=[
                    snap.NamespaceElement(value="intel"),
                    snap.NamespaceElement(value="streaming"),
                    snap.NamespaceElement(value="random"),
                    snap.NamespaceElement(value=key)
                ],
                version=1,
                tags={"mtype": "gauge"},
                description="Random {}".format(key),
            )
            metrics.append(metric)

        return metrics

    def get_config_policy(self):
        LOG.debug("GetConfigPolicy called")
        return snap.ConfigPolicy(
            [
                ("random-stream"),
                [
                    (
                        "int_max",
                        snap.IntegerRule(default=100, minimum=1, maximum=10000)
                    ),
                    (
                        "int_min",
                        snap.IntegerRule(default=0, minimum=0)
                    )
                ]
            ]
        )


if __name__ == "__main__":
    RandomStream("random-stream-py", 1).start_plugin()