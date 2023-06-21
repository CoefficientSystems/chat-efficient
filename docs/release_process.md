# Release Process

> This process follows [this Git Flow release model](https://nvie.com/posts/a-successful-git-branching-model/).
> There is an excellent [Git Flow cheatsheet here](https://danielkummer.github.io/git-flow-cheatsheet/).
> You will need to install the Git Flow helper extension: `brew install git-flow-avh` and
> initialise your repo (see the cheatsheet above, or this can also be done from within Sourcetree).

**Replace VERSION with the relevant milestone, e.g. `0.3`**


## 1. CLI Steps

Sourcetree has great built-in support for Git Flow from the `Repository > Git flow` menu. We list
the commands below, but this can also be done via the GUI if you prefer.

```sh
# Ensure your working copy is clean before starting (e.g. stash any WIP).
# Fetch & pull latest origin/develop
git fetch && git checkout develop && git pull

# Locally, start a new release
git flow release start VERSION

# Summary of actions:
# - A new branch 'release/VERSION' was created, based on 'develop'
# - You are now on branch 'release/VERSION'

# Follow-up actions:
# - Bump the version number now!
# - Start committing last-minute fixes in preparing your release (e.g. towncrier)
# - Use amend commits here if possible to keep commits to a minimum
#   git commit --amend -m "updated commit message"
# - You don't have to push the release branch unless a) you'd like it reviewed, b) to run CI, c) others may wish to add commits to this release.

# Towncrier update
# - Review all towncrier entries.
# - Any missing vs issues closed within the milestone (don't forget bugs & maintenance)? Do the entries look good?
# - (Optional) towncrier preview: `towncrier build --version=VERSION --draft`
# - Publish towncrier update: `towncrier build --version=VERSION`
# - Add any additional notes to the CHANGELOG.md as required

# Update project version number
# - This is in [poetry] section at the top of pyproject.toml

# (Optional) pre-commit
# - You shouldn't need to run pre-commit unless you've changed things manually
# - If you're seeing changes to poetry.lock, try clearing your Poetry cache & run again
poetry cache clear pypi --all
pre-commit run --all-files --hook-stage=manual

# Commit & amend commit as required

# (Optional) If others have commits to add to this release, you can push as follows
git flow release publish VERSION

# Complete the release by merging back into `main` and `develop`
# - Add -k if you do not want to auto-delete the release branch
# - Add -p if you want to auto-push to origin
# - Just use "Release VERSION" as commit messages
git flow release finish -n VERSION

# Summary of actions:
# - Release branch 'release/VERSION' has been merged into 'main'
# - Master branch 'main' has been back-merged into 'develop'
# - Release branch 'release/VERSION' is still locally available
# - You are now on branch 'develop'

# Tag the release
git checkout main
git tag VERSION
git push origin --tags

# Check everything over, if you're happy, push `develop`, push `main` and delete your release branch.
git checkout develop && git push
git checkout main && git push
git branch -D release/VERSION
```

## 2. GitHub Steps

  - Copy the **raw markdown** for the release notes in CHANGELOG: [https://github.com/CoefficientSystems/coefficient-cookiecutter/blob/main/CHANGELOG.md]
  - Once you've pushed the tag, you will see it on this page: [https://github.com/CoefficientSystems/coefficient-cookiecutter/tags]
  - Edit the tag and add the release notes
  - You will then see the release appear here: [https://github.com/CoefficientSystems/coefficient-cookiecutter/releases]
  - This also sends an email update to anyone on the team who has subscribed containing formatted release notes.
  - Once the release is created, edit the release and assign the milestone to the release. Save changes.

To finish, copy the release notes and post in any relevant Slack channel or email lists to inform members about the release.
