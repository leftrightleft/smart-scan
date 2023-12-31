# Smart Scan Bot
Smart-scan is an AI assistant that helps decide when to run a security analysis using CodeQL.  Not every PR needs to have a CodeQL scan run. Sometimes, you're only updating a markdown file, or maybe you're only changing pieces of code that have no potential security impact. 

The Smart Scan Bot reviews the changes in your PR (using GPT) and skips the CodeQL scan when you open a PR that doesn't impact your source code.

## How it works
Smart-scan is an action backed by OpenAI.  When a PR is triggered, this action sends the diff to GPT where a decision is made about the change.  If the change impacts the operation of your application, smart-scan triggers a CodeQL scan for an in-depth SAST scan.  If there are no operational changes to the application, the CodeQL scan is skipped :+1:.  

Smart Scan only operates on new PRs and changes to existing PRs.  CodeQL is still run when the PR is merged and every time a change is directly committed. 

Smart scan can be used directly with the OpenAI API, or you can use your own Azure OpenAI API instance.

**Here's a screenshot of smart-scan in action**

![image](https://github.com/leftrightleft/smart-scan/assets/4910518/73565ce7-b74b-4713-a1ca-d514b7f1a2ba)


## How to use smart-scan with the OpenAI API

You can check out our example workflows [here](./examples)

* First, you'll need to have an OpenAI account and API token.  Take a look at the [OpenAI intro documentation](https://platform.openai.com/docs/introduction) for steps on creating an account and provisioning a token.
* Enter your OpenAI API key as a new Actions secret called `OPENAI_KEY`
* Edit your `codeql.yml` workflow to add this action as a new job before your `analyze` job:
  ```
  jobs:
    smart_scan:
      name: "run smart scan"
      runs-on: ubuntu-latest
      permissions:
        pull-requests: write
        contents: read
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
* Edit the `analyze` job to only trigger on completion of the `smart_scan` job using the `needs:` and `if:` statements below.  This makes it so your CodeQL scan will always default to scan even if there's an error with smart-scan.
  ```
    analyze:
      needs: smart_scan
      if: ${{ always() && needs.smart_scan.outputs.decision == 'yes' }}
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



## How to use smart-scan with the Azure OpenAI Service API

You can check out our example workflows [here](./examples)

* Provision an Azure OpenAI Service resource.  The steps for this are in the [Azure OpenAI Service documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/) 
* Enter your Azure API key as a new Actions secret called `AZURE_OPENAI_KEY`
* Enter your Azure model name as a new Actions secret called `AZURE_OPENAI_MODEL`
* Enter your Azure endpoint url as a secret called `AZURE_OPENAI_ENDPOINT`
* Enter your Azure deployment ID as an Actions secret called `AZURE_OPENAI_DEPLOYMENT_ID`
* Edit your `codeql.yml` workflow to add this action as a new job before your `analyze` job:
  ```
  jobs:
    smart_scan:
      name: "Run smart scan"
      runs-on: ubuntu-latest
      permissions:
        pull-requests: write
        contents: read
      outputs:
        decision: ${{ steps.decide.outputs.decision }}
      steps:
        - uses: leftrightleft/smart-scan@main
          id: decide 
          with:
            gh_token: ${{ secrets.GITHUB_TOKEN }}
            model: ${{ secrets.AZURE_OPENAI_MODEL }}
            azure_api_key: ${{ secrets.AZURE_OPENAI_KEY }}
            azure_endpoint: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
            azure_deployment_id: ${{ secrets.AZURE_OPENAI_DEPLOYMENT_ID }}
      ...
  ```
* Edit the `analyze` job to only trigger on completion of the `smart_scan` job using the `needs:` and `if:` statements below.  This makes it so your CodeQL scan will always default to scan even if there's an error with smart-scan.
  ```
    analyze:
      needs: smart_scan
      if: ${{ always() && needs.smart_scan.outputs.decision == 'yes' }}
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
