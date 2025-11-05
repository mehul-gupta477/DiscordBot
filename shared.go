package services

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/propel-gtm/propel-gtm/api/clients"
	"github.com/propel-gtm/propel-gtm/api/utils"
	"go.uber.org/zap"
)

// LibraryCommentValidator handles validation and enhancement of library-related comments using AI and MCP servers
type LibraryCommentValidator struct {
	aiConfig clients.AIConfig
}

// LibraryClassificationResult represents the result of library comment classification
type LibraryClassificationResult struct {
	IsLibraryRelated bool     `json:"is_library_related"`
	LibraryType      string   `json:"library_type"` // "version", "method", "deprecation", "dependency", "api"
	Confidence       float64  `json:"confidence"`
	Libraries        []string `json:"libraries,omitempty"`
}

// LibraryInfo contains extracted information about a library mentioned in a comment
type LibraryInfo struct {
	Name       string   `json:"name"`
	Version    string   `json:"version,omitempty"`
	Methods    []string `json:"methods,omitempty"`
	ChangeType string   `json:"change_type"` // "version_update", "method_usage", "deprecation", "breaking_change"
	Language   string   `json:"language,omitempty"`
	Context    string   `json:"context,omitempty"`
}

// ValidationResult contains the result of validating a library comment
type ValidationResult struct {
	IsCorrect         bool                   `json:"is_correct"`
	Confidence        float64                `json:"confidence"`
	Issues            []string               `json:"issues,omitempty"`
	Recommendations   []string               `json:"recommendations,omitempty"`
	Sources           []ValidationSource     `json:"sources,omitempty"`
	CurrentUsage      string                 `json:"current_usage,omitempty"`
	RecommendedUsage  string                 `json:"recommended_usage,omitempty"`
	BreakingChanges   []string               `json:"breaking_changes,omitempty"`
	Documentation     string                 `json:"documentation,omitempty"`
	AdditionalContext map[string]interface{} `json:"additional_context,omitempty"`
}

// ValidationSource represents a source used for validation
type ValidationSource struct {
	Type        string  `json:"type"` // "chroma_mcp", "web_search", "context7_mcp"
	Content     string  `json:"content"`
	Reliability float64 `json:"reliability"` // 0.0 - 1.0
	URL         string  `json:"url,omitempty"`
}

// LibraryValidationResponse represents the response from library validation AI
type LibraryValidationResponse struct {
	Comments []LibraryValidationResult `json:"comments"`
}

// LibraryValidationResult represents the validation result for a single comment
type LibraryValidationResult struct {
	ID               string            `json:"id"`
	IsLibraryRelated bool              `json:"is_library_related"`
	NeedsValidation  bool              `json:"needs_validation"`
	LibraryInfo      *LibraryInfo      `json:"library_info,omitempty"`
	ValidationResult *ValidationResult `json:"validation_result,omitempty"`
	EnhancedComment  string            `json:"enhanced_comment,omitempty"`
	ProcessingNotes  []string          `json:"processing_notes,omitempty"`
}

// NewLibraryCommentValidator creates a new library comment validator
func NewLibraryCommentValidator(aiConfig clients.AIConfig) *LibraryCommentValidator {
	return &LibraryCommentValidator{
		aiConfig: aiConfig,
	}
}

// ValidateAndEnhanceComments validates and enhances library-related comments
func (v *LibraryCommentValidator) ValidateAndEnhanceComments(
	ctx context.Context,
	generatedComments []*InternalReviewComment,
	owner string,
	repo string,
	logger *zap.Logger,
) ([]*InternalReviewComment, error) {

	if len(generatedComments) == 0 {
		logger.Info("No comments to validate")
		return generatedComments, nil
	}

	logger.Info("Starting library comment validation and enhancement",
		zap.Int("comment_count", len(generatedComments)))

	startTime := time.Now()

	// Step 1: Classify and extract library information from comments
	libraryValidationResults, err := v.classifyAndValidateComments(ctx, generatedComments, owner, repo, logger)
	if err != nil {
		logger.Error("Failed to classify and validate library comments", zap.Error(err))
		return generatedComments, fmt.Errorf("failed to classify and validate library comments: %w", err)
	}

	// Step 2: Apply enhancements to comments that need it
	enhancedComments := v.applyLibraryValidationResults(generatedComments, libraryValidationResults, logger)

	processingTime := time.Since(startTime)
	enhancedCount := 0
	for _, result := range libraryValidationResults {
		if result.IsLibraryRelated && result.EnhancedComment != "" {
			enhancedCount++
		}
	}

	logger.Info("Library comment validation completed",
		zap.Int("original_count", len(generatedComments)),
		zap.Int("enhanced_count", enhancedCount),
		zap.Duration("processing_time", processingTime))

	return enhancedComments, nil
}

// classifyAndValidateComments classifies comments and validates library-related ones
func (v *LibraryCommentValidator) classifyAndValidateComments(
	ctx context.Context,
	comments []*InternalReviewComment,
	owner string,
	repo string,
	logger *zap.Logger,
) ([]LibraryValidationResult, error) {

	// Build system message for library classification and validation
	systemMessage := v.buildLibraryValidationSystemMessage()

	// Build user message with comments to analyze
	userMessage := v.buildLibraryValidationUserMessage(comments, owner, repo)

	logger.Debug("Calling AI for library comment classification and validation",
		zap.Int("comment_count", len(comments)))

	// Use Anthropic with both Chroma MCP and Context7 MCP plus Web Search for comprehensive validation
	response, err := v.aiConfig.CallAnthropicWithModel(ctx, systemMessage, userMessage, v.aiConfig.GetAnthropicModel(), true, true)
	if err != nil {
		logger.Error("Failed to call AI for library validation", zap.Error(err))
		return nil, fmt.Errorf("failed to call AI for library validation: %w", err)
	}

	// Parse the AI response
	var validationResponse LibraryValidationResponse
	if err := SanitizeAndParseJSON(response, &validationResponse); err != nil {
		logger.Error("Failed to parse library validation response",
			zap.Error(err),
			zap.String("response", utils.TruncateString(response, 500)))
		return nil, fmt.Errorf("failed to parse library validation response: %w", err)
	}

	logger.Info("Library validation response parsed",
		zap.Int("results_count", len(validationResponse.Comments)))

	return validationResponse.Comments, nil
}

// buildLibraryValidationSystemMessage creates the system message for library validation
func (v *LibraryCommentValidator) buildLibraryValidationSystemMessage() string {
	return `You are a library and package expert code review assistant. Your task is to:

1. CLASSIFY comments as library-related or not
2. EXTRACT library information from library-related comments
3. VALIDATE library-related comments using available tools
4. ENHANCE incorrect or incomplete library comments

A comment is LIBRARY-RELATED if it mentions:
- Library/package version changes or updates
- API method usage, deprecation, or changes
- Framework upgrades or migrations
- Dependency management issues
- Breaking changes in libraries
- Security vulnerabilities in packages
- Performance implications of library choices

For LIBRARY-RELATED comments:
1. Extract library information (name, version, methods, change type)
2. Use available MCP tools to search the codebase for current usage
3. Use web search to find latest documentation and best practices
4. Validate the comment against current reality
5. If incorrect/incomplete, enhance with accurate information

TOOLS AVAILABLE:
- Chroma MCP (code-collections): Search codebase for current library usage patterns and implementations
  * Use to find: How libraries are currently used in this codebase, existing patterns, import statements
- Context7 MCP (context7-docs): Get up-to-date, version-specific library documentation and examples  
  * Use to get: Official documentation, API references, version-specific changes, best practices
- Web Search: Find latest library documentation, changelogs, and community discussions
  * Use to find: Breaking changes, migration guides, security advisories, community feedback

WORKFLOW:
1. For library-related comments, use Chroma MCP to understand current codebase usage
2. Use Context7 MCP to get official, up-to-date documentation for the specific library version
3. Use Web Search to validate against latest changes, security issues, or migration guides
4. Compare comment accuracy against all three sources
5. If incorrect, enhance with accurate information from the most reliable source

For each comment, provide:
- Classification (is_library_related: true/false)
- Library information extraction (if applicable)
- Validation result with confidence score
- Enhanced comment (if needed) - ONLY the corrected comment text, without validation details
- Processing notes explaining your reasoning

ENHANCED COMMENT FORMAT RULES:
- If the comment is CORRECT: Leave enhanced_comment empty (do not include validation details)
- If the comment is INCORRECT: Provide ONLY the corrected comment text in enhanced_comment
- DO NOT include validation details (like "**Validation**: This comment is accurate...") in enhanced_comment
- The enhanced_comment should be the actual comment that will be shown to the developer
- Validation details belong in validation_result, NOT in enhanced_comment

Respond with JSON in this exact format:
{
  "comments": [
    {
      "id": "0",
      "is_library_related": true,
      "needs_validation": true,
      "library_info": {
        "name": "react",
        "version": "18.0.0",
        "methods": ["useEffect", "useState"],
        "change_type": "method_usage",
        "language": "typescript",
        "context": "hook usage pattern"
      },
      "validation_result": {
        "is_correct": false,
        "confidence": 0.8,
        "issues": ["Outdated usage pattern"],
        "recommendations": ["Use new React 18 patterns"],
        "current_usage": "Found 15 files using old pattern",
        "recommended_usage": "Use concurrent features",
        "documentation": "https://react.dev/reference/react"
      },
      "enhanced_comment": "Use the new React 18 concurrent features instead of the legacy patterns...",
      "processing_notes": ["Found current usage in codebase", "Validated against React 18 docs"]
    }
  ]
}

CRITICAL: Return ONLY the JSON object, no additional text.`
}

// buildLibraryValidationUserMessage creates the user message for library validation
func (v *LibraryCommentValidator) buildLibraryValidationUserMessage(
	comments []*InternalReviewComment,
	owner string,
	repo string,
) string {

	// Format comments for analysis
	commentsData := make([]map[string]interface{}, 0, len(comments))
	for i, comment := range comments {
		if comment == nil {
			continue
		}
		commentData := map[string]interface{}{
			"id":   fmt.Sprintf("%d", i),
			"path": comment.Path,
			"line": comment.Line,
			"body": comment.Body,
			"type": comment.Type,
		}
		if comment.StartLine != nil && *comment.StartLine != 0 {
			commentData["start_line"] = *comment.StartLine
		}
		commentsData = append(commentsData, commentData)
	}

	userMessageData := map[string]interface{}{
		"task":        "Analyze comments for library-related content and validate/enhance them",
		"repository":  fmt.Sprintf("%s/%s", owner, repo),
		"comments":    commentsData,
		"instruction": "For each comment: 1) Classify if library-related 2) Extract library info 3) Validate using MCP tools 4) Enhance if needed",
		"context":     "Use Chroma MCP to search codebase for current library usage. Use Context7 MCP for up-to-date documentation. Use web search for additional validation.",
	}

	userMessageJSON, err := json.MarshalIndent(userMessageData, "", "  ")
	if err != nil {
		// Fallback to simple string format
		return fmt.Sprintf("Repository: %s/%s\nComments to analyze: %v", owner, repo, commentsData)
	}

	return string(userMessageJSON)
}

// applyLibraryValidationResults applies validation results to comments
func (v *LibraryCommentValidator) applyLibraryValidationResults(
	originalComments []*InternalReviewComment,
	validationResults []LibraryValidationResult,
	logger *zap.Logger,
) []*InternalReviewComment {

	// Create a map of validation results by comment ID
	validationMap := make(map[string]LibraryValidationResult)
	for _, result := range validationResults {
		validationMap[result.ID] = result
	}

	var enhancedComments []*InternalReviewComment
	for i, comment := range originalComments {
		commentID := fmt.Sprintf("%d", i)

		if result, exists := validationMap[commentID]; exists {
			if result.IsLibraryRelated && result.NeedsValidation && result.EnhancedComment != "" {
				// Create enhanced comment with updated body
				enhanced := *comment
				enhanced.Body = result.EnhancedComment

				logger.Info("Enhanced library-related comment",
					zap.String("comment_id", commentID),
					zap.String("library", getLibraryName(result.LibraryInfo)),
					zap.String("change_type", getChangeType(result.LibraryInfo)),
					zap.Bool("was_enhanced", true))

				enhancedComments = append(enhancedComments, &enhanced)
			} else if result.IsLibraryRelated {
				// Library-related but no enhancement needed
				logger.Info("Library comment validated, no enhancement needed",
					zap.String("comment_id", commentID),
					zap.String("library", getLibraryName(result.LibraryInfo)))

				enhancedComments = append(enhancedComments, comment)
			} else {
				// Not library-related
				enhancedComments = append(enhancedComments, comment)
			}
		} else {
			// No validation result, keep original
			enhancedComments = append(enhancedComments, comment)
		}
	}

	return enhancedComments
}

// Helper functions
func getLibraryName(info *LibraryInfo) string {
	if info != nil {
		return info.Name
	}
	return "unknown"
}

func getChangeType(info *LibraryInfo) string {
	if info != nil {
		return info.ChangeType
	}
	return "unknown"
}
