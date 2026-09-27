# TODO

## Backlog

- Feature 10: add a nice icon to the program

- Feature 6: Add an installer for Windows (should it comprehend a ffmpeg too? maybe used only if not already present in the system?)

- Feature 8: cleanup project structure
  rename folder ui-text to "localization" or "L10N"
  rename "libs" to "src"
  move all .py files (apart main.py and tests) to the "src" folder

  Better ideas?

- Feature 9 | UX: Move split result status below action button

  Goal
  Make the split operation feedback easier to understand by placing it where users expect the result of the action to appear.

  Changes
    - Move the status text from the top of the window to directly below the `Split` button.
    - Reserve a fixed status area below the button for progress, success, and error messages.
    - Keep feedback in the main window rather than showing a separate success dialog.

  Rationale

    The intended interaction flow is:

    1. Select an MP3 file.
    2. Configure output options.
    3. Click `Split`.
    4. Read the operation result.

    Putting the status below the action button visually connects it to the operation that generated it and avoids competing with the file-selection controls.

  Status message examples

    | State | Message |
    |---|---|
    | In progress | `Splitting file…` |
    | Success | `✓ Done — 11 parts created` |
    | Error | `Could not split the file: invalid MP3` |

  Visual details

    - Display successful completion with a green checkmark or green status text.
    - Use an error color for failures.

  
  
## Done (last 20 teaks)

- Feature 7: The internal log will be replaced by a log file, plus a button that shows it when an operation fails.
