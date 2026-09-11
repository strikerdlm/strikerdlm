# Maintaining this profile

This is a GitHub profile README, not a separately deployed website. GitHub renders
`README.md` directly. No build, package install, deployment, API token or GitHub
Actions workflow is needed for the profile.

## Edit

- Update the biography, research focus, project descriptions and contacts in `README.md`.
- Keep the project showcase short and link each project only once.
- Verify project visibility while signed out before adding a repository. Label forks
  and experimental software accurately; do not imply clinical validation.
- Edit the two SVGs in `assets/` together. They are self-contained, static artwork
  for light and dark themes, not telemetry. No external fonts or scripts are loaded.
- Keep image paths relative so branch previews and the merged profile both work.
- Do not reintroduce live badge/stat services, generated contribution graphics,
  counters or scheduled profile workflows.

## Check locally (optional; Python 3.9+)

```sh
python -m unittest discover -s tests -v
```

These checks use only the Python standard library. They verify local image paths,
static SVG structure, the absence of profile workflows, unique curated project
links and basic content constraints. They do not verify live link availability or
current repository visibility. Update the expected project list in the tests when
intentionally changing the showcase.

Preview on GitHub in both themes and at a narrow viewport. The name, biography,
project links and contact links remain native selectable text, not an image.

## Retired automation

The Metrics, 3D Contribution Graph and Snake Animation workflows and their unused
main-branch SVG output files were removed. Their previous versions remain in Git
history. The old `output` branch and historical workflow runs are not deleted.
Once this change is merged into the default branch, those three workflow files no
longer schedule new runs. Any already queued or running jobs require separate
cancellation if applicable. No account-wide Actions or billing settings are changed.
