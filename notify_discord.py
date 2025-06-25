import os
import json
import requests
import re


# Load GitHub context and event payload\
def load_event_context():
    event_name = os.getenv("GITHUB_EVENT_NAME")
    if not event_name:
        raise ValueError("GITHUB_EVENT_NAME environment variable is not set")

    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        raise ValueError("GITHUB_EVENT_PATH environment variable is not set")

    with open(event_path, "r") as f:
        event = json.load(f)

    return event_name, event.get("action"), event


def load_user_map():
    with open("user_map.json", "r") as f:
        user_map = json.load(f)

        return user_map


def load_webhook_url():
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError(
            "DISCORD_WEBHOOK_URL environment variable is missing or empty."
        )

    return webhook_url


def post_to_discord(message: str, webhook_url: str):
    if not webhook_url:
        raise ValueError("DISCORD_WEBHOOK_URL environment variable is not set")
    payload = {"content": message}
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()


def generate_developer_list(assignees, user_map):
    return [
        f"<@{user_map[user['login']]}>"
        for user in assignees
        if user["login"] in user_map
    ]


def notify_assignment(obj, user_map, webhook_url):
    title = obj.get("title", "Untitled")
    url = obj.get("html_url", "")
    assignees = obj.get("assignees", [])

    mentions = generate_developer_list(assignees, user_map)

    if mentions:
        message = (
            f"📌 **Assignment Notice**\n"
            f"🔗 [{title}]({url})\n"
            f"👤 Assigned to: {', '.join(mentions)}"
        )
        post_to_discord(message, webhook_url)


def notify_review_request(pr_obj, user_map, webhook_url):
    title = pr_obj.get("title", "Untitled")
    url = pr_obj.get("html_url", "")
    reviewers = pr_obj.get("requested_reviewers", [])

    mentions = generate_developer_list(reviewers, user_map)
    if mentions:
        message = (
            f"🔍 **Review Requested**\n"
            f"🔗 [{title}]({url})\n"
            f"👤 Reviewers: {', '.join(mentions)}"
        )
        post_to_discord(message, webhook_url)


# Notify review state changes to the assignee
def notify_review_state_change(pr_obj, state: str, user_map, webhook_url):
    title = pr_obj.get("title", "Untitled")
    url = pr_obj.get("html_url", "")
    assignee = pr_obj.get("assignee", {})

    mentioned_assignee = f"<@{user_map[assignee['login']]}>"

    message = (
        f"🔔 **PR Review State Change**\n"
        f"🔗 [{title}]({url})\n"
        f"🔄 State: {state}\n"
        f"👤 Assigned to: {mentioned_assignee}"
    )
    post_to_discord(message, webhook_url)


def notify_comment_mention(comment_body: str, context_obj, user_map, webhook_url):
    mentioned_users = re.findall(r"@(\w+)", comment_body)

    mentions = [
        f"<@{user_map[login]}>" for login in mentioned_users if login in user_map
    ]

    if mentions:
        message = (
            f"💬 **Mention in Comment**\n"
            f"🔗 [{context_obj.get('title', 'Untitled')}]({context_obj.get('html_url', '')})\n"
            f"👤 Mentioned: {', '.join(mentions)}\n"
            f'📝 "{comment_body.strip()}"'
        )
        post_to_discord(message, webhook_url)


def main():
    event_name, event_action, event = load_event_context()
    user_map = load_user_map()
    webhook_url = load_webhook_url()

    # === Event dispatch ===

    print(f"Event Name: {event_name}, Action: {event_action}")
    # 1. Valid assignment events
    if event_name == "issues" and event_action in ["opened", "assigned"]:
        notify_assignment(event["issue"], user_map, webhook_url)

    # 2. Valid review request events
    elif event_name == "pull_request" and event_action in ["review_requested"]:
        notify_review_request(event["pull_request"], user_map, webhook_url)

    # 3. Valid request review events
    elif event_name == "pull_request_review" and event_action in ["submitted"]:
        state = event["review"].get("state")
        print(f"Review state: {state}")
        if state == "approved":
            notify_review_state_change(
                event["pull_request"], "approved", user_map, webhook_url
            )
        elif state == "changes_requested":
            notify_review_state_change(
                event["pull_request"], "changes requested", user_map, webhook_url
            )

    # 4. Valid comment events with possible @mentions
    elif (
        event_name in ["issue_comment", "pull_request_review_comment"]
        and "comment" in event
    ):
        comment_body = event["comment"]["body"]
        context_obj = event.get("issue") or event.get("pull_request", {})
        notify_comment_mention(comment_body, context_obj, user_map, webhook_url)
