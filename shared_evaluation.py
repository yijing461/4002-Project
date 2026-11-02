from collections import Counter

def intent_accuracy(gold, predicted):
    if len(gold) != len(predicted) or len(gold) == 0:
        raise ValueError("Answer lists must have equal, nonzero lengths")

    correct = 0

    for gold_label, predicted_label in zip(gold, predicted):
        if gold_label == predicted_label:
            correct += 1

    return 100 * correct / len(gold)

def decode_slots(tokens, tags):
    if len(tokens) != len(tags):
        raise ValueError("Token and tag lengths differ")

    slots = []
    current_type = None
    current_words = []

    for token, tag in list(zip(tokens, tags)) + [(None, "O")]:
        if tag.startswith("I-") and tag[2:] == current_type:
            current_words.append(token)
            continue

        if current_type is not None:
            slots.append((current_type, " ".join(current_words)))

        if tag == "O":
            current_type = None
            current_words = []
        elif tag.startswith(("B-", "I-")) and len(tag) > 2:
            current_type = tag[2:]
            current_words = [token]
        else:
            raise ValueError("Invalid tag: " + tag)

    return slots

def slot_micro_f1(gold_slots, predicted_slots):
    if len(gold_slots) != len(predicted_slots) or len(gold_slots) == 0:
        raise ValueError("Answer lists must have equal, nonzero lengths")

    tp = 0
    fp = 0
    fn = 0

    for gold, predicted in zip(gold_slots, predicted_slots):
        gold_counts = Counter(tuple(slot) for slot in gold)
        predicted_counts = Counter(tuple(slot) for slot in predicted)

        tp += sum((gold_counts & predicted_counts).values())
        fp += sum((predicted_counts - gold_counts).values())
        fn += sum((gold_counts - predicted_counts).values())

    denominator = 2 * tp + fp + fn
    f1 = 100 * 2 * tp / denominator if denominator else 0.0

    return {"slot_f1": f1, "tp": tp, "fp": fp, "fn": fn}

