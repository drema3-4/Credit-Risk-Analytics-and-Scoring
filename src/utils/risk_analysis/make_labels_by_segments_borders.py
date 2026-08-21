def make_labels(
    segments: list[float]
) -> list[str]:
    labels = []
    
    for i in range(len(segments) - 1):
        left = segments[i]
        right = segments[i + 1]

        if i == 0:
            labels.append(f"[{left}, {right}]")
        else:
            labels.append(f"({left}, {right}]")

    return labels