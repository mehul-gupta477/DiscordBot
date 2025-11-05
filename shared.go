package types

import (
	"context"
	"encoding/json"
	"time"

	"github.com/propel-gtm/propel-gtm/api/checkrun"
	"github.com/propel-gtm/propel-gtm/api/clients"
	"github.com/propel-gtm/propel-gtm/api/logging"
	"github.com/propel-gtm/propel-gtm/api/models"
	"github.com/propel-gtm/propel-gtm/api/utils"
	"go.uber.org/zap"
	"gorm.io/gorm"
)

// Helper function to check if a PR is merged
func IsMergedPR(prDetails *clients.PullRequestDetails) bool {
	return prDetails.State == "closed" && prDetails.MergedAt != nil
}

func ShouldProcessWorkflow(
	ctx context.Context,
	db *gorm.DB,
	prContext *models.PullRequestContext,
	config WorkflowConfig,
	repoWorkflowSetting *models.RepoWorkflowSetting,
	prDetails *clients.PullRequestDetails,
) bool {
	func ShouldProcessWorkflow(
	ctx context.Context,
	db *gorm.DB,
	prContext *models.PullRequestContext,
	config WorkflowConfig,
	repoWorkflowSetting *models.RepoWorkflowSetting,
	prDetails *clients.PullRequestDetails,
) bool {
	logger := logging.GetGlobalLogger().With(
		zap.String("repo_name", prContext.FullRepoName),
		zap.Int("pr_number", prContext.PRNumber),
		zap.String("workflow", string(config.WorkflowType)),
		zap.String("action", prContext.Action),
		zap.String("pr_context_commit_sha", prContext.CommitSHA),
		zap.String("pr_details_head_sha", prDetails.Head.SHA),
	)

	var reviewDraftPr bool
	switch config.WorkflowType {
	case models.WorkflowTypePR_SUMMARY:
		con, err := repoWorkflowSetting.GetPRSummaryConfig()
		if err != nil {
			return false
		}
		reviewDraftPr = con.ProcessDraftPRs
	case models.WorkflowTypeCODE_REVIEW:
		con, err := repoWorkflowSetting.GetCodeReviewConfig()
		if err != nil {
			return false
		}
		reviewDraftPr = con.ProcessDraftPRs
	}
case models.WorkflowTypeCODE_REVIEW:
		con, err := repoWorkflowSetting.GetCodeReviewConfig()
		if err != nil {
			return false
		}
		reviewDraftPr = con.ProcessDraftPRs
	}

	shouldStopIfPRDraft := prDetails.Draft
	if reviewDraftPr {
		shouldStopIfPRDraft = false
	}

	// First check if it's a draft PR - this applies to all workflows except PR_REACTION_SYNC
	if shouldStopIfPRDraft && config.WorkflowType != models.WorkflowTypePR_REACTION_SYNC {
		logger.Info("Skipping workflow for draft PR")
		return false
	}

	// Special handling for PR reaction sync workflow
	if config.WorkflowType == models.WorkflowTypePR_REACTION_SYNC {
		// For reaction sync, we want to process closed and merged PRs
		if IsMergedPR(prDetails) {
			logger.Info("Processing workflow for merged/closed PR")
			return true
		}
		logger.Info("Skipping workflow for non-merged/open PR")
		return false
	}

	// For other workflows, check if PR is closed
	if prDetails.State != "open" {
	
	// For other workflows, check if PR is closed
	if prDetails.State != "open" {
		logger.Info("Skipping workflow for closed/merged PR")
		return false
	}

	// Check for new commits
	if prDetails.Head.SHA != prContext.CommitSHA {
		logger.Info("Skipping workflow because there have been new commits since this event")

		// Terminate any active AI Review check runs for the old commit SHA
		// Only do this for code review workflows to avoid unnecessary API calls
		if config.WorkflowType == models.WorkflowTypeCODE_REVIEW {
			go func() {
				ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
				defer cancel()
				if err := checkrun.TerminateAIReviewCheckRunsForInstallation(
					ctx,
					prContext.InstallationID,
					prContext.Owner,
					prContext.RepositoryName,
					prContext.CommitSHA,
					prContext.EnterpriseHostname,
				); err != nil {
					logger.Warn("Failed to terminate AI Review check runs for outdated commit",
						zap.Error(err))
				} else {
					logger.Info("Successfully terminated AI Review check runs for outdated commit")
				}
			}()
		}

		return false
	}

	// Check if action is valid for this workflow using the function
	isValidAction := config.ValidActions(ctx, prContext, repoWorkflowSetting, prDetails)

	if !isValidAction {
		logger.Info("Skipping workflow due to unwanted action type")
		return false
	}

	// Check branch targeting configuration
	if !ShouldProcessBasedOnBranchTargeting(repoWorkflowSetting, prDetails, logger, string(config.WorkflowType), prContext.PRNumber, prContext.FullRepoName) {
		return false
	}

	return true
}

// ShouldProcessBasedOnBranchTargeting checks if a PR should be processed based on branch targeting configuration
func ShouldProcessBasedOnBranchTargeting(repoWorkflowSetting *models.RepoWorkflowSetting, prDetails *clients.PullRequestDetails, logger *zap.Logger, workflowType string, prNumber int, repoName string) bool {
	logger = logger.With(
		zap.String("repo_name", repoName),
		zap.String("workflow", workflowType),
		zap.Int("pr_number", prNumber),
	)

	// If branch targeting is not enabled, process all PRs
	if !repoWorkflowSetting.BranchTargetingEnabled {
		return true
	}

	logger.Info("Branch targeting enabled for repo")

	// Get the target branch (base branch) of the PR
	targetBranch := prDetails.Base.Ref

	// Parse branch filter patterns from JSON
	var branchPatterns []string
	if len(repoWorkflowSetting.BranchFilterPatterns) > 0 {
		err := json.Unmarshal(repoWorkflowSetting.BranchFilterPatterns, &branchPatterns)
		if err != nil {
			logger.Error("Failed to unmarshal branch_filter_patterns",
				zap.Error(err),
				zap.Uint("settingID", repoWorkflowSetting.ID))
			// Fail closed: if patterns can't be read, don't process
			return false
		}
	}

	if len(branchPatterns) > 0 {
		matched := false
		for _, pattern := range branchPatterns {
			branchMatch, err := utils.Match(pattern, targetBranch)
			if err != nil {
				logger.Error("Error compiling glob pattern for branch filter",
					zap.String("pattern", pattern),
					zap.Error(err))
				continue // Skip faulty pattern
			}
			if branchMatch {
				matched = true
				break
			}
		}

		if repoWorkflowSetting.BranchFilterMode == "denylist" && matched {
			logger.Info("Skipping workflow due to denylisted target branch",
				zap.String("targetBranch", targetBranch))
			return false
		} else if repoWorkflowSetting.BranchFilterMode == "allowlist" && !matched {
			logger.Info("Skipping workflow due to non-allowlisted target branch",
				zap.String("targetBranch", targetBranch))
			return false
		}
	} else if repoWorkflowSetting.BranchFilterMode == "allowlist" {
		// Allowlist mode with no patterns means deny all
		logger.Info("Skipping workflow due to empty allowlist for target branch",
			zap.String("targetBranch", targetBranch))
		return false
	}

	logger.Info("Target branch is allowed",
		zap.String("targetBranch", targetBranch))

	return true
}
