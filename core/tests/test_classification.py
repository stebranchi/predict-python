from django.test import TestCase

from core.core import calculate
from core.tests.test_prepare import split_double, add_default_config


class TestClassification(TestCase):
    """Proof of concept tests"""

    def results(self):
        return {'f1score': 0.6666666666666666, 'acc': 0.5, 'auc': 0.16666666666666666, 'false_negative': 0,
                'false_positive': 1, 'true_positive': 1, 'true_negative': 0, 'precision': 0.5, 'recall': 1.0}

    def results2(self):
        return {'f1score': 0.6666666666666666, 'auc': 0.5, 'acc': 0.5, 'false_negative': 0, 'false_positive': 1,
                'true_positive': 1, 'true_negative': 0, 'precision': 0.5, 'recall': 1.0}

    def results3(self):
        return {'f1score': 0.3333333333333333, 'acc': 0.5, 'auc': 0, 'precision': 0.5, 'recall': 0.5}

    def get_job(self):
        json = dict()
        json["clustering"] = "kmeans"
        json["split"] = split_double()
        json["method"] = "randomForest"
        json["encoding"] = "simpleIndex"
        json["rule"] = "remaining_time"
        json["prefix_length"] = 1
        json["threshold"] = "default"
        json["type"] = "classification"
        json["padding"] = 'zero_padding'
        return json

    def test_class_randomForest(self):
        job = self.get_job()
        job['clustering'] = 'noCluster'
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result, self.results2())

    def test_class_KNN(self):
        job = self.get_job()
        job['method'] = 'knn'
        job['clustering'] = 'noCluster'
        job['classification.knn'] = {'n_neighbors': 3}
        result, _ = calculate(job)
        self.assertIsNotNone(result)

    def test_class_DecisionTree(self):
        job = self.get_job()
        job['method'] = 'decisionTree'
        add_default_config(job)
        result, _ = calculate(job)
        self.assertIsNotNone(result)

    def test_next_activity_randomForest(self):
        job = self.get_job()
        job['type'] = 'nextActivity'
        add_default_config(job)
        result, _ = calculate(job)
        self.assertIsNotNone(result)

    def test_next_activity_KNN(self):
        job = self.get_job()
        job['method'] = 'knn'
        job['type'] = 'nextActivity'
        job['nextActivity.knn'] = {'n_neighbors': 3}
        result, _ = calculate(job)
        self.assertIsNotNone(result)

    def test_next_activity_DecisionTree(self):
        job = self.get_job()
        job['method'] = 'decisionTree'
        job['type'] = 'nextActivity'
        job['clustering'] = 'noCluster'
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result, self.results3())

    def test_class_complex(self):
        job = self.get_job()
        job['clustering'] = 'noCluster'
        job["encoding"] = "complex"
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result, self.results2())

    def test_class_complex_zero_padding(self):
        job = self.get_job()
        job['clustering'] = 'noCluster'
        job["encoding"] = "complex"
        job["prefix_length"] = 8
        add_default_config(job)
        calculate(job)
        # it works, but results are unreliable

    def test_class_last_payload(self):
        job = self.get_job()
        job['clustering'] = 'noCluster'
        job["encoding"] = "lastPayload"
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result, self.results2())

    def test_class_last_payload_no_elapsed_time(self):
        job = self.get_job()
        job['clustering'] = 'noCluster'
        job["encoding"] = "lastPayload"
        job["add_elapsed_time"] = False
        add_default_config(job)
        result, _ = calculate(job)
        self.assertDictEqual(result, self.results2())
