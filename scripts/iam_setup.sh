#!/usr/bin/env bash
# Lesson 7 - the same hands-on as the console, but with the AWS CLI.
# Run each command ONE BY ONE and read the output (do not blindly run the file).
# Requires an admin-capable profile (not the root user!) configured via `aws configure`.
set -euo pipefail

# 1. Create a group for developers and give it read-only S3 access
aws iam create-group --group-name developers
aws iam attach-group-policy --group-name developers \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# 2. Create the user "meera-dev" and put it in the group
aws iam create-user --user-name meera-dev
aws iam add-user-to-group --user-name meera-dev --group-name developers

# 3. (Optional, Lesson 8) create access keys for programmatic access.
#    The secret is shown ONCE. Store it safely - never paste it in chat or code.
# aws iam create-access-key --user-name meera-dev

# 4. See who is in the group and what they can do
aws iam get-group --group-name developers
aws iam list-attached-group-policies --group-name developers

# 5. CLEAN UP when finished
# aws iam remove-user-from-group --user-name meera-dev --group-name developers
# aws iam delete-user --user-name meera-dev
# aws iam detach-group-policy --group-name developers --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
# aws iam delete-group --group-name developers
