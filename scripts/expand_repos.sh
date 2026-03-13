#!/bin/bash
# NEXUS Repo Expansion Script
# Aggressive cloning with smart categorization
# Rule: Clone for capability, install only when needed

set -e

echo "⚡ NEXUS Repo Expansion"
echo "======================="
echo ""

REPO_BASE="/Users/tomegathericon/clawd/repos"
mkdir -p "$REPO_BASE"

cd "$REPO_BASE"

# Track stats
CLONED=0
FAILED=0
EXISTING=0

# Function to clone with dedup
git_clone_smart() {
    local url="$1"
    local name=$(basename "$url" .git)
    
    if [ -d "$name" ]; then
        echo "  ○ $name exists"
        EXISTING=$((EXISTING + 1))
        return 0
    fi
    
    if git clone --depth 1 --single-branch "$url" "$name" 2>/dev/null; then
        echo "  ✓ $name cloned"
        CLONED=$((CLONED + 1))
        return 0
    else
        echo "  ✗ $name failed"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo "📦 Phase 1: Core Infrastructure & DevOps"
echo "----------------------------------------"

# Infrastructure as Code
repos_infra=(
    "https://github.com/hashicorp/terraform.git"
    "https://github.com/pulumi/pulumi.git"
    "https://github.com/kubernetes/kubernetes.git"
    "https://github.com/helm/helm.git"
    "https://github.com/argoproj/argo-cd.git"
    "https://github.com/grafana/grafana.git"
    "https://github.com/prometheus/prometheus.git"
    "https://github.com/jaegertracing/jaeger.git"
)

for repo in "${repos_infra[@]}"; do
    git_clone_smart "$repo"
done

echo ""
echo "📦 Phase 2: Security & Compliance"
echo "-----------------------------------"

repos_security=(
    "https://github.com/owasp/zap.git"
    "https://github.com/aquasecurity/trivy.git"
    "https://github.com/hashicorp/vault.git"
    "https://github.com/anchore/grype.git"
    "https://github.com/snyk/snyk.git"
)

for repo in "${repos_security[@]}"; do
    git_clone_smart "$repo"
done

echo ""
echo "📦 Phase 3: Data & Databases"
echo "-----------------------------"

repos_data=(
    "https://github.com/apache/kafka.git"
    "https://github.com/redis/redis.git"
    "https://github.com/mongodb/mongo.git"
    "https://github.com/postgres/postgres.git"
    "https://github.com/duckdb/duckdb.git"
    "https://github.com/apache/spark.git"
    "https://github.com/dbt-labs/dbt-core.git"
)

for repo in "${repos_data[@]}"; do
    git_clone_smart "$repo"
done

echo ""
echo "📦 Phase 4: AI/ML Infrastructure"
echo "---------------------------------"

repos_ai=(
    "https://github.com/mlflow/mlflow.git"
    "https://github.com/kubeflow/kubeflow.git"
    "https://github.com/ray-project/ray.git"
    "https://github.com/huggingface/transformers.git"
    "https://github.com/invoke-ai/InvokeAI.git"
)

for repo in "${repos_ai[@]}"; do
    git_clone_smart "$repo"
done

echo ""
echo "📦 Phase 5: Business/Enterprise Tools"
echo "--------------------------------------"

repos_business=(
    "https://github.com/n8n-io/n8n.git"
    "https://github.com/ToolJet/ToolJet.git"
    "https://github.com/appsmithorg/appsmith.git"
    "https://github.com/metabase/metabase.git"
    "https://github.com/apache/superset.git"
)

for repo in "${repos_business[@]}"; do
    git_clone_smart "$repo"
done

echo ""
echo "======================="
echo "✅ Expansion Complete"
echo "======================="
echo "Cloned: $CLONED"
echo "Existing: $EXISTING"
echo "Failed: $FAILED"
echo ""
echo "Total repos in $REPO_BASE:"
ls -1 | wc -l
echo ""
echo "Disk usage:"
du -sh .
