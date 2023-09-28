# Smart Scan
Smart-scan is an AI assistant that helps decide when to run a security analysis using CodeQL.  Not every PR needs to have a CodeQL scan run. Sometimes, you're only updating a markdown file, or maybe you're only changing pieces of code that have no potential security impact.

This is an experiment to see if we can introduce CodeQL scans only when they're actually needed.  

## How it works
Smart-scan is an action backed by OpenAI.  When a PR is triggered, this action sends the diff to GPT where a deicion is made about the change.  If the change impacts the operation of your application, smart-scan triggers a CodeQL scan for an in-depth SAST scan.  If there are no operational changes to the application, the CodeQL scan is skipped.

## How to use smart-scan
* Enter your OpenAI API key as a new Actions secret called `OPENAI_KEY`
* Edit your `codeql.yml` workflow to add this action as a new job before your `analyze` job:
  ```
  jobs:
    smart_scan:
      name: "run smart scan"
      runs-on: ubuntu-latest
      outputs:
        decision: ${{ steps.decide.outputs.decision }}
      steps:
        - uses: leftrightleft/smart-scan@main
          id: decide 
          with:
            openai_api_key: ${{ secrets.OPENAI_KEY }}
            gh_token: ${{ secrets.GITHUB_TOKEN }}
    ...
  ```
* Edit the `analyze` job to only trigger on completion of the `smart_scan` job using the `needs:` and `if:` statements below:
  ```
    analyze:
      needs: smart_scan
      if: needs.smart_scan.outputs.decision == 'yes'
      name: Analyze
      # Runner size impacts CodeQL analysis time. To learn more, please see:
      #   - https://gh.io/recommended-hardware-resources-for-running-codeql
      #   - https://gh.io/supported-runners-and-hardware-resources
      #   - https://gh.io/using-larger-runners
      # Consider using larger runners for possible analysis time improvements.
      runs-on: ${{ (matrix.language == 'swift' && 'macos-latest') || 'ubuntu-latest' }}
      timeout-minutes: ${{ (matrix.language == 'swift' && 120) || 360 }}
      permissions:
        actions: read
        contents: read
        security-events: write
  ```

Here's a full example workflow for a python repository:
```
# For most projects, this workflow file will not need changing; you simply need
# to commit it to your repository.
#
# You may wish to alter this file to override the set of languages analyzed,
# or to provide custom queries or build logic.
#
# ******** NOTE ********
# We have attempted to detect the languages in your repository. Please check
# the `language` matrix defined below to confirm you have the correct set of
# supported CodeQL languages.
#
name: "CodeQL"

on:
  push:
    branches: [ "main" ]
  pull_request:
    # The branches below must be a subset of the branches above
    branches: [ "main" ]
  schedule:
    - cron: '42 11 * * 2'

jobs:
  smart_scan:
    name: "run smart scan"
    runs-on: ubuntu-latest
    outputs:
      decision: ${{ steps.decide.outputs.decision }}
    steps:
      - uses: leftrightleft/smart-scan@main
        id: decide 
        with:
          openai_api_key: ${{ secrets.OPENAI_KEY }}
          gh_token: ${{ secrets.GITHUB_TOKEN }}
  
  analyze:
    needs: smart_scan
    if: needs.smart_scan.outputs.decision == 'yes'
    name: Analyze
    # Runner size impacts CodeQL analysis time. To learn more, please see:
    #   - https://gh.io/recommended-hardware-resources-for-running-codeql
    #   - https://gh.io/supported-runners-and-hardware-resources
    #   - https://gh.io/using-larger-runners
    # Consider using larger runners for possible analysis time improvements.
    runs-on: ${{ (matrix.language == 'swift' && 'macos-latest') || 'ubuntu-latest' }}
    timeout-minutes: ${{ (matrix.language == 'swift' && 120) || 360 }}
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: [ 'python' ]
        # CodeQL supports [ 'cpp', 'csharp', 'go', 'java', 'javascript', 'python', 'ruby', 'swift' ]
        # Use only 'java' to analyze code written in Java, Kotlin or both
        # Use only 'javascript' to analyze code written in JavaScript, TypeScript or both
        # Learn more about CodeQL language support at https://aka.ms/codeql-docs/language-support

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    # Initializes the CodeQL tools for scanning.
    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: ${{ matrix.language }}
        # If you wish to specify custom queries, you can do so here or in a config file.
        # By default, queries listed here will override any specified in a config file.
        # Prefix the list here with "+" to use these queries and those in the config file.

        # For more details on CodeQL's query packs, refer to: https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/configuring-code-scanning#using-queries-in-ql-packs
        # queries: security-extended,security-and-quality


    # Autobuild attempts to build any compiled languages (C/C++, C#, Go, Java, or Swift).
    # If this step fails, then you should remove it and run the build manually (see below)
    - name: Autobuild
      uses: github/codeql-action/autobuild@v2

    # ℹ️ Command-line programs to run using the OS shell.
    # 📚 See https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsrun

    #   If the Autobuild fails above, remove it and uncomment the following three lines.
    #   modify them (or add more) to build your code if your project, please refer to the EXAMPLE below for guidance.

    # - run: |
    #     echo "Run, Build Application using script"
    #     ./location_of_script_within_repo/buildscript.sh

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2
      with:
        category: "/language:${{matrix.language}}"
```
