import subprocess

def run_bash(function, capture_return, *args):
    result = subprocess.run(["bash", "distributor.sh", function, *args], capture_output=capture_return, text=True)
    if capture_return:
        return result.stdout.strip()

def is_valid_number(value):
    return value.isdigit() and int(value) > 0

# menu:
# 1 - add new commits
# 2 - redistribute commits
# 3 - delete n commits
# 4 - undo last action

# distribution
# --- dates ---
# equally spread
# once every n days
# overlapping ranges
# fully random
# --- time ---
# withing a range (ranges)
# exclude a range (ranges)

def main():
    while True:
        mode = input("Welcome! Would you like to generate new commits(1) or redistribute the existing ones(2)?\nor delete commits(3)?")
        if mode not in ["1", "2", "3"]:
            print("Invalid input. Please enter 1 to generate new commits or 2 to redistribute the existing ones.\n")
        else:
            break

    try:
        existing_commits = int(run_bash("get_commit_count", True))
    except Exception:
        existing_commits = 0
    print(f"There are currently {existing_commits} commits in this repo")



    if mode == "1":
        while True:
            n_commits = input("Enter the number of commits to generate: ")
            if is_valid_number(n_commits):
                n_commits = int(n_commits)
                break
            print("Invalid input. Please enter a valid number.")

        print(f"Adding {n_commits} new commits")
        run_bash("add_new_commits", False, str(n_commits))
        print(n_commits, " new commits added.")

    elif mode == "2":
        num = int(input("Enter the number of commits to redistribute:"))
        if num > existing_commits:
            print("Not enough commits to redistribute, add more to proceed.")
            return
        print("Redistributing existing commits...")
        if num == existing_commits:
            print("Cannot move the original commit. Decreasing the requested number by 1.")
            num -= 1
            if num == 0:
                print("Not enough commits do redistribute. Add at least one more to proceed. Exiting.")
                return
        run_bash("redistribute_commits", False, str(num))
        print("Commits redistributed.")

    elif mode == "3":
        n = int(input("Enter the number of the last commits to delete:"))
        if n > existing_commits:
            print("You are trying to delete more commits than there are. Exiting.")
            return
        print(f"Deleting your last {n} commits...")
        run_bash("delete_commits", False, str(n))
        print(f"Successfully deleted {n} commits.")


#def create_range()


if __name__ == "__main__":
    is_in_repo = run_bash("is_in_repo", True)
    if is_in_repo != "true":
        print("You are not inside a git repository. Exiting.")
        exit(1)
    main()
