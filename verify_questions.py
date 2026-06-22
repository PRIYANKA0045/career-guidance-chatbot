import json
import sys

def verify_questionnaire():
    try:
        with open("questions.json", "r") as f:
            questions = json.load(f)
    except Exception as e:
        print(f"Error loading questions.json: {e}")
        sys.exit(1)

    print(f"Loaded {len(questions)} questions from questions.json.")
    
    # Store all path results
    paths = []
    errors = []

    def dfs(current_id, path, visited):
        if current_id is None:
            # We reached a terminal state
            paths.append(path)
            return

        if current_id not in questions:
            errors.append(f"Broken Link: Question ID '{current_id}' referenced but does not exist in questions.json. Path: {' -> '.join(path)}")
            return

        if current_id in visited:
            errors.append(f"Cycle Detected: Question ID '{current_id}' already visited in path. Path: {' -> '.join(path)} -> {current_id}")
            return

        # Visit current node
        new_path = path + [current_id]
        new_visited = visited | {current_id}
        
        q_data = questions[current_id]
        options = q_data.get("options", [])
        
        if not options:
            errors.append(f"No Options: Question '{current_id}' has no options. Path: {' -> '.join(new_path)}")
            return

        for opt in options:
            next_q = opt.get("next_question")
            dfs(next_q, new_path, new_visited)

    # Start DFS traversal from root "q1"
    dfs("q1", [], set())

    # Analyze paths
    print(f"\nTotal unique paths traversed: {len(paths)}")
    
    path_lengths = [len(p) for p in paths]
    length_distribution = {}
    for length in path_lengths:
        length_distribution[length] = length_distribution.get(length, 0) + 1
        
    print("Path length distribution:")
    for length, count in sorted(length_distribution.items()):
        print(f"  Length {length}: {count} paths")

    # Check if all paths are exactly 10 questions long
    non_10_paths = [p for p in paths if len(p) != 10]
    if non_10_paths:
        errors.append(f"Invalid Path Lengths: Found {len(non_10_paths)} paths that are not exactly 10 questions long.")
        for p in non_10_paths[:5]:
            print(f"  Example bad path (length {len(p)}): {' -> '.join(p)}")
        if len(non_10_paths) > 5:
            print(f"  ... and {len(non_10_paths) - 5} more.")

    # Report errors
    if errors:
        print("\n[FAILED] VERIFICATION FAILED with the following errors:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("\n[SUCCESS] VERIFICATION SUCCESSFUL! All paths are exactly 10 questions deep, with zero cycles or broken links.")

if __name__ == "__main__":
    verify_questionnaire()
