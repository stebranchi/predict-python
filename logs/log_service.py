from collections import defaultdict, OrderedDict

from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier


def events_by_date(logs):
    """Creates dict of events by date ordered by date

    :return {'2010-12-30': 7, '2011-01-06': 8}
    :rtype: OrderedDict
    """
    classifier = XEventAttributeClassifier("Event", ["time:timestamp"])
    stamp_dict = defaultdict(lambda: 0)
    for log in logs:
        for trace in log:
            for event in trace:
                timestamp = classifier.get_class_identity(event)
                date = timestamp.split("T")[0]
                stamp_dict[date] += 1
    return OrderedDict(sorted(stamp_dict.items()))


def resources_by_date(logs):
    """Creates dict of used unique resources ordered by date

    Resource and timestamp delimited by &&. If this is in resources name, bad stuff will happen.
    Returns a dict with a date and the number of unique resources used on that day.
    :return {'2010-12-30': 7, '2011-01-06': 8}
    :rtype: OrderedDict
    """
    classifier = XEventAttributeClassifier("Resource", ["Resource", "time:timestamp"])
    stamp_dict = defaultdict(lambda: [])
    for log in logs:
        for trace in log:
            for event in trace:
                resource_and_timestamp = classifier.get_class_identity(event)
                resource = resource_and_timestamp.split("&&")[0]
                timestamp = resource_and_timestamp.split("&&")[1]
                date = timestamp.split("T")[0]
                stamp_dict[date].append(resource)

    for key, value in stamp_dict.items():
        stamp_dict[key] = len(set(value))

    return OrderedDict(sorted(stamp_dict.items()))


def event_executions(logs):
    """Creates dict of event execution count

    :return {'Event A': 7, '2011-01-06': 8}
    :rtype: OrderedDict
    """
    classifier = XEventAttributeClassifier("Event", ["concept:name"])
    executions = defaultdict(lambda: 0)
    for log in logs:
        for trace in log:
            for event in trace:
                event_name = classifier.get_class_identity(event)
                executions[event_name] += 1
    return OrderedDict(sorted(executions.items()))
