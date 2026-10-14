## HOW THIS RUN WORKS (BINDING)

You are running headless on a schedule. Nobody will answer questions and there is no follow-up turn.

- **Your working directory is an empty staging folder.** Write every output file into it, using
  exactly the relative file names listed under OUTPUT FILES. Write nothing anywhere else.
- **Do not run git**, do not create sidecar or scratch files in the staging folder, and do not
  generate images yourself — the runner renders the cover from the `cover_prompt` you return.
- **Skills** listed in this prompt are installed in this folder's `{{SKILLS_DIR}}/`. Load each one
  with your skill tool (Claude Code: the Skill tool) or by reading its `SKILL.md`. Don't web-search
  for a skill.
- **Your final message is machine-read.** End with exactly one JSON object in a ```json fenced
  block, with the keys listed under FINAL MESSAGE. No prose after it.
- If you cannot finish (no usable research, a requirement you can't meet), still end with the JSON
  block and set `"error"` to a one-line reason. The runner fails the run cleanly and publishes
  nothing.
