is_valid_number() {
    [[ "$1" =~ ^[0-9]+$ ]]
}

get_commit_count()
{
  git rev-list --count HEAD
}

add_new_commits() {
    local num_commits="$1"  # Alias the first argument to a local variable
    local commit_file="commit.txt"
    for (( i=1; i<="$num_commits"; i++ )); do
        # Append unique content to the same file
        echo "Making commit $i" >> "$commit_file"
        git add "$commit_file"
        git commit -m "Commit $i"
    done
}


# Function to redistribute existing commits
redistribute_commits()
{
    GIT_SEQUENCE_EDITOR="sed -i 's/^pick/edit/'" git rebase -i HEAD~"$1"
    while git rebase --continue 2>/dev/null; do
       NEW_DATE="$(date -d "$((RANDOM % 365)) days ago" +"%Y-%m-%dT%H:%M:%S")"
       GIT_COMMITTER_DATE="$NEW_DATE" git commit --amend --no-edit --date="$NEW_DATE"
    done
}

delete_commits()
{
  GIT_SEQUENCE_EDITOR="sed -i 's/^pick/drop/'" git rebase -i HEAD~"$1"
}

is_in_repo()
{
  git rev-parse --is-inside-work-tree
}

greet()
{
  echo -e "hello, $1!\n"
}


"$@"
