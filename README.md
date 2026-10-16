# TaskBoard — Full-Stack DevOps Capstone Project

> A production-oriented SaaS task management application demonstrating the **complete software delivery lifecycle**: development → testing → containerization → security scanning → CI/CD → cloud infrastructure → Kubernetes deployment → monitoring → troubleshooting.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Features](#3-features)
4. [Technology Stack](#4-technology-stack)
5. [Repository Structure](#5-repository-structure)
6. [Prerequisites](#6-prerequisites)
7. [Local Docker Compose Setup](#7-local-docker-compose-setup)
8. [Backend Development Setup](#8-backend-development-setup)
9. [Frontend Development Setup](#9-frontend-development-setup)
10. [Environment Variables](#10-environment-variables)
11. [Database Migrations](#11-database-migrations)
12. [Testing](#12-testing)
13. [Git & GitHub Workflow](#13-git--github-workflow)
14. [Docker Build Instructions](#14-docker-build-instructions)
15. [CI/CD Pipeline](#15-cicd-pipeline)
16. [Trivy Security Scanning](#16-trivy-security-scanning)
17. [GHCR Image Publishing](#17-ghcr-image-publishing)
18. [Terraform AWS Infrastructure](#18-terraform-aws-infrastructure)
19. [AWS EKS Configuration](#19-aws-eks-configuration)
20. [Kubernetes Deployment](#20-kubernetes-deployment)
21. [Helm Operations](#21-helm-operations)
22. [Ingress Configuration](#22-ingress-configuration)
23. [HPA & Load Testing](#23-hpa--load-testing)
24. [Prometheus & Grafana](#24-prometheus--grafana)
25. [Troubleshooting Exercises](#25-troubleshooting-exercises)
26. [Security Considerations](#26-security-considerations)
27. [AWS Cost Management & Cleanup](#27-aws-cost-management--cleanup)
28. [Final Demonstration Checklist](#28-final-demonstration-checklist)
29. [Known Limitations](#29-known-limitations)
30. [Future Improvements](#30-future-improvements)

---

## 01. Application

### Objective

Develop and run the TaskBoard application, verifying that its frontend and backend operate correctly before containerization and deployment.

### Technology Stack

- Frontend: To be verified from the project configuration
- Backend: Python
- Container orchestration: Docker Compose

### Execution

Commands and configuration will be documented after verifying the application's actual startup procedure.

### Verification

The application must start successfully, and its backend health endpoint or an appropriate application request must return a successful response.

### Screenshots

**Application Running**

![Application running](screenshots/01-application/application-running.png)

**Application Test**

![Application test](screenshots/01-application/application-test.png)

# Stage 2: Git Commit and Version Control

## 2.1 Objective

Use Git to track project changes, create commits, and manage the TaskBoard project's source code using GitHub.

## 2.2 Tools Used

- Git
- GitHub
- PowerShell
- Visual Studio Code

## 2.3 Implementation and Screenshots

### Step 1: Check Git Repository Status

**Command:**

```powershell
git status
```

**Screenshot:** Save the terminal output as `screenshots/02-git-commit/01-git-status.png`.

![Git repository status](screenshots/02-git-commit/01-git-status.png)

### Step 2: Review Code Changes

**Command:**

```powershell
git diff
```

**Screenshot:** Save the terminal output as `screenshots/02-git-commit/02-git-diff.png`.

![Git diff output](screenshots/02-git-commit/02-git-diff.png)

### Step 3: Stage Project Files

**Security check:** Ensure `.env` and other secret files are excluded by `.gitignore` before staging.

**Command:**

```powershell
git add .
```

**Screenshot:** Save the staging/status evidence as `screenshots/02-git-commit/03-git-staging.png`.

![Git staging evidence](screenshots/02-git-commit/03-git-staging.png)

### Step 4: Verify Staged Changes

**Command:**

```powershell
git status
```

**Screenshot:** Save the output showing staged files as `screenshots/02-git-commit/04-staged-status.png`.

![Staged Git changes](screenshots/02-git-commit/04-staged-status.png)

### Step 5: Create a Commit

**Command:**

```powershell
git commit -m "Add TaskBoard DevOps capstone application"
```

**Screenshot:** Save the successful commit output as `screenshots/02-git-commit/05-git-commit.png`.

![Successful Git commit](screenshots/02-git-commit/05-git-commit.png)

### Step 6: Verify Commit History

**Command:**

```powershell
git log -1 --oneline
```

**Screenshot:** Save the commit hash and message as `screenshots/02-git-commit/06-git-log.png`.

![Git commit history](screenshots/02-git-commit/06-git-log.png)

### Step 7: Verify the Current Branch

**Command:**

```powershell
git branch
```

**Screenshot:** Save the active branch output as `screenshots/02-git-commit/07-git-branch.png`.

![Current Git branch](screenshots/02-git-commit/07-git-branch.png)

### Step 8: Check Remote Repository

**Command:**

```powershell
git remote -v
```

**Screenshot:** Save the remote configuration output as `screenshots/02-git-commit/08-git-remote.png`.

![Git remote configuration](screenshots/02-git-commit/08-git-remote.png)

### Step 9: Push Changes to GitHub

**Command:**

```powershell
git push
```

If Git reports that the branch has no upstream, configure the correct upstream before retrying.

**Screenshot:** Save the successful push output as `screenshots/02-git-commit/09-git-push.png`.

![Successful Git push](screenshots/02-git-commit/09-git-push.png)

### Step 10: Verify the GitHub Repository

Open the repository in your browser and verify that the committed files are present.

**Screenshot:** Save the GitHub repository page as `screenshots/02-git-commit/10-github-repository.png`.

![GitHub repository](screenshots/02-git-commit/10-github-repository.png)



## 2.4 Verification Criteria

- The intended project files are committed.
- The commit hash appears in Git history.
- The working tree is clean, except for intentional changes.
- The remote repository is configured when GitHub integration is required.
- The pushed commit is visible on GitHub.

## 2.5 Outcome

This stage documents the Git version-control workflow, from reviewing changes and staging files to creating commits and verifying the remote repository.

All screenshots must be captured from the actual terminal or browser and saved at the specified paths. Images will display automatically in GitHub's README preview once the files are committed and pushed.

# Stage 3 — Continuous Integration (CI) Pipeline

## 1. Overview

Continuous Integration (CI) is a DevOps practice in which code changes are automatically checked whenever developers push code to a repository or create a pull request.

In this stage, the TaskBoard application is prepared for automated validation through GitHub Actions.

### Objectives

- Understand the purpose of a CI pipeline.
- Inspect the GitHub Actions configuration.
- Configure workflow triggers.
- Run automated application checks.
- Inspect workflow execution logs.
- Identify and troubleshoot pipeline failures.
- Verify successful execution through GitHub Actions.
- Maintain screenshots as project documentation.

---

## 2. CI Pipeline Workflow

The expected workflow is:

```text
Developer writes code
        |
        v
Git add and Git commit
        |
        v
Git push to GitHub
        |
        v
GitHub Actions workflow starts
        |
        v
Install dependencies
        |
        v
Run automated checks
        |
        v
Pipeline result
   /          \
  v            v
Success      Failure
  |            |
  v            v
Continue     Inspect logs
deployment   and fix errors
```

**Screenshot 1 — CI pipeline overview**

Save a screenshot of the workflow diagram or your pipeline overview as:

`screenshots/03-ci-pipeline/01-ci-pipeline-overview.png`

![CI pipeline overview](screenshots/03-ci-pipeline/01-ci-pipeline-overview.png)

---

## 3. Inspect the Project Structure

Open PowerShell in the project root directory.

```powershell
Get-Location
```

**Screenshot 2 — Project working directory**

Save as `screenshots/03-ci-pipeline/02-project-directory.png`.

![Project directory](screenshots/03-ci-pipeline/02-project-directory.png)

Inspect the GitHub configuration directory:

```powershell
Get-ChildItem .github -Recurse
```

**Screenshot 3 — GitHub configuration files**

Save as `screenshots/03-ci-pipeline/03-github-config-files.png`.

![GitHub configuration files](screenshots/03-ci-pipeline/03-github-config-files.png)

A standard GitHub Actions workflow is stored inside `.github/workflows/` and uses a `.yml` or `.yaml` extension.

> Note: A file named `ci-cd-notes.txt` is not automatically executed as a GitHub Actions workflow. If it contains notes rather than workflow configuration, keep it outside the workflows directory.

---

## 4. Inspect the CI Workflow

List workflow files:

```powershell
Get-ChildItem .github/workflows
```

**Screenshot 4 — Workflow directory**

Save as `screenshots/03-ci-pipeline/04-workflow-directory.png`.

![Workflow directory](screenshots/03-ci-pipeline/04-workflow-directory.png)

If a YAML workflow exists, display its contents:

```powershell
Get-Content .github/workflows/ci.yml
```

**Screenshot 5 — CI workflow configuration**

Save as `screenshots/03-ci-pipeline/05-ci-workflow-code.png`.

![CI workflow configuration](screenshots/03-ci-pipeline/05-ci-workflow-code.png)

If your workflow has a different filename, replace `ci.yml` with the actual filename. Do not create or assume a workflow file exists until you have inspected the directory.

A typical CI workflow defines:

- **Trigger:** Events that start the workflow, such as a push or pull request.
- **Runner:** The machine or environment that executes the job.
- **Steps:** Commands that validate the application.
- **Result:** Whether the job succeeds or fails.

---

## 5. Validate the Workflow Before Pushing

Check the working tree:

```powershell
git status
```

**Screenshot 6 — Git status before CI push**

Save as `screenshots/03-ci-pipeline/06-git-status-before-push.png`.

![Git status before push](screenshots/03-ci-pipeline/06-git-status-before-push.png)

Review the changes:

```powershell
git diff
```

**Screenshot 7 — Review CI changes**

Save as `screenshots/03-ci-pipeline/07-ci-code-diff.png`.

![CI code diff](screenshots/03-ci-pipeline/07-ci-code-diff.png)

Stage the intended files:

```powershell
git add .github
```

**Screenshot 8 — Stage workflow files**

Save as `screenshots/03-ci-pipeline/08-stage-workflow-files.png`.

![Stage workflow files](screenshots/03-ci-pipeline/08-stage-workflow-files.png)

Check the staged changes:

```powershell
git diff --cached
```

**Screenshot 9 — Staged CI changes**

Save as `screenshots/03-ci-pipeline/09-staged-ci-diff.png`.

![Staged CI changes](screenshots/03-ci-pipeline/09-staged-ci-diff.png)

Only stage the intended files. If `.github` contains notes or unrelated files, stage the specific workflow file instead.

---

## 6. Commit and Push the CI Configuration

Commit the reviewed changes:

```powershell
git commit -m "Add CI pipeline configuration"
```

**Screenshot 10 — CI configuration commit**

Save as `screenshots/03-ci-pipeline/10-ci-commit.png`.

![CI configuration commit](screenshots/03-ci-pipeline/10-ci-commit.png)

Push the branch:

```powershell
git push
```

**Screenshot 11 — Push CI changes to GitHub**

Save as `screenshots/03-ci-pipeline/11-ci-git-push.png`.

![Push CI changes](screenshots/03-ci-pipeline/11-ci-git-push.png)

If GitHub rejects the push, resolve the authentication or permission issue before treating the push as successful.

---

## 7. Verify the Workflow on GitHub

Open your repository on GitHub and select the **Actions** tab.

**Screenshot 12 — GitHub Actions dashboard**

Save as `screenshots/03-ci-pipeline/12-github-actions-dashboard.png`.

![GitHub Actions dashboard](screenshots/03-ci-pipeline/12-github-actions-dashboard.png)

Select the workflow run triggered by your push.

**Screenshot 13 — CI workflow run**

Save as `screenshots/03-ci-pipeline/13-ci-workflow-run.png`.

![CI workflow run](screenshots/03-ci-pipeline/13-ci-workflow-run.png)

Open the job to inspect its steps.

**Screenshot 14 — CI job steps**

Save as `screenshots/03-ci-pipeline/14-ci-job-steps.png`.

![CI job steps](screenshots/03-ci-pipeline/14-ci-job-steps.png)

Open the relevant step to view its logs.

**Screenshot 15 — CI execution logs**

Save as `screenshots/03-ci-pipeline/15-ci-execution-logs.png`.

![CI execution logs](screenshots/03-ci-pipeline/15-ci-execution-logs.png)

---

## 8. Troubleshooting

If the workflow fails, inspect the failed step and its logs before changing the configuration.

| Problem | What to check |
|---|---|
| Workflow does not start | Confirm the workflow is valid YAML and the push or pull-request trigger matches your event and branch. |
| Workflow file is not detected | Confirm it is under `.github/workflows/` and ends in `.yml` or `.yaml`. |
| Dependency installation fails | Inspect the dependency files and installation command. |
| Tests fail | Read the test output and reproduce the failure locally. |
| Git push is rejected | Check repository access and token permissions. |
| Workflow fails on a secret | Configure the required secret in repository settings; never commit credentials. |

**Screenshot 16 — Failed workflow or troubleshooting logs**

Save as `screenshots/03-ci-pipeline/16-ci-troubleshooting.png`.

![CI troubleshooting](screenshots/03-ci-pipeline/16-ci-troubleshooting.png)

If your pipeline succeeds on the first attempt, use this screenshot slot for a successful run's logs instead.

---

## 9. Final Verification Checklist

- [ ] Inspected the `.github` directory.
- [ ] Identified the actual CI workflow file.
- [ ] Reviewed the workflow configuration.
- [ ] Checked the changes before committing.
- [ ] Committed the intended CI files.
- [ ] Successfully pushed the commit to GitHub.
- [ ] Confirmed the workflow started.
- [ ] Inspected the job steps and logs.
- [ ] Recorded the result using genuine screenshots.

**Screenshot 17 — Final successful CI run**

Save as `screenshots/03-ci-pipeline/17-ci-success.png`.

![Final successful CI run](screenshots/03-ci-pipeline/17-ci-success.png)

---

## 10. Conclusion

This stage documents the CI pipeline setup and verification process for the TaskBoard DevOps capstone. The GitHub Actions dashboard and execution logs provide evidence of whether automated validation ran successfully.

The pipeline should only be marked successful after a real workflow run completes successfully. A screenshot placeholder alone is not proof of execution.

