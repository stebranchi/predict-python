import numpy as np
import pandas as pd
from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier

from encoders.log_util import DEFAULT_COLUMNS, remaining_time, elapsed_time, DEFAULT_COLUMNS_NO_LABEL

CLASSIFIER = XEventAttributeClassifier("Trace name", ["concept:name"])


def boolean(log: list, event_names: list, add_label=True, add_elapsed_time=True):
    return encode_boolean_frequency(log, event_names, is_boolean=True, add_label=add_label,
                                    add_elapsed_time=add_elapsed_time)


def frequency(log: list, event_names: list, add_label=True, add_elapsed_time=True):
    return encode_boolean_frequency(log, event_names, is_boolean=False, add_label=add_label,
                                    add_elapsed_time=add_elapsed_time)


def encode_boolean_frequency(log: list, event_names: list, add_label: bool, add_elapsed_time: bool, is_boolean=True):
    """Encodes the log by boolean or frequency

    :param add_label If to add remaining_time and elapsed_time columns
    :return pandas dataframe
    """
    if add_label and add_elapsed_time:
        columns = np.append(event_names, list(DEFAULT_COLUMNS))
    elif add_label:
        columns = np.append(event_names, ["trace_id", "event_nr", "remaining_time"])
    else:
        columns = np.append(event_names, list(DEFAULT_COLUMNS_NO_LABEL))
    encoded_data = []

    for trace in log:
        trace_name = CLASSIFIER.get_class_identity(trace)
        # starts with all False, changes to event
        event_happened = create_event_happened(event_names, is_boolean)
        for event_index, event in enumerate(trace):
            trace_row = []
            update_event_happened(event, event_names, event_happened, is_boolean)
            trace_row += event_happened

            trace_row.append(trace_name)
            # Start counting at 1
            trace_row.append(event_index + 1)
            if add_label:
                trace_row.append(remaining_time(trace, event))
                if add_elapsed_time:
                    trace_row.append(elapsed_time(trace, event))
            encoded_data.append(trace_row)
    return pd.DataFrame(columns=columns, data=encoded_data)


def create_event_happened(event_names: list, is_boolean: bool):
    """Creates list of event happened placeholders"""
    if is_boolean:
        return [False] * len(event_names)
    return [0] * len(event_names)


def update_event_happened(event, event_names: list, event_happened: list, is_boolean: bool):
    """Updates the event_happened list at event index

    For boolean set happened to True.
    For frequency updates happened count.
    """
    event_name = CLASSIFIER.get_class_identity(event)
    event_index = event_names.index(event_name)
    if is_boolean:
        event_happened[event_index] = True
    else:
        event_happened[event_index] += 1
